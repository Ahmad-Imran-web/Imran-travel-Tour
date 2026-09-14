# 🌍 WanderLuxe - Luxury Travel Agency & Tour Operator Website

A responsive, high-converting Travel Agency web application with a complete Customer Portal and an **Operations Admin Panel**. Powered by **Python FastAPI** with native support for real **MongoDB** (and automatic persistent document DB fallback).

---

## ✨ Key Features

### 🌟 Customer Portal
1. **Home Page (`/`)**:
   - Hero banner with dynamic search bar (Destination, Trip Style, Duration).
   - Value propositions (100% Verified Stays, 24/7 Concierge, Best Price Guarantee).
   - Featured Signature Tours with discount pricing and badges.
   - Destinations showcase (Switzerland, Bali, Dubai, Hunza, Maldives, Japan, Turkey, Serengeti).
   - Limited-time promotional discount offer.
   - Verified traveler reviews with 5-star ratings.
   - Newsletter VIP subscription & interactive footer.

2. **Tour Packages Catalog (`/tours`)**:
   - Real-time instant search input.
   - Category filtering (Luxury, Honeymoon, Adventure, Cultural).
   - Price range slider with live feedback ($500 - $4,000).
   - Sorting by Price (Low to High, High to Low), Rating, and Duration.
   - Live counter of matching tours and empty state recovery.

3. **Tour Details Page (`/tour-details?id=...`)**:
   - Photo gallery with thumbnail preview.
   - Highlights checklist.
   - Interactive day-by-day itinerary accordion.
   - Inclusions and exclusions side-by-side.
   - **Live Booking Calculator Widget**: Dynamic guest counter (Adults & Children with 50% discount), departure date selector, tax calculation, and instant total price.

4. **Destinations Explorer (`/destinations`)**:
   - Global destination guides with weather, best travel season, and links to tours.

5. **About Us (`/about`)**:
   - Agency story, team specialist profiles, awards, and partner airlines & luxury hotel chains.

6. **Contact Concierge (`/contact`)**:
   - Working contact inquiry form (saves directly to database).
   - Direct WhatsApp click-to-chat button.
   - Global office addresses (Lahore, Dubai, London).
   - Interactive FAQ accordion.

7. **Booking Flow & Confirmation (`/booking` & `/booking-confirmation/{ref}`)**:
   - Lead passenger form, trip customization, and payment selection.
   - **Printable Official Travel Voucher** with unique Booking Reference ID (`WL-XXXXX`).

8. **My Bookings (`/my-bookings`)**:
   - Customer portal to track reservations by email address or reference ID.

---

### 🛡️ Admin Operations Panel (`/admin`)
- **Credentials**: `admin@wanderluxe.com` / `admin123`
- **Dashboard Overview**: Total Revenue ($), Total Bookings, Active Tours, Customer Inquiries.
- **Tour CRUD Manager**: Add new tour with image, pricing, itinerary; Edit tour; Delete tour; Toggle featured status.
- **Bookings Manager**: Real-time reservations list with 1-click status update (`Confirmed`, `Completed`, `Cancelled`).
- **Inquiries Manager**: View incoming customer messages from Contact Us, mark as contacted/resolved, or delete.
- **Demo Data Seeder**: 1-click button to reload default international tours and demo bookings.

---

## 🗄️ Database: MongoDB & Fallback Engine
- The database layer (`app/database.py`) automatically attempts to connect to **MongoDB** using `MONGODB_URI` from `.env`.
- **If MongoDB is running**: It connects and stores collections (`tours`, `bookings`, `inquiries`, `users`).
- **If MongoDB is not yet running locally**: It activates an automatic persistent JSON document database (`data/wanderluxe_db.json`) with identical query behavior so the site is immediately usable without any setup barriers!
- To use MongoDB Atlas, simply update `MONGODB_URI` in `.env`:
  ```env
  MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
  ```

---

## 🚀 How To Run

1. Open PowerShell / Command Prompt in the project folder:
   ```bash
   cd C:\Users\ahmad\.gemini\antigravity\scratch\wanderluxe-travel
   ```

2. Start the application:
   ```bash
   python run.py
   ```

3. Open your browser:
   - **Website**: [http://localhost:8000](http://localhost:8000)
   - **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)
   - **API Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
