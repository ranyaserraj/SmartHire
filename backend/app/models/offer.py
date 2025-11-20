from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB
from ..database import Base


class ScrapedOffer(Base):
    __tablename__ = "scraped_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    entreprise = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    localisation = Column(String(100), nullable=True)
    ville = Column(String(100), nullable=True, index=True)
    type_contrat = Column(String(50), nullable=True)
    salaire = Column(String(100), nullable=True)
    url_source = Column(Text, unique=True, nullable=False)
    source_site = Column(String(50), nullable=False, index=True)
    date_publication = Column(Date, nullable=True, index=True)
    competences_requises = Column(JSONB, nullable=True)
    competences_souhaitees = Column(JSONB, nullable=True)
    est_active = Column(Boolean, default=True, index=True)
    date_scraping = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())


