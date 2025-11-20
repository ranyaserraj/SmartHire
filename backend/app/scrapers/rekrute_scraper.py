import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from typing import List, Dict
from sqlalchemy.orm import Session
from datetime import datetime
from .base_scraper import BaseScraper
from ..models.offer import ScrapedOffer
from ..config import settings


class RekruteScraper(BaseScraper):
    """Scraper for Rekrute.com job offers"""
    
    def __init__(self):
        super().__init__()
        self.source_site = "rekrute"
        self.base_url = "https://www.rekrute.com"
        self.offers_url = f"{self.base_url}/offres.html"
        self.ua = UserAgent()
    
    def scrape(self) -> List[Dict]:
        """Scrape job offers from Rekrute.com"""
        offers = []
        
        try:
            headers = {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            }
            
            response = requests.get(self.offers_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find job offer cards (adjust selectors based on actual website structure)
            offer_cards = soup.find_all("div", class_="post-id")[:settings.SCRAPING_MAX_OFFERS]
            
            for card in offer_cards:
                try:
                    offer = self.parse_offer(card)
                    if offer:
                        offers.append(offer)
                except Exception as e:
                    print(f"Error parsing offer: {e}")
                    continue
        
        except Exception as e:
            print(f"Error scraping Rekrute: {e}")
        
        return offers
    
    def parse_offer(self, card) -> Dict:
        """Parse a single offer card"""
        try:
            # Extract title
            title_elem = card.find("h3") or card.find("h2") or card.find("a", class_="titreJob")
            titre = title_elem.get_text(strip=True) if title_elem else "Titre non disponible"
            
            # Extract company
            company_elem = card.find("span", class_="company") or card.find("div", class_="company")
            entreprise = company_elem.get_text(strip=True) if company_elem else None
            
            # Extract location
            location_elem = card.find("span", class_="location") or card.find("div", class_="location")
            localisation = location_elem.get_text(strip=True) if location_elem else None
            
            # Extract city from location
            ville = localisation.split(",")[0].strip() if localisation else None
            
            # Extract description
            desc_elem = card.find("p", class_="description") or card.find("div", class_="description")
            description = desc_elem.get_text(strip=True) if desc_elem else "Description non disponible"
            
            # Extract URL
            link_elem = card.find("a", href=True)
            url_relative = link_elem["href"] if link_elem else ""
            url_source = f"{self.base_url}{url_relative}" if url_relative.startswith("/") else url_relative
            
            # Extract contract type (if available)
            contract_elem = card.find("span", class_="contrat")
            type_contrat = contract_elem.get_text(strip=True) if contract_elem else None
            
            return {
                "titre": titre,
                "entreprise": entreprise,
                "description": description[:1000],  # Limit description length
                "localisation": localisation,
                "ville": ville,
                "type_contrat": type_contrat,
                "salaire": None,
                "url_source": url_source,
                "source_site": self.source_site,
                "date_publication": None,
                "competences_requises": [],
                "competences_souhaitees": [],
            }
        
        except Exception as e:
            print(f"Error in parse_offer: {e}")
            return None
    
    def save_to_db(self, offers: List[Dict], db: Session) -> int:
        """Save offers to database"""
        saved_count = 0
        
        for offer_data in offers:
            try:
                # Check if offer already exists (by URL)
                existing = db.query(ScrapedOffer).filter(
                    ScrapedOffer.url_source == offer_data["url_source"]
                ).first()
                
                if existing:
                    # Update existing offer
                    for key, value in offer_data.items():
                        setattr(existing, key, value)
                    existing.date_scraping = datetime.utcnow()
                else:
                    # Create new offer
                    new_offer = ScrapedOffer(**offer_data)
                    db.add(new_offer)
                
                saved_count += 1
            
            except Exception as e:
                print(f"Error saving offer: {e}")
                continue
        
        db.commit()
        return saved_count


