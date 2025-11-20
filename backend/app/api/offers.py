from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.offer import ScrapedOffer
from ..schemas.offer import OfferResponse
from ..scrapers.rekrute_scraper import RekruteScraper
from ..config import settings

router = APIRouter(prefix="/api/offers", tags=["Offers"])


@router.get("", response_model=List[OfferResponse])
def get_offers(
    ville: Optional[str] = None,
    type_contrat: Optional[str] = None,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """Get list of active job offers"""
    query = db.query(ScrapedOffer).filter(ScrapedOffer.est_active == True)
    
    # Apply filters
    if ville:
        query = query.filter(ScrapedOffer.ville.ilike(f"%{ville}%"))
    if type_contrat:
        query = query.filter(ScrapedOffer.type_contrat.ilike(f"%{type_contrat}%"))
    
    # Sort by date and limit
    offers = query.order_by(ScrapedOffer.date_publication.desc()).limit(limit).all()
    
    return offers


@router.get("/search", response_model=List[OfferResponse])
def search_offers(
    q: Optional[str] = None,
    ville: Optional[str] = None,
    type_contrat: Optional[str] = None,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    """Search job offers by keywords"""
    query = db.query(ScrapedOffer).filter(ScrapedOffer.est_active == True)
    
    # Search in title and description
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            (ScrapedOffer.titre.ilike(search_term)) | 
            (ScrapedOffer.description.ilike(search_term))
        )
    
    # Apply filters
    if ville:
        query = query.filter(ScrapedOffer.ville.ilike(f"%{ville}%"))
    if type_contrat:
        query = query.filter(ScrapedOffer.type_contrat.ilike(f"%{type_contrat}%"))
    
    # Sort by date and limit
    offers = query.order_by(ScrapedOffer.date_publication.desc()).limit(limit).all()
    
    return offers


@router.get("/{offer_id}", response_model=OfferResponse)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    """Get specific job offer details"""
    offer = db.query(ScrapedOffer).filter(ScrapedOffer.id == offer_id).first()
    
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    
    return offer


@router.post("/scrape")
def scrape_offers(db: Session = Depends(get_db)):
    """Manually trigger job scraping (admin only in production)"""
    if not settings.SCRAPING_ENABLED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Scraping is disabled"
        )
    
    try:
        scraper = RekruteScraper()
        offers = scraper.scrape()
        saved_count = scraper.save_to_db(offers, db)
        
        return {
            "status": "success",
            "offers_found": len(offers),
            "offers_saved": saved_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Scraping failed: {str(e)}"
        )


