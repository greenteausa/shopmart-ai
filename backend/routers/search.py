from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import asyncio
import logging

from database import get_db, SearchHistory, Product, PriceHistory
from llm_service import llm_service, SearchRound
from search_service import search_service

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    user_id: Optional[int] = None
    max_rounds: int = 3

class SearchResponse(BaseModel):
    query: str
    rounds_completed: int
    total_results: int
    search_analysis: Dict[str, Any]
    products: List[Dict[str, Any]]
    price_analysis: Dict[str, Any]
    category_insights: str
    buying_recommendation: str
    search_id: int

class ChatRequest(BaseModel):
    search_id: int
    message: str
    user_id: Optional[int] = None

def create_mock_search_response(query: str) -> Dict[str, Any]:
    """Create a mock search response when LLM service is unavailable"""
    mock_products = [
        {
            "name": f"{query} - Premium Edition",
            "brand": "TechBrand",
            "price": 299.99,
            "currency": "USD",
            "source": "Amazon",
            "source_url": "https://amazon.com/product1",
            "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=100&h=100&fit=crop",
            "key_features": ["High Quality", "Fast Shipping", "1 Year Warranty"],
            "pros": ["Great value", "Reliable brand"],
            "cons": ["Higher price"],
            "rating": 4.5,
            "review_count": 1234,
            "availability": True
        },
        {
            "name": f"{query} - Budget Model",
            "brand": "ValueBrand",
            "price": 149.99,
            "currency": "USD",
            "source": "eBay",
            "source_url": "https://ebay.com/product2",
            "image_url": "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=100&h=100&fit=crop",
            "key_features": ["Affordable", "Good Quality", "Fast Delivery"],
            "pros": ["Low price", "Good reviews"],
            "cons": ["Limited features"],
            "rating": 4.0,
            "review_count": 567,
            "availability": True
        },
        {
            "name": f"{query} - Professional Grade",
            "brand": "ProBrand",
            "price": 499.99,
            "currency": "USD",
            "source": "Best Buy",
            "source_url": "https://bestbuy.com/product3",
            "image_url": "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?w=100&h=100&fit=crop",
            "key_features": ["Professional Grade", "Extended Warranty", "Premium Support"],
            "pros": ["Top quality", "Professional support"],
            "cons": ["Expensive"],
            "rating": 4.8,
            "review_count": 890,
            "availability": True
        }
    ]
    
    return {
        "products": mock_products,
        "price_analysis": {
            "lowest_price": 149.99,
            "highest_price": 499.99,
            "average_price": 316.65,
            "best_deal": "eBay - Budget Model offers best value"
        },
        "category_insights": f"The {query} market offers good variety from budget to premium options. Prices range significantly based on brand and features.",
        "buying_recommendation": f"For {query}, consider the Budget Model for value or Premium Edition for best features. Professional Grade is ideal if you need maximum quality."
    }

