"""
Seed data for Subscription Points Planner.
Run this script to populate the database with Canadian credit cards and common subscriptions.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CreditCard, SpendingCategory, CardBonus, Subscription

# Database setup
engine = create_engine("sqlite:///clients.db", echo=False)
Session = sessionmaker(bind=engine)


def create_tables():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully!")


def seed_spending_categories():
    """Seed spending categories."""
    categories = [
        {"name": "Groceries", "icon": "bi-cart", "description": "Supermarkets and grocery stores"},
        {"name": "Gas", "icon": "bi-fuel-pump", "description": "Gas stations and fuel"},
        {"name": "Dining", "icon": "bi-cup-hot", "description": "Restaurants and food delivery"},
        {"name": "Travel", "icon": "bi-airplane", "description": "Airlines, hotels, car rentals"},
        {"name": "Transit", "icon": "bi-bus-front", "description": "Public transit and rideshare"},
        {"name": "Recurring Bills", "icon": "bi-receipt", "description": "Subscriptions, utilities, phone"},
        {"name": "Drug Stores", "icon": "bi-capsule", "description": "Pharmacies and drug stores"},
        {"name": "Entertainment", "icon": "bi-film", "description": "Movies, concerts, events"},
        {"name": "Online Shopping", "icon": "bi-bag", "description": "E-commerce purchases"},
        {"name": "Other", "icon": "bi-three-dots", "description": "All other purchases"},
    ]
    
    session = Session()
    try:
        for cat_data in categories:
            existing = session.query(SpendingCategory).filter_by(name=cat_data["name"]).first()
            if not existing:
                session.add(SpendingCategory(**cat_data))
        session.commit()
        print(f"✅ Seeded {len(categories)} spending categories!")
    finally:
        session.close()


def seed_credit_cards():
    """Seed Canadian credit cards with their reward structures."""
    cards = [
        # RBC Cards
        {
            "name": "RBC Avion Visa Infinite",
            "bank": "RBC",
            "annual_fee": 120.0,
            "points_name": "Avion Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        {
            "name": "RBC Cash Back Mastercard",
            "bank": "RBC",
            "annual_fee": 0.0,
            "points_name": "Cash Back",
            "base_earn_rate": 0.5,  # 0.5% on everything
            "point_value_cents": 1.0,
        },
        {
            "name": "RBC ION Visa",
            "bank": "RBC",
            "annual_fee": 0.0,
            "points_name": "Avion Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0, # Avion points are worth 1 cent usually
        },
        {
            "name": "RBC ION+ Visa",
            "bank": "RBC",
            "annual_fee": 48.0, # $4/month
            "points_name": "Avion Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        # BMO Cards
        {
            "name": "BMO CashBack World Elite Mastercard",
            "bank": "BMO",
            "annual_fee": 120.0,
            "points_name": "Cash Back",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        {
            "name": "BMO Rewards Mastercard",
            "bank": "BMO",
            "annual_fee": 0.0,
            "points_name": "BMO Rewards",
            "base_earn_rate": 1.0,
            "point_value_cents": 0.7,
        },
        {
            "name": "BMO eclipse Visa Infinite",
            "bank": "BMO",
            "annual_fee": 99.0,
            "points_name": "BMO Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        # TD Cards
        {
            "name": "TD Cash Back Visa Infinite",
            "bank": "TD",
            "annual_fee": 89.0,
            "points_name": "Cash Back",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        {
            "name": "TD Aeroplan Visa Infinite",
            "bank": "TD",
            "annual_fee": 139.0,
            "points_name": "Aeroplan Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.5,
        },
        {
            "name": "TD First Class Travel Visa Infinite",
            "bank": "TD",
            "annual_fee": 89.0,
            "points_name": "TD Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 0.8,
        },
        # CIBC Cards
        {
            "name": "CIBC Aeroplan Visa Infinite",
            "bank": "CIBC",
            "annual_fee": 139.0,
            "points_name": "Aeroplan Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.5,
        },
        {
            "name": "CIBC Dividend Visa Infinite",
            "bank": "CIBC",
            "annual_fee": 99.0,
            "points_name": "Cash Back",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        {
            "name": "CIBC Costco Mastercard",
            "bank": "CIBC",
            "annual_fee": 0.0,
            "points_name": "Cash Back",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        # Scotiabank Cards
        {
            "name": "Scotiabank Gold American Express",
            "bank": "Scotiabank",
            "annual_fee": 120.0,
            "points_name": "Scene+ Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        {
            "name": "Scotia Momentum Visa Infinite",
            "bank": "Scotiabank",
            "annual_fee": 120.0,
            "points_name": "Cash Back",
            "base_earn_rate": 1.0,
            "point_value_cents": 1.0,
        },
        {
            "name": "Scotiabank Scene+ Visa",
            "bank": "Scotiabank",
            "annual_fee": 0.0,
            "points_name": "Scene+ Points",
            "base_earn_rate": 1.0,
            "point_value_cents": 0.8,
        },
    ]
    
    session = Session()
    try:
        for card_data in cards:
            existing = session.query(CreditCard).filter_by(name=card_data["name"]).first()
            if not existing:
                session.add(CreditCard(**card_data))
                print(f"Added new card: {card_data['name']}")
            else:
                # Update existing card details
                updated = False
                for key, value in card_data.items():
                    if getattr(existing, key) != value:
                        setattr(existing, key, value)
                        updated = True
                if updated:
                    print(f"Updated card: {card_data['name']}")
                    
        session.commit()
        print(f"✅ Processed {len(cards)} credit cards!")
    finally:
        session.close()


def seed_card_bonuses():
    """Seed bonus categories for credit cards."""
    # Define bonus rates: (card_name, category_name, earn_rate)
    bonuses = [
        # RBC Avion - 1.25x on travel
        ("RBC Avion Visa Infinite", "Travel", 1.25),
        ("RBC Avion Visa Infinite", "Dining", 1.25),
        
        # RBC Cash Back - 2% groceries
        ("RBC Cash Back Mastercard", "Groceries", 2.0),
        
        # RBC ION Visa - 1.5x on Groceries, Gas, Transit, Streaming (Recuring Bills)
        ("RBC ION Visa", "Groceries", 1.5),
        ("RBC ION Visa", "Gas", 1.5),
        ("RBC ION Visa", "Transit", 1.5),
        ("RBC ION Visa", "Recurring Bills", 1.5), 

        # RBC ION+ Visa - 3x on Groceries, Dining, Gas, Transit, Streaming
        ("RBC ION+ Visa", "Groceries", 3.0),
        ("RBC ION+ Visa", "Dining", 3.0),
        ("RBC ION+ Visa", "Gas", 3.0),
        ("RBC ION+ Visa", "Transit", 3.0),
        ("RBC ION+ Visa", "Recurring Bills", 3.0),
        
    # BMO CashBack World Elite
        ("BMO CashBack World Elite Mastercard", "Groceries", 5.0),
        ("BMO CashBack World Elite Mastercard", "Transit", 4.0),
        ("BMO CashBack World Elite Mastercard", "Gas", 3.0),
        ("BMO CashBack World Elite Mastercard", "Recurring Bills", 2.0),
        
        # BMO eclipse Visa Infinite
        ("BMO eclipse Visa Infinite", "Dining", 5.0),
        ("BMO eclipse Visa Infinite", "Groceries", 5.0),
        ("BMO eclipse Visa Infinite", "Gas", 5.0),
        ("BMO eclipse Visa Infinite", "Transit", 5.0),
        
        # TD Cash Back
        ("TD Cash Back Visa Infinite", "Groceries", 3.0),
        ("TD Cash Back Visa Infinite", "Recurring Bills", 3.0),
        ("TD Cash Back Visa Infinite", "Gas", 3.0),
        
        # TD Aeroplan
        ("TD Aeroplan Visa Infinite", "Travel", 1.5),
        ("TD Aeroplan Visa Infinite", "Gas", 1.5),
        ("TD Aeroplan Visa Infinite", "Groceries", 1.5),
        
        # TD First Class Travel
        ("TD First Class Travel Visa Infinite", "Travel", 8.0), # Expedia for TD
        ("TD First Class Travel Visa Infinite", "Groceries", 6.0),
        ("TD First Class Travel Visa Infinite", "Dining", 6.0),
        ("TD First Class Travel Visa Infinite", "Recurring Bills", 4.0),

        # CIBC Dividend
        ("CIBC Dividend Visa Infinite", "Groceries", 4.0),
        ("CIBC Dividend Visa Infinite", "Gas", 4.0),
        ("CIBC Dividend Visa Infinite", "Dining", 2.0),
        ("CIBC Dividend Visa Infinite", "Transit", 2.0),
        ("CIBC Dividend Visa Infinite", "Recurring Bills", 2.0),
        
        # CIBC Costco
        ("CIBC Costco Mastercard", "Gas", 3.0),
        ("CIBC Costco Mastercard", "Dining", 3.0),
        
        # Scotiabank Gold Amex
        ("Scotiabank Gold American Express", "Groceries", 5.0), # 6x at Sobeys/etc, 5x other groceries/dining
        ("Scotiabank Gold American Express", "Dining", 5.0),
        ("Scotiabank Gold American Express", "Entertainment", 3.0),
        ("Scotiabank Gold American Express", "Gas", 3.0),
        ("Scotiabank Gold American Express", "Transit", 3.0),
        ("Scotiabank Gold American Express", "Recurring Bills", 3.0), # Includes streaming services 
        
        # Scotia Momentum
        ("Scotia Momentum Visa Infinite", "Groceries", 4.0),
        ("Scotia Momentum Visa Infinite", "Recurring Bills", 4.0),
        ("Scotia Momentum Visa Infinite", "Drug Stores", 4.0),
        ("Scotia Momentum Visa Infinite", "Gas", 2.0),
        ("Scotia Momentum Visa Infinite", "Transit", 2.0),
    ]
    
    session = Session()
    try:
        count = 0
        for card_name, category_name, earn_rate in bonuses:
            card = session.query(CreditCard).filter_by(name=card_name).first()
            category = session.query(SpendingCategory).filter_by(name=category_name).first()
            
            if card and category:
                existing = session.query(CardBonus).filter_by(
                    credit_card_id=card.id, 
                    category_id=category.id
                ).first()
                
                if not existing:
                    session.add(CardBonus(
                        credit_card_id=card.id,
                        category_id=category.id,
                        earn_rate=earn_rate
                    ))
                    count += 1
                else:
                    if existing.earn_rate != earn_rate:
                        existing.earn_rate = earn_rate
                        count += 1
                        
        session.commit()
        print(f"✅ Processed/Updated {len(bonuses)} card bonus categories!")
    finally:
        session.close()


def seed_subscriptions():
    """Seed common subscription services with CAD pricing."""
    subscriptions = [
        # AI & Productivity
        {"name": "ChatGPT Plus", "category": "productivity", "monthly_cost_cad": 28.00, 
         "icon": "bi-robot", "color": "#10A37F", "description": "GPT-4, DALL-E, Analysis"},
        {"name": "Claude Pro", "category": "productivity", "monthly_cost_cad": 28.00, 
         "icon": "bi-stars", "color": "#D97757", "description": "Claude 3 Opus, 5x usage"},
         
        # Streaming
        {"name": "Netflix Standard", "category": "streaming", "monthly_cost_cad": 16.49, 
         "icon": "bi-play-circle", "color": "#E50914", "description": "1080p streaming, 2 screens"},
        {"name": "Netflix Premium", "category": "streaming", "monthly_cost_cad": 20.99, 
         "icon": "bi-play-circle", "color": "#E50914", "description": "4K streaming, 4 screens"},
        {"name": "Spotify Premium", "category": "streaming", "monthly_cost_cad": 11.99, 
         "icon": "bi-spotify", "color": "#1DB954", "description": "Ad-free music streaming"},
        {"name": "Spotify Duo", "category": "streaming", "monthly_cost_cad": 16.99, 
         "icon": "bi-spotify", "color": "#1DB954", "description": "2 Premium accounts"},
        {"name": "Disney+", "category": "streaming", "monthly_cost_cad": 11.99, 
         "icon": "bi-play-btn", "color": "#113CCF", "description": "Disney, Marvel, Star Wars"},
        {"name": "Amazon Prime", "category": "streaming", "monthly_cost_cad": 9.99, 
         "icon": "bi-box", "color": "#FF9900", "description": "Prime Video + shipping"},
        {"name": "Apple Music", "category": "streaming", "monthly_cost_cad": 10.99, 
         "icon": "bi-music-note-beamed", "color": "#FC3C44", "description": "Apple's music service"},
        {"name": "YouTube Premium", "category": "streaming", "monthly_cost_cad": 13.99, 
         "icon": "bi-youtube", "color": "#FF0000", "description": "Ad-free YouTube + Music"},
        {"name": "Crave", "category": "streaming", "monthly_cost_cad": 19.99, 
         "icon": "bi-tv", "color": "#2B2B2B", "description": "HBO, Showtime content"},
         
        # Social Media Premium
        {"name": "Twitter/X Premium", "category": "social", "monthly_cost_cad": 11.00, 
         "icon": "bi-twitter-x", "color": "#000000", "description": "Blue checkmark, less ads"},
        {"name": "Twitter/X Premium+", "category": "social", "monthly_cost_cad": 22.00, 
         "icon": "bi-twitter-x", "color": "#000000", "description": "No ads, max features"},
        {"name": "LinkedIn Premium Career", "category": "social", "monthly_cost_cad": 39.99, 
         "icon": "bi-linkedin", "color": "#0A66C2", "description": "InMail, who viewed profile"},
        {"name": "LinkedIn Premium Business", "category": "social", "monthly_cost_cad": 79.99, 
         "icon": "bi-linkedin", "color": "#0A66C2", "description": "Unlimited search, 15 InMail"},
        
        # Productivity
        {"name": "Microsoft 365 Personal", "category": "productivity", "monthly_cost_cad": 9.99, 
         "icon": "bi-microsoft", "color": "#0078D4", "description": "Office apps, 1TB OneDrive"},
        {"name": "iCloud+ 50GB", "category": "productivity", "monthly_cost_cad": 1.29, 
         "icon": "bi-cloud", "color": "#3478F6", "description": "Apple cloud storage"},
        {"name": "iCloud+ 200GB", "category": "productivity", "monthly_cost_cad": 3.99, 
         "icon": "bi-cloud", "color": "#3478F6", "description": "Apple cloud storage"},
        {"name": "Google One 100GB", "category": "productivity", "monthly_cost_cad": 2.79, 
         "icon": "bi-google", "color": "#4285F4", "description": "Google storage + VPN"},
    ]
    
    session = Session()
    try:
        for sub_data in subscriptions:
            existing = session.query(Subscription).filter_by(name=sub_data["name"]).first()
            if not existing:
                session.add(Subscription(**sub_data))
        session.commit()
        print(f"✅ Seeded {len(subscriptions)} subscriptions!")
    finally:
        session.close()


def run_all_seeds():
    """Run all seed functions."""
    print("\n🌱 Starting database seeding...\n")
    create_tables()
    seed_spending_categories()
    seed_credit_cards()
    seed_card_bonuses()
    seed_subscriptions()
    print("\n✅ All seeding complete!\n")


if __name__ == "__main__":
    run_all_seeds()
