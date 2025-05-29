from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from database import get_db, User, UserInteraction

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserPreferences(BaseModel):
    categories: List[str]
    budget_range: Dict[str, float]
    shopping_style: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    preferences: Optional[Dict[str, Any]]
    created_at: Any

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user (password hashing would be added in production)
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=user.password,  # Should be hashed
        preferences={}
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.put("/{user_id}/preferences")
async def update_preferences(user_id: int, preferences: UserPreferences, db: Session = Depends(get_db)):
    """Update user preferences for personalized recommendations"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.preferences = preferences.dict()
    db.commit()
    
    return {"message": "Preferences updated successfully"}

@router.get("/{user_id}/categories")
async def get_recommended_categories():
    """Get recommended categories for first-time users"""
    categories = [
        {"id": "electronics", "name": "Electronics", "icon": "smartphone"},
        {"id": "home", "name": "Home & Garden", "icon": "home"},
        {"id": "fashion", "name": "Fashion", "icon": "shirt"},
        {"id": "sports", "name": "Sports & Outdoors", "icon": "dumbbell"},
        {"id": "books", "name": "Books", "icon": "book"},
        {"id": "health", "name": "Health & Beauty", "icon": "heart"},
        {"id": "automotive", "name": "Automotive", "icon": "car"},
        {"id": "toys", "name": "Toys & Games", "icon": "gamepad"}
    ]
    
    return {"categories": categories}

@router.post("/{user_id}/interaction")
async def track_interaction(user_id: int, interaction_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Track user interactions for analytics and recommendations"""
    interaction = UserInteraction(
        user_id=user_id,
        interaction_type=interaction_data.get("type"),
        product_id=interaction_data.get("product_id"),
        search_query=interaction_data.get("search_query"),
        interaction_data=interaction_data
    )
    
    db.add(interaction)
    db.commit()
    
    return {"message": "Interaction tracked"} 