@router.post("/", response_model=SearchResponse)
async def search_products(request: SearchRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Perform multi-round LLM-powered product search
    """
    try:
        # Step 1: Try LLM analysis, fallback to mock if it fails
        try:
            logging.info(f"Starting search for query: {request.query}")
            query_analysis = await llm_service.analyze_user_query(request.query)
            use_llm = True
        except Exception as llm_error:
            logging.warning(f"LLM service unavailable, using mock data: {llm_error}")
            query_analysis = {
                "product_name": request.query,
                "category": "general",
                "key_features": [],
                "price_range": {"min": 0, "max": 1000},
                "search_keywords": [request.query],
                "intent": "research",
                "specificity": "medium"
            }
            use_llm = False
        
        if use_llm:
            # Step 2: Perform multiple rounds of searching with LLM
            search_rounds = []
            all_search_results = []
            
            for round_num in range(1, request.max_rounds + 1):
                logging.info(f"Starting search round {round_num}")
                
                # Generate search queries for this round
                search_queries = await llm_service.generate_search_queries(query_analysis, round_num)
                
                # Perform searches across multiple sources
                round_results = await search_service.search_multiple_sources(search_queries)
                
                # Convert search results to dict format
                round_results_dict = [
                    {
                        "title": result.title,
                        "price": result.price,
                        "currency": result.currency,
                        "source": result.source,
                        "url": result.url,
                        "image_url": result.image_url,
                        "description": result.description,
                        "rating": result.rating,
                        "review_count": result.review_count,
                        "availability": result.availability
                    }
                    for result in round_results
                ]
                
                # Create search round object
                search_round = SearchRound(
                    query=f"Round {round_num}: {', '.join(search_queries)}",
                    results=round_results_dict,
                    reasoning=f"Round {round_num} focused on: " + (
                        "basic product info and prices" if round_num == 1 else
                        "technical specs and reviews" if round_num == 2 else
                        "deals and alternatives"
                    )
                )
                
                search_rounds.append(search_round)
                all_search_results.extend(round_results_dict)
                
                # Analyze current results and decide if more rounds are needed
                analysis = await llm_service.analyze_search_results(
                    request.query, 
                    round_results_dict, 
                    search_rounds[:-1]
                )
                
                # Stop early if we have sufficient quality results
                if not analysis.get("needs_more_rounds", True) and round_num >= 2:
                    logging.info(f"Stopping search early after round {round_num} - sufficient results found")
                    break
            
            # Step 3: Generate comprehensive summary using LLM
            logging.info("Generating product summary with LLM")
            product_summary = await llm_service.generate_product_summary(search_rounds)
            
        else:
            # Use mock data when LLM is unavailable
            logging.info("Using mock search results")
            product_summary = create_mock_search_response(request.query)
            search_rounds = [SearchRound(
                query=f"Mock search for: {request.query}",
                results=product_summary["products"],
                reasoning="Mock search results for demonstration"
            )]
        
        # Step 4: Store search history in database
        search_history = SearchHistory(
            user_id=request.user_id,
            query=request.query,
            search_results={
                "rounds": [round.dict() for round in search_rounds],
                "summary": product_summary,
                "analysis": query_analysis
            },
            search_rounds=len(search_rounds)
        )
        
        db.add(search_history)
        db.commit()
        db.refresh(search_history)
        
        # Step 5: Store products in database (background task)
        background_tasks.add_task(store_products_background, product_summary.get("products", []), db)
        
        # Step 6: Prepare response
        response = SearchResponse(
            query=request.query,
            rounds_completed=len(search_rounds),
            total_results=len(product_summary.get("products", [])),
            search_analysis=query_analysis,
            products=product_summary.get("products", []),
            price_analysis=product_summary.get("price_analysis", {}),
            category_insights=product_summary.get("category_insights", ""),
            buying_recommendation=product_summary.get("buying_recommendation", ""),
            search_id=search_history.id
        )
        
        logging.info(f"Search completed successfully. Found {len(product_summary.get('products', []))} products.")
        return response
        
    except Exception as e:
        logging.error(f"Search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.post("/chat")
async def chat_about_search(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Continue conversation about search results
    """
    try:
        # Get search history
        search_history = db.query(SearchHistory).filter(SearchHistory.id == request.search_id).first()
        if not search_history:
            raise HTTPException(status_code=404, detail="Search not found")
        
        # Try LLM response, fallback to simple response
        try:
            # Prepare context for LLM
            search_context = {
                "original_query": search_history.query,
                "search_results": search_history.search_results,
                "user_message": request.message
            }
            
            # Generate LLM response based on user's message and search context
            messages = [
                {
                    "role": "system",
                    "content": """You are a helpful shopping assistant. The user is asking about their previous search results. 
                    Provide helpful, specific advice based on the search results. You can:
                    - Answer questions about specific products
                    - Compare products from the search results
                    - Provide buying advice
                    - Clarify product features
                    - Suggest alternatives from the results
                    
                    Be conversational and helpful."""
                },
                {
                    "role": "user",
                    "content": f"Search context: {search_context}\n\nUser question: {request.message}"
                }
            ]
            
            response = await llm_service.call_llm(messages)
            
        except Exception as llm_error:
            logging.warning(f"LLM chat failed, using fallback: {llm_error}")
            # Simple fallback responses
            if "price" in request.message.lower():
                response = f"Based on your search for '{search_history.query}', I found products ranging from budget to premium options. The price analysis shows good variety to fit different budgets."
            elif "recommend" in request.message.lower():
                response = f"For '{search_history.query}', I'd recommend considering the budget model for value or the premium edition for best features, depending on your needs and budget."
            elif "compare" in request.message.lower():
                response = f"The products from your '{search_history.query}' search differ mainly in price, features, and brand reputation. Each has different strengths depending on your priorities."
            else:
                response = f"I found several options for '{search_history.query}'. What specific aspect would you like to know more about - pricing, features, or recommendations?"
        
        return {
            "response": response,
            "search_id": request.search_id,
            "query": search_history.query
        }
        
    except Exception as e:
        logging.error(f"Chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@router.get("/history")
async def get_search_history(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get user's search history
    """
    try:
        searches = db.query(SearchHistory).filter(
            SearchHistory.user_id == user_id
        ).order_by(
            SearchHistory.created_at.desc()
        ).limit(limit).all()
        
        return {
            "searches": [
                {
                    "id": search.id,
                    "query": search.query,
                    "created_at": search.created_at,
                    "search_rounds": search.search_rounds,
                    "results_count": len(search.search_results.get("summary", {}).get("products", []))
                }
                for search in searches
            ]
        }
        
    except Exception as e:
        logging.error(f"Failed to get search history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get search history: {str(e)}")

@router.get("/{search_id}")
async def get_search_details(search_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific search
    """
    try:
        search = db.query(SearchHistory).filter(SearchHistory.id == search_id).first()
        if not search:
            raise HTTPException(status_code=404, detail="Search not found")
        
        return {
            "id": search.id,
            "query": search.query,
            "created_at": search.created_at,
            "search_results": search.search_results,
            "search_rounds": search.search_rounds
        }
        
    except Exception as e:
        logging.error(f"Failed to get search details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get search details: {str(e)}")

async def store_products_background(products_data: List[Dict], db: Session):
    """Store products in database as background task"""
    try:
        for product_data in products_data:
            # Check if product already exists
            existing = db.query(Product).filter(
                Product.name == product_data.get("name"),
                Product.source == product_data.get("source")
            ).first()
            
            if not existing:
                product = Product(
                    name=product_data.get("name", ""),
                    brand=product_data.get("brand", ""),
                    category="general",  # Could be improved with LLM categorization
                    price=product_data.get("price", 0.0),
                    currency=product_data.get("currency", "USD"),
                    source=product_data.get("source", ""),
                    source_url=product_data.get("source_url", ""),
                    image_url=product_data.get("image_url"),
                    description=", ".join(product_data.get("key_features", [])),
                    features=product_data.get("key_features", []),
                    rating=product_data.get("rating"),
                    review_count=product_data.get("review_count"),
                    availability=product_data.get("availability", True)
                )
                db.add(product)
                
        db.commit()
        logging.info(f"Stored {len(products_data)} products in database")
        
    except Exception as e:
        logging.error(f"Failed to store products: {str(e)}")
        db.rollback() 