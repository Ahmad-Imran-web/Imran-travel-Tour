from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class TourItineraryItem(BaseModel):
    day: int
    title: str
    description: str


class TourModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    slug: str
    destination: str
    country: str
    category: str
    duration_days: int
    duration_nights: int
    price: float
    discount_price: Optional[float] = None
    rating: float = 4.8
    reviews_count: int = 12
    featured: bool = False
    image_url: str
    gallery: List[str] = []
    description: str
    highlights: List[str] = []
    itinerary: List[TourItineraryItem] = []
    inclusions: List[str] = []
    exclusions: List[str] = []
    max_group_size: int = 15
    start_dates: List[str] = []
    created_at: Optional[str] = None


class BookingCreate(BaseModel):
    tour_id: str
    tour_title: str
    customer_name: str
    customer_email: str
    customer_phone: str
    travel_date: str
    adults: int = 1
    children: int = 0
    total_price: float
    payment_method: str = "Credit Card"
    special_requests: Optional[str] = ""


class BookingStatusUpdate(BaseModel):
    status: str  # Pending, Confirmed, Completed, Cancelled


class InquiryCreate(BaseModel):
    name: str
    email: str
    phone: str
    destination: Optional[str] = "General Inquiry"
    message: str


class InquiryStatusUpdate(BaseModel):
    status: str  # New, Contacted, Resolved


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    phone: Optional[str] = ""
