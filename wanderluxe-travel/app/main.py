import random
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, Request, HTTPException, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import (
    BASE_DIR, ADMIN_EMAIL, ADMIN_PASSWORD
)
from app.database import (
    db_manager,
    get_tours_col,
    get_bookings_col,
    get_inquiries_col,
    get_users_col
)
from app.seed_data import seed_database, SAMPLE_TOURS, SAMPLE_BOOKINGS, SAMPLE_INQUIRIES
from app.models import (
    TourModel, BookingCreate, BookingStatusUpdate,
    InquiryCreate, InquiryStatusUpdate, UserLogin
)

app = FastAPI(title="WanderLuxe Travel Agency API", version="1.0.0")

# Mount Static Files & Templates
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def render(request: Request, name: str, context: Optional[Dict[str, Any]] = None):
    ctx = context or {}
    return templates.TemplateResponse(request=request, name=name, context=ctx)


@app.on_event("startup")
async def on_startup():
    """Seed initial sample data if empty on server start."""
    seed_database()


# ---------------------------------------------------------
# CUSTOMER FRONTEND ROUTES
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    tours_col = get_tours_col()
    all_tours = tours_col.find()
    featured_tours = [t for t in all_tours if t.get("featured")]
    if not featured_tours:
        featured_tours = all_tours[:6]

    return render(request, "index.html", {
        "active_page": "home",
        "featured_tours": featured_tours,
        "total_tours": len(all_tours)
    })


@app.get("/tours", response_class=HTMLResponse)
async def tours_page(
    request: Request,
    q: Optional[str] = None,
    category: Optional[str] = None,
    duration: Optional[str] = None
):
    tours_col = get_tours_col()
    all_tours = tours_col.find()

    # Apply initial server-side query filters if provided
    filtered = all_tours
    if q:
        ql = q.lower()
        filtered = [
            t for t in filtered
            if ql in t.get("title", "").lower() 
            or ql in t.get("destination", "").lower() 
            or ql in t.get("country", "").lower()
        ]
    if category and category.lower() != "all":
        filtered = [t for t in filtered if t.get("category", "").lower() == category.lower()]

    return render(request, "tours.html", {
        "active_page": "tours",
        "tours": filtered,
        "search_query": q,
        "category_query": category
    })


@app.get("/tour-details", response_class=HTMLResponse)
async def tour_details_page(request: Request, id: str):
    tours_col = get_tours_col()
    tour = tours_col.find_one({"_id": id})
    if not tour:
        # Try finding by slug or first
        all_t = tours_col.find()
        tour = all_t[0] if all_t else None

    if not tour:
        raise HTTPException(status_code=404, detail="Tour package not found")

    return render(request, "tour_details.html", {
        "active_page": "tours",
        "tour": tour
    })


@app.get("/destinations", response_class=HTMLResponse)
async def destinations_page(request: Request):
    return render(request, "destinations.html", {
        "active_page": "destinations"
    })


@app.get("/about", response_class=HTMLResponse)
async def about_page(request: Request):
    return render(request, "about.html", {
        "active_page": "about"
    })


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request):
    return render(request, "contact.html", {
        "active_page": "contact"
    })


@app.get("/booking", response_class=HTMLResponse)
async def booking_page(
    request: Request,
    tour_id: str,
    date: Optional[str] = None,
    adults: int = 2,
    children: int = 0
):
    tours_col = get_tours_col()
    tour = tours_col.find_one({"_id": tour_id})
    if not tour:
        all_t = tours_col.find()
        tour = all_t[0] if all_t else None
    if not tour:
        return RedirectResponse(url="/tours")

    effective_price = tour.get("discount_price") or tour.get("price", 0)
    base_subtotal = (adults * effective_price) + (children * effective_price * 0.5)
    tax_amount = base_subtotal * 0.05
    total_price = base_subtotal + tax_amount

    return render(request, "booking.html", {
        "tour": tour,
        "selected_date": date,
        "adults": adults,
        "children": children,
        "base_subtotal": base_subtotal,
        "tax_amount": tax_amount,
        "total_price": total_price
    })


