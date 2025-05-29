from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from database import get_db, User, SearchHistory, UserInteraction, Product
from llm_service import llm_service

router = APIRouter()

@router.get("/user/{user_id}")
async def get_user_recommendations(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """Get personalized recommendations for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's search history
    search_history = db.query(SearchHistory).filter(
        SearchHistory.user_id == user_id
    ).order_by(SearchHistory.created_at.desc()).limit(10).all()
    
    search_queries = [search.query for search in search_history]
    
    # Generate recommendations using LLM
    recommendations = await llm_service.generate_recommendations(
        user.preferences or {}, 
        search_queries
    )
    
    return {
        "user_id": user_id,
        "recommendations": recommendations[:limit]
    }

@router.get("/trending")
async def get_trending_products(category: Optional[str] = None, limit: int = 20, db: Session = Depends(get_db)):
    """Get trending products based on user interactions"""
    
    # Mock trending products (in production, this would analyze actual interaction data)
    trending = [
        {
            "product_name": "iPhone 15 Pro",
            "category": "electronics",
            "estimated_price": 999.99,
            "trending_score": 0.95,
            "reason": "High search volume and user engagement"
        },
        {
            "product_name": "AirPods Pro 3",
            "category": "electronics", 
            "estimated_price": 249.99,
            "trending_score": 0.87,
            "reason": "Frequently viewed with phones"
        },
        {
            "product_name": "Nike Air Max",
            "category": "fashion",
            "estimated_price": 129.99,
            "trending_score": 0.82,
            "reason": "Popular in sports category"
        }
    ]
    
    if category:
        trending = [item for item in trending if item["category"] == category]
    
    return {"trending": trending[:limit]}

@router.get("/deals")
async def get_current_deals(category: Optional[str] = None, limit: int = 15, db: Session = Depends(get_db)):
    """Get current deals and discounts"""
    
    # Mock deals (in production, this would query real deal data)
    deals = [
        {
            "product_name": "Samsung Galaxy S24",
            "original_price": 899.99,
            "sale_price": 699.99,
            "discount_percent": 22,
            "source": "Best Buy",
            "expires_at": "2024-02-28",
            "category": "electronics"
        },
        {
            "product_name": "MacBook Air M3",
            "original_price": 1199.99,
            "sale_price": 999.99,
            "discount_percent": 17,
            "source": "Apple Store",
            "expires_at": "2024-03-01",
            "category": "electronics"
        },
        {
            "product_name": "Dyson V15 Vacuum",
            "original_price": 649.99,
            "sale_price": 449.99,
            "discount_percent": 31,
            "source": "Amazon",
            "expires_at": "2024-02-25",
            "category": "home"
        }
    ]
    
    if category:
        deals = [deal for deal in deals if deal["category"] == category]
    
    return {"deals": deals[:limit]}

@router.post("/user/{user_id}/similar")
async def get_similar_products(user_id: int, product_info: Dict[str, Any], db: Session = Depends(get_db)):
    """Get products similar to user's interests"""
    
    # Use LLM to find similar products
    messages = [
        {
            "role": "system",
            "content": """Find similar products based on the given product information. 
            Return a JSON array of similar products with estimated prices and reasons for similarity."""
        },
        {
            "role": "user", 
            "content": f"Find products similar to: {product_info}"
        }
    ]
    
    response = await llm_service.call_llm(messages)
    
    try:
        import json
        similar_products = json.loads(response)
        return {"similar_products": similar_products}
    except:
        return {"similar_products": [], "message": "Could not generate similar products"}

@router.get("/categories/{category}/popular")
async def get_popular_in_category(category: str, limit: int = 10, db: Session = Depends(get_db)):
    """Get popular products in a specific category"""
    
    # Get products from database in this category
    products = db.query(Product).filter(
        Product.category == category
    ).order_by(Product.ratings.desc()).limit(limit).all()
    
    return [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "currency": product.currency,
            "ratings": product.ratings,
            "reviews_count": product.reviews_count,
            "image_url": product.image_url,
            "source_url": product.source_url
        }
        for product in products
    ] 