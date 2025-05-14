from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime

from ..catalog.catalog import DataCatalog, DataProduct, DataProductVersion

app = FastAPI(title="Data Catalog Service")
catalog = DataCatalog()

class ProductRequest(BaseModel):
    """Request model for registering/updating a data product."""
    name: str
    description: str
    domain: str
    owner: str
    version: str
    schema: Dict[str, any]
    quality_rules: List[str] = []
    policies: List[str] = []
    tags: List[str] = []

class VersionRequest(BaseModel):
    """Request model for adding a new version."""
    product_name: str
    version: str
    schema: Dict[str, any]
    created_by: str
    change_description: str

@app.post("/products", response_model=DataProduct)
async def register_product(product: ProductRequest):
    """Register a new data product."""
    try:
        data_product = DataProduct(**product.dict())
        catalog.register_product(data_product)
        return data_product
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/products/{name}", response_model=DataProduct)
async def update_product(name: str, product: ProductRequest):
    """Update an existing data product."""
    try:
        data_product = DataProduct(**product.dict())
        catalog.update_product(data_product)
        return data_product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/products/{name}", response_model=DataProduct)
async def get_product(name: str):
    """Get a data product by name."""
    product = catalog.get_product(name)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {name} not found")
    return product

@app.get("/products", response_model=List[DataProduct])
async def list_products(domain: Optional[str] = None):
    """List all data products, optionally filtered by domain."""
    return catalog.list_products(domain)

@app.post("/products/{name}/versions", response_model=DataProductVersion)
async def add_version(name: str, version: VersionRequest):
    """Add a new version of a data product."""
    try:
        data_version = DataProductVersion(**version.dict())
        catalog.add_version(data_version)
        return data_version
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/products/{name}/versions", response_model=List[DataProductVersion])
async def get_versions(name: str):
    """Get all versions of a data product."""
    versions = catalog.get_versions(name)
    if not versions:
        raise HTTPException(status_code=404, detail=f"No versions found for product {name}")
    return versions

@app.get("/search", response_model=List[DataProduct])
async def search_products(query: str = Query(..., min_length=1)):
    """Search for data products."""
    return catalog.search_products(query)

@app.get("/products/{name}/lineage")
async def get_product_lineage(name: str):
    """Get lineage information for a data product."""
    try:
        return catalog.get_product_lineage(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/products/{name}/quality")
async def get_product_quality(name: str):
    """Get quality information for a data product."""
    try:
        return catalog.get_product_quality(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()} 