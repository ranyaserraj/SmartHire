from abc import ABC, abstractmethod
from typing import List, Dict
from sqlalchemy.orm import Session


class BaseScraper(ABC):
    """Abstract base class for job scrapers"""
    
    def __init__(self):
        self.source_site = "unknown"
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape job offers and return list of offer dictionaries"""
        pass
    
    @abstractmethod
    def parse_offer(self, html) -> Dict:
        """Parse a single offer HTML and return offer dictionary"""
        pass
    
    @abstractmethod
    def save_to_db(self, offers: List[Dict], db: Session) -> int:
        """Save offers to database and return count of saved offers"""
        pass