@app.get("/booking-confirmation/{booking_ref}", response_class=HTMLResponse)
async def booking_confirmation_page(request: Request, booking_ref: str):
    bookings_col = get_bookings_col()
    booking = bookings_col.find_one({"booking_ref": booking_ref})
    if not booking:
        # Try fallback find by ID
        booking = bookings_col.find_one({"_id": booking_ref})
    if not booking:
        all_b = bookings_col.find()
        booking = all_b[0] if all_b else {
            "booking_ref": booking_ref,
            "tour_title": "Luxury Vacation Package",
            "customer_name": "Valued Guest",
            "customer_email": "guest@wanderluxe.com",
            "customer_phone": "+92 300 0000000",
            "travel_date": "2026-06-15",
            "adults": 2,
            "children": 0,
            "total_price": 2500.0,
            "payment_method": "Credit Card",
            "status": "Confirmed"
        }

    return render(request, "confirmation.html", {
        "booking": booking
    })


@app.get("/my-bookings", response_class=HTMLResponse)
async def my_bookings_page(request: Request, email: Optional[str] = None):
    bookings_col = get_bookings_col()
    all_b = bookings_col.find(sort_by="created_at", reverse=True)

    matched = all_b
    if email:
        el = email.strip().lower()
        matched = [
            b for b in all_b
            if el in b.get("customer_email", "").lower()
            or el in b.get("booking_ref", "").lower()
        ]

    return render(request, "my_bookings.html", {
        "bookings": matched,
        "search_email": email
    })


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render(request, "login.html", {})


@app.post("/login")
async def handle_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    if email.strip().lower() == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
        resp = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        resp.set_cookie(key="admin_session", value="authenticated_admin", max_age=86400)
        return resp
    
    # Generic customer redirection
    resp = RedirectResponse(url=f"/my-bookings?email={email}", status_code=status.HTTP_303_SEE_OTHER)
    return resp


@app.get("/logout")
async def handle_logout():
    resp = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    resp.delete_cookie(key="admin_session")
    return resp


# ---------------------------------------------------------
# ADMIN CONSOLE ROUTES
# ---------------------------------------------------------

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    bookings_col = get_bookings_col()
    tours_col = get_tours_col()
    inquiries_col = get_inquiries_col()

    all_bookings = bookings_col.find(sort_by="created_at", reverse=True)
    all_tours = tours_col.find()
    all_inquiries = inquiries_col.find(sort_by="created_at", reverse=True)

    total_revenue = sum(float(b.get("total_price", 0)) for b in all_bookings if b.get("status") != "Cancelled")
    
    return render(request, "admin/dashboard.html", {
        "admin_page": "dashboard",
        "total_revenue": total_revenue,
        "total_bookings": len(all_bookings),
        "total_tours": len(all_tours),
        "total_inquiries": len(all_inquiries),
        "recent_bookings": all_bookings[:5],
        "recent_inquiries": all_inquiries[:4],
        "db_status": db_manager.db_type
    })


@app.get("/admin/tours", response_class=HTMLResponse)
async def admin_tours(request: Request):
    tours_col = get_tours_col()
    all_tours = tours_col.find(sort_by="created_at", reverse=True)
    return render(request, "admin/tours.html", {
        "admin_page": "tours",
        "tours": all_tours,
        "db_status": db_manager.db_type
    })


@app.get("/admin/bookings", response_class=HTMLResponse)
async def admin_bookings(request: Request):
    bookings_col = get_bookings_col()
    all_bookings = bookings_col.find(sort_by="created_at", reverse=True)
    return render(request, "admin/bookings.html", {
        "admin_page": "bookings",
        "bookings": all_bookings,
        "db_status": db_manager.db_type
    })


@app.get("/admin/inquiries", response_class=HTMLResponse)
async def admin_inquiries(request: Request):
    inquiries_col = get_inquiries_col()
    all_inquiries = inquiries_col.find(sort_by="created_at", reverse=True)
    return render(request, "admin/inquiries.html", {
        "admin_page": "inquiries",
        "inquiries": all_inquiries,
        "db_status": db_manager.db_type
    })


# ---------------------------------------------------------
# REST API ENDPOINTS
# ---------------------------------------------------------

# Tours CRUD
@app.get("/api/tours")
async def api_get_tours():
    tours_col = get_tours_col()
    return tours_col.find()


@app.get("/api/tours/{tour_id}")
async def api_get_tour(tour_id: str):
    tours_col = get_tours_col()
    tour = tours_col.find_one({"_id": tour_id})
    if not tour:
        raise HTTPException(status_code=404, detail="Tour package not found")
    return tour


