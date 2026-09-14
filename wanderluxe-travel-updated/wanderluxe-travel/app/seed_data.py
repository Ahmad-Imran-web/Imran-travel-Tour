from datetime import datetime
from app.database import get_tours_col, get_bookings_col, get_inquiries_col, get_users_col

SAMPLE_TOURS = [
    {
        "_id": "tour-swiss-01",
        "title": "Swiss Alpine Panorama & Glacier Express",
        "slug": "swiss-alpine-panorama",
        "destination": "Zurich, Zermatt & Interlaken",
        "country": "Switzerland",
        "category": "Luxury",
        "duration_days": 7,
        "duration_nights": 6,
        "price": 2499.0,
        "discount_price": 2199.0,
        "rating": 4.95,
        "reviews_count": 84,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1527668752968-14dc70a27c95?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Experience the majestic Swiss Alps aboard the world-famous Glacier Express. Walk through fairytale villages in Interlaken, gaze upon the Matterhorn in Zermatt, and indulge in luxury 5-star Swiss chalets with private thermal spa baths.",
        "highlights": [
            "First-Class panoramic ride on the Glacier Express",
            "Summit excursion to Jungfraujoch – Top of Europe",
            "Private Matterhorn sunrise view with Swiss chocolate tasting",
            "5-Star Alpine spa resort stay with daily gourmet breakfast"
        ],
        "itinerary": [
            {"day": 1, "title": "Arrival in Zurich & Lake Cruise", "description": "Private VIP limousine transfer to your luxury hotel. Evening private cruise along Lake Zurich with champagne reception."},
            {"day": 2, "title": "Interlaken & Grindelwald First", "description": "Scenic rail journey to Interlaken. Ride the cliff walk cable car at Grindelwald First with breathtaking mountain vistas."},
            {"day": 3, "title": "Jungfraujoch Top of Europe", "description": "Ascend to 3,454m on the historic cogwheel train. Explore Ice Palace and the Sphinx observation terrace."},
            {"day": 4, "title": "The Scenic Glacier Express", "description": "Full-day scenic train journey crossing 291 bridges and 91 tunnels directly to the car-free haven of Zermatt."},
            {"day": 5, "title": "Matterhorn Alpine Paradise", "description": "Cable car ascent to Matterhorn Glacier Paradise. Evening fondue feast with vintage Swiss wines."},
            {"day": 6, "title": "Lucerne & Chapel Bridge", "description": "Travel to picturesque Lucerne. Explore the medieval Chapel Bridge and enjoy a sunset luxury yacht sail."},
            {"day": 7, "title": "Departure Zurich", "description": "Breakfast at hotel and private chauffeur transfer to Zurich International Airport."}
        ],
        "inclusions": [
            "6 Nights in handpicked 5-star Alpine hotels",
            "Swiss Travel Pass 1st Class unlimited train travel",
            "All private transfers & airport limousines",
            "Daily buffet breakfast & 4 three-course dinners",
            "English-speaking licensed mountain concierge",
            "All entry permits, tickets & taxes"
        ],
        "exclusions": [
            "International flights",
            "Personal travel insurance",
            "Optional helicopter excursions"
        ],
        "max_group_size": 12,
        "start_dates": ["2026-05-10", "2026-06-15", "2026-07-20", "2026-09-05"]
    },
    {
        "_id": "tour-bali-02",
        "title": "Bali Tropical Haven, Ubud & Nusa Penida",
        "slug": "bali-tropical-haven",
        "destination": "Ubud, Seminyak & Nusa Penida",
        "country": "Indonesia",
        "category": "Honeymoon",
        "duration_days": 6,
        "duration_nights": 5,
        "price": 1250.0,
        "discount_price": 999.0,
        "rating": 4.92,
        "reviews_count": 112,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Escape to the paradise island of Bali. Rejuvenate in luxurious jungle pool villas in Ubud, discover sacred water temples, swing above rice terraces, and cruise across turquoise waters to Nusa Penida's iconic Kelingking T-Rex cliff.",
        "highlights": [
            "Private infinity pool villa in the heart of Ubud rainforest",
            "Speedboat day tour to Nusa Penida & Kelingking Beach",
            "Romantic floating breakfast & traditional Balinese flower bath",
            "Sunset cocktail dinner at Uluwatu Cliffside Temple"
        ],
        "itinerary": [
            {"day": 1, "title": "Welcome to Denpasar & Ubud Retreat", "description": "Traditional flower garland welcome and private transport to your jungle villa in Ubud."},
            {"day": 2, "title": "Tegallalang Rice Terrace & Sacred Water Temple", "description": "Early morning visit to misty rice fields, giant jungle swing, and purification ritual at Tirta Empul."},
            {"day": 3, "title": "Mount Batur Sunrise Jeep & Hot Springs", "description": "4WD sunrise volcanic jeep tour followed by soaking in natural lakeside geothermal hot springs."},
            {"day": 4, "title": "Nusa Penida Island Adventure", "description": "Private speedboat to Nusa Penida. Visit Kelingking Beach, Broken Beach, and Angel's Billabong."},
            {"day": 5, "title": "Seminyak Beach Club & Uluwatu Sunset", "description": "Transfer to Seminyak beachfront resort. Watch the famous Kecak Fire Dance atop Uluwatu cliffs."},
            {"day": 6, "title": "Souvenir Market & Departure", "description": "Relaxing spa massage before private airport transfer."}
        ],
        "inclusions": [
            "5 Nights in luxury private pool villas & 5-star resorts",
            "Daily floating breakfast & 3 specialty romantic dinners",
            "Private air-conditioned car & dedicated local chauffeur",
            "Speedboat tickets & snorkeling gear at Nusa Penida",
            "2-Hour couple Balinese Aromatherapy spa"
        ],
        "exclusions": [
            "International flight tickets",
            "Personal expenses and tipping"
        ],
        "max_group_size": 10,
        "start_dates": ["2026-04-12", "2026-05-18", "2026-06-22", "2026-08-10"]
    },
    {
        "_id": "tour-dubai-03",
        "title": "Dubai Ultra-Luxury & Royal Desert Safari",
        "slug": "dubai-ultra-luxury",
        "destination": "Downtown Dubai, Palm Jumeirah & Desert",
        "country": "United Arab Emirates",
        "category": "Luxury",
        "duration_days": 5,
        "duration_nights": 4,
        "price": 1850.0,
        "discount_price": 1599.0,
        "rating": 4.88,
        "reviews_count": 96,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1580674684081-7617fbf3d745?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1518684079-3c830dcef090?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Indulge in futuristic glamour and Middle Eastern grandeur. Stay at the world-famous Palm Jumeirah, gaze over the city from Burj Khalifa 148th floor VIP lounge, and venture into the red desert sands in vintage Land Rovers with a 5-star banquet.",
        "highlights": [
            "Burj Khalifa 'At the Top SKY' Level 148 VIP access",
            "Private luxury mega-yacht cruise around Dubai Marina & Palm",
            "Platinum Desert Safari with private bedouin tent & falconry",
            "Helicopter tour over Dubai's iconic coastline"
        ],
        "itinerary": [
            {"day": 1, "title": "Arrival in Dubai & Limousine Escort", "description": "Arrival at DXB Airport with Marhaba VIP fast-track service and transfer to 5-star hotel."},
            {"day": 2, "title": "Modern Dubai, Burj Khalifa & Dubai Mall", "description": "Private guided tour of Downtown, sky lounge access at Burj Khalifa, and evening fountain show."},
            {"day": 3, "title": "Marina Yacht Sail & Palm Jumeirah", "description": "Morning 12-minute helicopter skyline flight, followed by afternoon private yacht cruise with chef dining."},
            {"day": 4, "title": "Royal Heritage Desert Safari", "description": "Dune bashing, camel trekking, sunset falconry demonstration, and Arabic BBQ banquet under the stars."},
            {"day": 5, "title": "Gold Souk & Farewell", "description": "Shopping tour of traditional Deira Gold & Spice Souks before return flight."}
        ],
        "inclusions": [
            "4 Nights in 5-star luxury hotel on Palm Jumeirah",
            "Private luxury SUV transfers throughout",
            "Burj Khalifa 148th floor VIP lounge tickets",
            "Royal Desert Safari with 5-star dinner",
            "Private yacht charter & BBQ lunch"
        ],
        "exclusions": ["UAE tourist visa", "Personal shopping purchases"],
        "max_group_size": 8,
        "start_dates": ["2026-04-05", "2026-05-01", "2026-10-15", "2026-11-20"]
    },
    {
        "_id": "tour-hunza-04",
        "title": "Hunza & Skardu Majestic Northern Wonders",
        "slug": "hunza-skardu-wonders",
        "destination": "Hunza, Attabad Lake & Skardu Valley",
        "country": "Pakistan",
        "category": "Adventure",
        "duration_days": 8,
        "duration_nights": 7,
        "price": 950.0,
        "discount_price": 799.0,
        "rating": 4.98,
        "reviews_count": 140,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1627894483216-2138af692e32?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Journey into the crown of the Karakoram. Marvel at 8,000-meter snowy peaks (Rakaposhi, K2 view points), the crystal turquoise waters of Attabad Lake, ancient 1,000-year-old Baltit & Altit Forts, and the magical cold desert of Sarfaranga.",
        "highlights": [
            "Jet boat safari & luxury glamping on turquoise Attabad Lake",
            "Visit the 900-year-old Baltit & Altit Forts in Karimabad",
            "Eagle's Nest sunset viewpoint overlooking 7 legendary peaks",
            "Stargazing and ATV rides across Sarfaranga Cold Desert"
        ],
        "itinerary": [
            {"day": 1, "title": "Islamabad to Gilgit / Chilas", "description": "Scenic drive along the Karakoram Highway or direct flight to Gilgit with views of Nanga Parbat."},
            {"day": 2, "title": "Arrival in Hunza & Rakaposhi View", "description": "Stop at the breathtaking Rakaposhi Viewpoint. Check into Serena Hunza with balcony view of Ladyfinger Peak."},
            {"day": 3, "title": "Altit & Baltit Forts & Eagle's Nest", "description": "Explore historical Silk Road forts and watch the golden hour sunset over the Hunza valley."},
            {"day": 4, "title": "Attabad Lake & Passu Cones", "description": "Speedboat ride on Attabad Lake, walk the Passu suspension bridge, and view the jagged Passu Cathedral."},
            {"day": 5, "title": "Khunjerab Pass (Pak-China Border)", "description": "Ascend to the highest paved international border crossing at 4,693 meters."},
            {"day": 6, "title": "Journey to Skardu & Shangrila Lake", "description": "Travel through the dramatic Indus River gorge to Shangrila Lower Kachura Lake."},
            {"day": 7, "title": "Sarfaranga Cold Desert & Shigar Fort", "description": "Experience sand dunes surrounded by snowy mountains. Tour the Serena Shigar Heritage Fort."},
            {"day": 8, "title": "Flight back to Islamabad", "description": "Scenic mountain flight back to Islamabad international airport."}
        ],
        "inclusions": [
            "7 Nights in luxury Serena hotels & deluxe valley resorts",
            "Dedicated 4x4 Prado with fuel & professional mountain driver",
            "Breakfast, lunches, and traditional dinners included",
            "All entry passes, fort tickets, and boat tour charges",
            "Professional local tour guide & photography assistance"
        ],
        "exclusions": ["Domestic flights", "Tips and personal souvenirs"],
        "max_group_size": 14,
        "start_dates": ["2026-05-01", "2026-06-10", "2026-07-15", "2026-09-01"]
    },
    {
        "_id": "tour-japan-05",
        "title": "Tokyo, Kyoto & Mount Fuji Heritage Trail",
        "slug": "japan-heritage-trail",
        "destination": "Tokyo, Hakone, Kyoto & Osaka",
        "country": "Japan",
        "category": "Cultural",
        "duration_days": 9,
        "duration_nights": 8,
        "price": 2850.0,
        "discount_price": 2499.0,
        "rating": 4.96,
        "reviews_count": 68,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Immerse yourself in the timeless harmony of ancient tradition and hyper-modern innovation. Ride the Shinkansen Bullet Train, walk through Kyoto's 10,000 vermilion Torii gates, relax in Hakone onsens gazing at Mt. Fuji, and savor Michelin-star dining.",
        "highlights": [
            "Ride the iconic Shinkansen Bullet Train at 300 km/h",
            "Hakone hot spring Ryokan with private onsen & Mt. Fuji view",
            "Fushimi Inari Shrine & Arashiyama Bamboo Grove at sunrise",
            "Exclusive tea ceremony with an apprentice Geisha (Maiko) in Gion"
        ],
        "itinerary": [
            {"day": 1, "title": "Arrival in Tokyo & Shinjuku Neon", "description": "Arrival at Haneda/Narita. Evening walk through Shinjuku's glowing skyscraper alleys."},
            {"day": 2, "title": "Old & New Tokyo", "description": "Asakusa Senso-ji Temple, Meiji Shrine, Shibuya Crossing, and digital art museum TeamLab Planets."},
            {"day": 3, "title": "Mount Fuji & Hakone Onsen", "description": "Lake Ashi cruise with Mt. Fuji reflection. Check into traditional Japanese Ryokan with Kaiseki banquet."},
            {"day": 4, "title": "Bullet Train to Ancient Kyoto", "description": "Board the Shinkansen. Afternoon walking tour of historic Gion and Yasaka Shrine."},
            {"day": 5, "title": "Kyoto's Golden Pavilion & Bamboo Grove", "description": "Kinkaku-ji (Golden Temple) and serene rickshaw tour through Arashiyama bamboo forest."},
            {"day": 6, "title": "Nara Deer Park & Todai-ji", "description": "Feed the sacred bowing sika deer in Nara Park and marvel at the Great Bronze Buddha."},
            {"day": 7, "title": "Osaka Gastronomy & Castle", "description": "Explore Osaka Castle and sample street food delicacies in bustling Dotonbori."},
            {"day": 8, "title": "Kyoto Free Leisure & Souvenirs", "description": "Free day to explore Nishiki market, artisan crafts, and zen rock gardens."},
            {"day": 9, "title": "Departure via Kansai International", "description": "Private transfer to Osaka Kansai Airport."}
        ],
        "inclusions": [
            "8 Nights in boutique 4 & 5-star hotels + 1 night traditional Ryokan",
            "7-Day Japan Rail Pass Ordinary Class",
            "All guided excursions and entrance tickets",
            "Daily breakfast and multi-course Kaiseki dinner",
            "Pocket Wi-Fi device throughout Japan"
        ],
        "exclusions": ["International flights", "Personal shopping expenses"],
        "max_group_size": 12,
        "start_dates": ["2026-04-10", "2026-05-15", "2026-10-01", "2026-11-10"]
    },
    {
        "_id": "tour-maldives-06",
        "title": "Maldives Overwater Luxury Villa & Reef Diving",
        "slug": "maldives-overwater-luxury",
        "destination": "North Malé Atoll",
        "country": "Maldives",
        "category": "Honeymoon",
        "duration_days": 5,
        "duration_nights": 4,
        "price": 3200.0,
        "discount_price": 2799.0,
        "rating": 4.99,
        "reviews_count": 135,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Pure bliss awaits in the pristine turquoise lagoons of the Indian Ocean. Step directly into crystal waters from your private overwater pool villa, swim with majestic manta rays, and enjoy a candlelit dining experience under the starry constellations.",
        "highlights": [
            "Overwater bungalow with glass floor panels & private pool",
            "Scenic Seaplane return transfer over turquoise atolls",
            "Guided nurse shark and coral reef snorkeling safari",
            "Romantic private sandbank picnic with butler service"
        ],
        "itinerary": [
            {"day": 1, "title": "Seaplane Arrival & Overwater Check-in", "description": "Seaplane transfer to luxury island resort. Bottle of champagne on arrival."},
            {"day": 2, "title": "Lagoon Snorkeling & Coral Garden", "description": "Explore vibrant house reefs with marine biologist guide. Afternoon cocktail tasting."},
            {"day": 3, "title": "Dolphin Cruise & Private Sandbank Picnic", "description": "Sunset cruise alongside wild spinner dolphins, followed by private island dining."},
            {"day": 4, "title": "Overwater Spa Treatment & Starlit Cinema", "description": "60-minute revitalizing couples massage over the lagoon waves and outdoor beach cinema."},
            {"day": 5, "title": "Farewell Paradise", "description": "Morning yoga on the pier and seaplane transfer back to Malé International Airport."}
        ],
        "inclusions": [
            "4 Nights in luxury 5-star Overwater Pool Villa",
            "All-Inclusive premium meals & international beverage package",
            "Roundtrip scenic seaplane transfers",
            "Complimentary non-motorized watersports",
            "Couples signature wellness spa treatment"
        ],
        "exclusions": ["International airfare", "Motorized watersports like jet skis"],
        "max_group_size": 6,
        "start_dates": ["2026-04-20", "2026-05-25", "2026-09-15", "2026-11-01"]
    },
    {
        "_id": "tour-turkey-07",
        "title": "Cappadocia Balloon Flight & Istanbul Heritage",
        "slug": "cappadocia-istanbul-heritage",
        "destination": "Istanbul & Cappadocia",
        "country": "Turkey",
        "category": "Cultural",
        "duration_days": 7,
        "duration_nights": 6,
        "price": 1650.0,
        "discount_price": 1399.0,
        "rating": 4.91,
        "reviews_count": 89,
        "featured": True,
        "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Uncover the crossroads of continents where East meets West. Drift in a hot air balloon over Cappadocia's mystical fairy chimneys, stay in an authentic carved cave suite, cruise the Bosphorus Strait, and discover the Hagia Sophia and Grand Bazaar.",
        "highlights": [
            "Sunrise Hot Air Balloon flight over Goreme Valley",
            "Luxury carved cave hotel suite with panoramic terrace",
            "Private Bosphorus sunset yacht cruise between Europe & Asia",
            "VIP guided tour of Hagia Sophia, Blue Mosque & Topkapi Palace"
        ],
        "itinerary": [
            {"day": 1, "title": "Istanbul Arrival & Sultanahmet", "description": "Airport transfer to boutique hotel in historic Sultanahmet. Evening Turkish tea tasting."},
            {"day": 2, "title": "Byzantine & Ottoman Marvels", "description": "Full-day tour of Hagia Sophia, Blue Mosque, Basilica Cistern, and Hippodrome."},
            {"day": 3, "title": "Grand Bazaar & Bosphorus Sunset Yacht", "description": "Explore spice stalls of Grand Bazaar and enjoy 2-hour private yacht cruise on Bosphorus."},
            {"day": 4, "title": "Flight to Cappadocia & Underground City", "description": "Domestic flight to Cappadocia. Explore Kaymakli subterranean city and cave churches."},
            {"day": 5, "title": "Sunrise Balloon Flight & Devrent Valley", "description": "Magical dawn balloon ride, champagne toast, and hiking through Love Valley rock formations."},
            {"day": 6, "title": "Pottery Workshop & Turkish Night Show", "description": "Traditional ceramic art in Avanos and evening whirling dervish and folklore performance."},
            {"day": 7, "title": "Return Flight to Istanbul & Departure", "description": "Morning breakfast overlooking fairy chimneys and return flight to Istanbul."}
        ],
        "inclusions": [
            "6 Nights in premium boutique & luxury cave hotels",
            "Domestic flights (Istanbul - Cappadocia - Istanbul)",
            "Hot Air Balloon flight with flight certificate & champagne",
            "All museum entrance fees & licensed English guide",
            "Daily Turkish breakfast and 3 dinners"
        ],
        "exclusions": ["International airfare", "Personal drinks and souvenirs"],
        "max_group_size": 14,
        "start_dates": ["2026-05-12", "2026-06-20", "2026-09-10", "2026-10-15"]
    },
    {
        "_id": "tour-safari-08",
        "title": "Serengeti Great Migration Safari & Zanzibar",
        "slug": "serengeti-safari-zanzibar",
        "destination": "Serengeti, Ngorongoro & Zanzibar",
        "country": "Tanzania",
        "category": "Adventure",
        "duration_days": 8,
        "duration_nights": 7,
        "price": 3100.0,
        "discount_price": 2650.0,
        "rating": 4.97,
        "reviews_count": 52,
        "featured": False,
        "image_url": "https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=80",
        "gallery": [
            "https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?auto=format&fit=crop&w=800&q=80"
        ],
        "description": "Witness nature's greatest spectacle. Track the Big Five lions, leopards, elephants, rhinos, and buffaloes in the endless plains of the Serengeti and inside the Ngorongoro Crater, before unwinding on the white-sand coral beaches of spice island Zanzibar.",
        "highlights": [
            "Exclusive Big Five game drives in custom pop-up roof 4x4 Land Cruisers",
            "Ngorongoro Crater floor safari with picnic by hippo pool",
            "Luxury tented camp experience under the African wilderness sky",
            "White-sand tropical beach relaxation at Zanzibar luxury resort"
        ],
        "itinerary": [
            {"day": 1, "title": "Kilimanjaro to Arusha", "description": "Arrival at JRO Airport and transfer to peaceful coffee plantation lodge in Arusha."},
            {"day": 2, "title": "Lake Manyara National Park", "description": "Game drive spotting tree-climbing lions and flocks of pink flamingos."},
            {"day": 3, "title": "Serengeti National Park Plains", "description": "Enter the legendary Serengeti. Afternoon safari tracking cheetahs and lion prides."},
            {"day": 4, "title": "Full Day Great Migration Tracking", "description": "All-day adventure following wildebeest herds and predator action with bush lunch."},
            {"day": 5, "title": "Ngorongoro Crater Basin", "description": "Descend 600m into the volcanic caldera for rare black rhino tracking."},
            {"day": 6, "title": "Flight to Zanzibar Spice Island", "description": "Bush flight to Zanzibar. Check into 5-star beachfront ocean retreat in Nungwi."},
            {"day": 7, "title": "Stone Town & Prison Island Giant Tortoises", "description": "Explore historic Stone Town alleys and feed giant Aldabra tortoises."},
            {"day": 8, "title": "Zanzibar Departure", "description": "Final morning dip in the turquoise Indian Ocean before airport transfer."}
        ],
        "inclusions": [
            "7 Nights luxury lodges, tented camps, and beachfront resort",
            "Private 4x4 safari vehicle with binoculars and expert tracker",
            "All national park conservation & crater service fees",
            "Domestic flight from Serengeti/Arusha to Zanzibar",
            "All meals on safari (Full Board) and breakfast in Zanzibar"
        ],
        "exclusions": ["International flights", "Tanzania tourist visa ($50-$100)"],
        "max_group_size": 8,
        "start_dates": ["2026-06-05", "2026-07-10", "2026-08-15", "2026-09-20"]
    }
]

SAMPLE_BOOKINGS = []
SAMPLE_INQUIRIES = []

def seed_database():
    tours_col = get_tours_col()

    # Seed tours if empty
    if tours_col.count_documents() == 0:
        for t in SAMPLE_TOURS:
            tours_col.insert_one(t)
        print("[OK] Tour packages initialized successfully.")

if __name__ == "__main__":
    seed_database()
