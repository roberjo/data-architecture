from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class DataProduct(BaseModel):
    """Represents a data product in the catalog."""
    name: str
    description: str
    domain: str
    owner: str
    version: str
    schema: Dict[str, Any]
    quality_rules: List[str] = []
    policies: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    tags: List[str] = []
    status: str = "active"

class DataProductVersion(BaseModel):
    """Represents a version of a data product."""
    product_name: str
    version: str
    schema: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)
    created_by: str
    change_description: str

class DataCatalog:
    """Core catalog for managing data products and metadata."""
    
    def __init__(self):
        self.products: Dict[str, DataProduct] = {}
        self.versions: Dict[str, List[DataProductVersion]] = {}
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the catalog."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def register_product(self, product: DataProduct) -> None:
        """
        Register a new data product in the catalog.
        
        Args:
            product: The data product to register
        """
        self.products[product.name] = product
        self.versions[product.name] = []
        logger.info(f"Registered data product: {product.name}")
    
    def update_product(self, product: DataProduct) -> None:
        """
        Update an existing data product.
        
        Args:
            product: The updated data product
        """
        if product.name not in self.products:
            raise ValueError(f"Product {product.name} not found")
        
        self.products[product.name] = product
        product.updated_at = datetime.now()
        logger.info(f"Updated data product: {product.name}")
    
    def get_product(self, name: str) -> Optional[DataProduct]:
        """
        Get a data product by name.
        
        Args:
            name: Name of the data product
            
        Returns:
            The data product if found, None otherwise
        """
        return self.products.get(name)
    
    def list_products(self, domain: Optional[str] = None) -> List[DataProduct]:
        """
        List all data products, optionally filtered by domain.
        
        Args:
            domain: Optional domain to filter by
            
        Returns:
            List of data products
        """
        if domain:
            return [p for p in self.products.values() if p.domain == domain]
        return list(self.products.values())
    
    def add_version(self, version: DataProductVersion) -> None:
        """
        Add a new version of a data product.
        
        Args:
            version: The new version to add
        """
        if version.product_name not in self.versions:
            raise ValueError(f"Product {version.product_name} not found")
        
        self.versions[version.product_name].append(version)
        logger.info(f"Added version {version.version} for product {version.product_name}")
    
    def get_versions(self, product_name: str) -> List[DataProductVersion]:
        """
        Get all versions of a data product.
        
        Args:
            product_name: Name of the data product
            
        Returns:
            List of versions
        """
        return self.versions.get(product_name, [])
    
    def search_products(self, query: str) -> List[DataProduct]:
        """
        Search for data products by name, description, or tags.
        
        Args:
            query: Search query
            
        Returns:
            List of matching data products
        """
        query = query.lower()
        return [
            p for p in self.products.values()
            if query in p.name.lower() or
               query in p.description.lower() or
               any(query in tag.lower() for tag in p.tags)
        ]
    
    def get_product_lineage(self, product_name: str) -> Dict[str, Any]:
        """
        Get the lineage information for a data product.
        
        Args:
            product_name: Name of the data product
            
        Returns:
            Lineage information
        """
        if product_name not in self.products:
            raise ValueError(f"Product {product_name} not found")
        
        # In a real implementation, this would include actual lineage information
        return {
            "product": product_name,
            "versions": [v.version for v in self.versions[product_name]],
            "dependencies": [],  # Would include actual dependencies
            "dependents": []     # Would include actual dependents
        }
    
    def get_product_quality(self, product_name: str) -> Dict[str, Any]:
        """
        Get quality information for a data product.
        
        Args:
            product_name: Name of the data product
            
        Returns:
            Quality information
        """
        if product_name not in self.products:
            raise ValueError(f"Product {product_name} not found")
        
        product = self.products[product_name]
        return {
            "product": product_name,
            "quality_rules": product.quality_rules,
            "policies": product.policies,
            "last_updated": product.updated_at.isoformat()
        } 