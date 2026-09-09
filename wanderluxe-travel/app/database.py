import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import pymongo
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.config import MONGODB_URI, DATABASE_NAME, BASE_DIR

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
JSON_DB_PATH = DATA_DIR / "wanderluxe_db.json"


class FallbackCollection:
    """Document collection simulating MongoDB collection behavior with JSON persistence."""
    def __init__(self, db: "FallbackDatabase", name: str):
        self.db = db
        self.name = name

    def _get_docs(self) -> List[Dict[str, Any]]:
        return self.db.data.setdefault(self.name, [])

    def find(self, filter_query: Optional[Dict[str, Any]] = None, sort_by: Optional[str] = None, reverse: bool = False) -> List[Dict[str, Any]]:
        docs = self._get_docs()
        if not filter_query:
            results = [dict(d) for d in docs]
        else:
            results = []
            for d in docs:
                match = True
                for k, v in filter_query.items():
                    if k == "$or" and isinstance(v, list):
                        or_match = any(all(d.get(ok) == ov for ok, ov in cond.items()) for cond in v)
                        if not or_match:
                            match = False
                            break
                    elif d.get(k) != v:
                        match = False
                        break
                if match:
                    results.append(dict(d))
        if sort_by:
            results.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)
        return results

    def find_one(self, filter_query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        docs = self.find(filter_query)
        return docs[0] if docs else None

    def insert_one(self, document: Dict[str, Any]) -> str:
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = str(uuid.uuid4())
        if "created_at" not in doc:
            doc["created_at"] = datetime.utcnow().isoformat()
        self._get_docs().append(doc)
        self.db.save()
        return doc["_id"]

    def update_one(self, filter_query: Dict[str, Any], update_data: Dict[str, Any]) -> bool:
        docs = self._get_docs()
        for idx, doc in enumerate(docs):
            match = all(doc.get(k) == v for k, v in filter_query.items())
            if match:
                set_fields = update_data.get("$set", update_data)
                docs[idx].update(set_fields)
                docs[idx]["updated_at"] = datetime.utcnow().isoformat()
                self.db.save()
                return True
        return False

    def delete_one(self, filter_query: Dict[str, Any]) -> bool:
        docs = self._get_docs()
        for idx, doc in enumerate(docs):
            match = all(doc.get(k) == v for k, v in filter_query.items())
            if match:
                docs.pop(idx)
                self.db.save()
                return True
        return False

    def count_documents(self, filter_query: Optional[Dict[str, Any]] = None) -> int:
        return len(self.find(filter_query))


class FallbackDatabase:
    """Persistent JSON database simulating MongoDB database."""
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self.load()

    def load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}
        else:
            self.data = {}

    def save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving local DB: {e}")

    def __getitem__(self, name: str) -> FallbackCollection:
        return FallbackCollection(self, name)


class DatabaseManager:
    """Manages real MongoDB client with fallback document database."""
    def __init__(self):
        self.is_mongo_connected = False
        self.client = None
        self.db = None
        self.db_type = "fallback"
        self._init_db()

    def _init_db(self):
        try:
            client = pymongo.MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
            # Test connection
            client.admin.command('ping')
            self.client = client
            self.db = client[DATABASE_NAME]
            self.is_mongo_connected = True
            self.db_type = "mongodb"
            print(f"[OK] Connected to MongoDB at {MONGODB_URI} (DB: {DATABASE_NAME})")
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as err:
            print(f"[INFO] MongoDB not running locally ({err}). Activating persistent local document database engine.")
            self.db = FallbackDatabase(JSON_DB_PATH)
            self.is_mongo_connected = False
            self.db_type = "fallback_json"

    def get_collection(self, collection_name: str):
        if self.is_mongo_connected:
            return self.db[collection_name]
        return self.db[collection_name]


db_manager = DatabaseManager()

def get_db():
    return db_manager.db

def get_tours_col():
    return db_manager.get_collection("tours")

def get_bookings_col():
    return db_manager.get_collection("bookings")

def get_inquiries_col():
    return db_manager.get_collection("inquiries")

def get_users_col():
    return db_manager.get_collection("users")

def get_reviews_col():
    return db_manager.get_collection("reviews")
