from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db, Product, PriceHistory
from llm_service import llm_service

router = APIRouter()

@router.get("/{product_id}")
async def get_product_details(product_id: int, db: Session = Depends(get_db)):
    """Get detailed product information"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get price history
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.recorded_at.desc()).limit(30).all()
    
    return {
        "product": {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "category": product.category,
            "brand": product.brand,
            "price": product.price,
            "currency": product.currency,
            "source_url": product.source_url,
            "image_url": product.image_url,
            "characteristics": product.characteristics,
            "ratings": product.ratings,
            "reviews_count": product.reviews_count,
            "availability": product.availability
        },
        "price_history": [
            {
                "price": ph.price,
                "currency": ph.currency,
                "source": ph.source,
                "recorded_at": ph.recorded_at
            }
            for ph in price_history
        ]
    }

@router.get("/{product_id}/price-analysis")
async def get_price_analysis(product_id: int, db: Session = Depends(get_db)):
    """Get price trend analysis using LLM"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get price history for last 90 days
    since_date = datetime.utcnow() - timedelta(days=90)
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.recorded_at >= since_date
    ).order_by(PriceHistory.recorded_at).all()
    
    if not price_history:
        return {"message": "No price history available"}
    
    # Prepare price data for LLM analysis
    price_data = [
        {
            "price": ph.price,
            "date": ph.recorded_at.isoformat(),
            "source": ph.source
        }
        for ph in price_history
    ]
    
    # Get LLM analysis
    analysis = await llm_service.analyze_price_trends(price_data)
    
    return {
        "product_name": product.name,
        "current_price": product.price,
        "analysis": analysis,
        "data_points": len(price_data)
    }

@router.get("/category/{category}")
async def get_products_by_category(category: str, limit: int = 20, db: Session = Depends(get_db)):
    """Get products by category"""
    products = db.query(Product).filter(
        Product.category == category
    ).limit(limit).all()
    
    return [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "currency": product.currency,
            "image_url": product.image_url,
            "ratings": product.ratings,
            "source_url": product.source_url
        }
        for product in products
    ] 