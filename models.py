"""
Database models for Subscription Points Planner MVP.
Includes credit cards, subscriptions, and user relationship models.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from datetime import datetime

Base = declarative_base()


class Client(Base, UserMixin):
    """User account model - extends existing Client with Flask-Login support."""
    __tablename__ = "Client"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    surname = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Email verification fields
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String(6), nullable=True)
    code_expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user_cards = relationship("UserCard", back_populates="client", cascade="all, delete-orphan")
    user_subscriptions = relationship("UserSubscription", back_populates="client", cascade="all, delete-orphan")


class CreditCard(Base):
    """
    Canadian credit cards with rewards information.
    Pre-populated with RBC, BMO, TD, CIBC, Scotiabank cards.
    """
    __tablename__ = "credit_card"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)  # e.g., "RBC Avion Visa Infinite"
    bank = Column(String(100), nullable=False)  # e.g., "RBC"
    annual_fee = Column(Float, default=0.0)
    points_name = Column(String(100))  # e.g., "Avion Points", "BMO Rewards"
    base_earn_rate = Column(Float, default=1.0)  # Points per $1 base spend
    point_value_cents = Column(Float, default=1.0)  # Value per point in cents
    image_url = Column(String(500))  # Card image URL (optional)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    bonus_categories = relationship("CardBonus", back_populates="credit_card", cascade="all, delete-orphan")
    user_cards = relationship("UserCard", back_populates="credit_card")


class SpendingCategory(Base):
    """Spending categories like groceries, gas, dining, travel, etc."""
    __tablename__ = "spending_category"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)  # e.g., "Groceries"
    icon = Column(String(50))  # Bootstrap icon name, e.g., "bi-cart"
    description = Column(String(200))
    
    # Relationships
    card_bonuses = relationship("CardBonus", back_populates="category")


class CardBonus(Base):
    """Bonus points for specific categories on specific cards."""
    __tablename__ = "card_bonus"
    
    id = Column(Integer, primary_key=True)
    credit_card_id = Column(Integer, ForeignKey("credit_card.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("spending_category.id"), nullable=False)
    earn_rate = Column(Float, nullable=False)  # Points per $1 in this category
    
    # Relationships
    credit_card = relationship("CreditCard", back_populates="bonus_categories")
    category = relationship("SpendingCategory", back_populates="card_bonuses")


class Subscription(Base):
    """
    Subscription services like Netflix, Spotify, Twitter Blue, LinkedIn Premium.
    Pre-populated with common services and CAD pricing.
    """
    __tablename__ = "subscription"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # e.g., "Netflix Standard"
    category = Column(String(50))  # e.g., "streaming", "social", "productivity"
    monthly_cost_cad = Column(Float, nullable=False)  # Monthly cost in CAD
    icon = Column(String(50))  # Bootstrap icon or custom class
    color = Column(String(20))  # Brand color for UI
    description = Column(String(200))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user_subscriptions = relationship("UserSubscription", back_populates="subscription")


class UserCard(Base):
    """User's credit cards with their current points balance."""
    __tablename__ = "user_card"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("Client.id"), nullable=False)
    credit_card_id = Column(Integer, ForeignKey("credit_card.id"), nullable=False)
    current_points = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="user_cards")
    credit_card = relationship("CreditCard", back_populates="user_cards")


class UserSubscription(Base):
    """User's subscriptions they want to track/cover with points."""
    __tablename__ = "user_subscription"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("Client.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscription.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    client = relationship("Client", back_populates="user_subscriptions")
    subscription = relationship("Subscription", back_populates="user_subscriptions")