@app.post("/api/tours")
async def api_create_tour(payload: Dict[str, Any]):
    tours_col = get_tours_col()
    if "_id" not in payload:
        payload["_id"] = "tour-" + str(uuid.uuid4())[:8]
    if "created_at" not in payload:
        payload["created_at"] = datetime.utcnow().isoformat()
    if "rating" not in payload:
        payload["rating"] = 4.9
    if "reviews_count" not in payload:
        payload["reviews_count"] = random.randint(10, 50)
    
    tours_col.insert_one(payload)
    return {"message": "Tour created successfully", "tour_id": payload["_id"]}


@app.put("/api/tours/{tour_id}")
async def api_update_tour(tour_id: str, payload: Dict[str, Any]):
    tours_col = get_tours_col()
    success = tours_col.update_one({"_id": tour_id}, payload)
    if not success:
        raise HTTPException(status_code=404, detail="Tour package not found to update")
    return {"message": "Tour updated successfully"}


@app.delete("/api/tours/{tour_id}")
async def api_delete_tour(tour_id: str):
    tours_col = get_tours_col()
    success = tours_col.delete_one({"_id": tour_id})
    if not success:
        raise HTTPException(status_code=404, detail="Tour package not found")
    return {"message": "Tour deleted successfully"}


# Bookings API
@app.get("/api/bookings")
async def api_get_bookings():
    bookings_col = get_bookings_col()
    return bookings_col.find(sort_by="created_at", reverse=True)


@app.post("/api/bookings")
async def api_create_booking(booking: BookingCreate):
    bookings_col = get_bookings_col()
    
    # Generate unique 5-digit booking reference
    ref_num = random.randint(10000, 99999)
    booking_ref = f"WL-{ref_num}"
    
    booking_dict = booking.dict()
    booking_dict["_id"] = f"bk-{ref_num}"
    booking_dict["booking_ref"] = booking_ref
    booking_dict["status"] = "Confirmed"
    booking_dict["created_at"] = datetime.utcnow().isoformat()
    
    bookings_col.insert_one(booking_dict)
    return {"message": "Booking confirmed", "booking_ref": booking_ref, "id": booking_dict["_id"]}


@app.patch("/api/bookings/{booking_id}/status")
async def api_update_booking_status(booking_id: str, status_data: BookingStatusUpdate):
    bookings_col = get_bookings_col()
    success = bookings_col.update_one({"_id": booking_id}, {"status": status_data.status})
    if not success:
        # Try by booking_ref
        success = bookings_col.update_one({"booking_ref": booking_id}, {"status": status_data.status})
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": f"Status updated to {status_data.status}"}


# Inquiries API
@app.get("/api/inquiries")
async def api_get_inquiries():
    inquiries_col = get_inquiries_col()
    return inquiries_col.find(sort_by="created_at", reverse=True)


@app.post("/api/inquiries")
async def api_create_inquiry(inquiry: InquiryCreate):
    inquiries_col = get_inquiries_col()
    inq_dict = inquiry.dict()
    inq_dict["_id"] = "inq-" + str(uuid.uuid4())[:6]
    inq_dict["status"] = "New"
    inq_dict["created_at"] = datetime.utcnow().isoformat()
    
    inquiries_col.insert_one(inq_dict)
    return {"message": "Inquiry submitted successfully", "inquiry_id": inq_dict["_id"]}


@app.patch("/api/inquiries/{inquiry_id}/status")
async def api_update_inquiry_status(inquiry_id: str, status_data: InquiryStatusUpdate):
    inquiries_col = get_inquiries_col()
    success = inquiries_col.update_one({"_id": inquiry_id}, {"status": status_data.status})
    if not success:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return {"message": f"Inquiry marked as {status_data.status}"}


@app.delete("/api/inquiries/{inquiry_id}")
async def api_delete_inquiry(inquiry_id: str):
    inquiries_col = get_inquiries_col()
    success = inquiries_col.delete_one({"_id": inquiry_id})
    if not success:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return {"message": "Inquiry deleted successfully"}


# Database Seed Endpoint
@app.post("/api/seed")
async def api_seed_database():
    tours_col = get_tours_col()
    bookings_col = get_bookings_col()
    inquiries_col = get_inquiries_col()

    # Re-insert any missing sample tours
    seeded_tours = 0
    for t in SAMPLE_TOURS:
        if not tours_col.find_one({"_id": t["_id"]}):
            tours_col.insert_one(t)
            seeded_tours += 1

    return {
        "message": "Tour catalog refreshed successfully",
        "tours_added": seeded_tours
    }
