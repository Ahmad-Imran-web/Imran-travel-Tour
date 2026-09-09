import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print("\n" + "=" * 65)
    print("   WanderLuxe - Luxury Travel Agency & Tour Operator")
    print("=" * 65)
    print(f" * Website URL:       http://localhost:{PORT}")
    print(f" * Tour Packages:     http://localhost:{PORT}/tours")
    print(f" * Destinations:      http://localhost:{PORT}/destinations")
    print(f" * Contact & Inquiry: http://localhost:{PORT}/contact")
    print(f" * Admin Panel:       http://localhost:{PORT}/admin")
    print(" * Admin Credentials: admin@wanderluxe.com  |  admin123")
    print("=" * 65 + "\n")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
