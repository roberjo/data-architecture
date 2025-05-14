import pytest
from datetime import datetime
from data_mesh.catalog.catalog import (
    DataCatalog,
    DataProduct,
    DataProductVersion
)

@pytest.fixture
def catalog():
    """Fixture to create a fresh catalog instance for each test."""
    return DataCatalog()

@pytest.fixture
def sample_product():
    """Fixture to create a sample data product."""
    return DataProduct(
        name="test_product",
        description="Test data product",
        domain="test_domain",
        owner="test_owner",
        version="1.0.0",
        schema={
            "id": "integer",
            "name": "string",
            "value": "float"
        },
        quality_rules=["completeness", "accuracy"],
        policies=["data_retention"],
        tags=["test", "sample"]
    )

@pytest.fixture
def sample_version(sample_product):
    """Fixture to create a sample product version."""
    return DataProductVersion(
        product_name=sample_product.name,
        version="1.0.1",
        schema={
            "id": "integer",
            "name": "string",
            "value": "float",
            "timestamp": "datetime"
        },
        created_by="test_user",
        change_description="Added timestamp field"
    )

def test_register_product(catalog, sample_product):
    """Test registering a new data product."""
    catalog.register_product(sample_product)
    assert sample_product.name in catalog.products
    assert catalog.products[sample_product.name] == sample_product
    assert sample_product.name in catalog.versions
    assert catalog.versions[sample_product.name] == []

def test_update_product(catalog, sample_product):
    """Test updating an existing data product."""
    catalog.register_product(sample_product)
    updated_product = DataProduct(
        **{**sample_product.dict(), "description": "Updated description"}
    )
    catalog.update_product(updated_product)
    assert catalog.products[sample_product.name].description == "Updated description"

def test_update_nonexistent_product(catalog, sample_product):
    """Test updating a nonexistent product."""
    with pytest.raises(ValueError, match="Product .* not found"):
        catalog.update_product(sample_product)

def test_get_product(catalog, sample_product):
    """Test retrieving a data product."""
    catalog.register_product(sample_product)
    retrieved_product = catalog.get_product(sample_product.name)
    assert retrieved_product == sample_product

def test_list_products(catalog, sample_product):
    """Test listing data products."""
    catalog.register_product(sample_product)
    products = catalog.list_products()
    assert len(products) == 1
    assert products[0] == sample_product

def test_list_products_by_domain(catalog, sample_product):
    """Test listing data products filtered by domain."""
    catalog.register_product(sample_product)
    products = catalog.list_products(domain="test_domain")
    assert len(products) == 1
    assert products[0] == sample_product
    
    products = catalog.list_products(domain="other_domain")
    assert len(products) == 0

def test_add_version(catalog, sample_product, sample_version):
    """Test adding a new version to a data product."""
    catalog.register_product(sample_product)
    catalog.add_version(sample_version)
    versions = catalog.get_versions(sample_product.name)
    assert len(versions) == 1
    assert versions[0] == sample_version

def test_add_version_nonexistent_product(catalog, sample_version):
    """Test adding a version to a nonexistent product."""
    with pytest.raises(ValueError, match="Product .* not found"):
        catalog.add_version(sample_version)

def test_get_versions(catalog, sample_product, sample_version):
    """Test retrieving versions of a data product."""
    catalog.register_product(sample_product)
    catalog.add_version(sample_version)
    versions = catalog.get_versions(sample_product.name)
    assert len(versions) == 1
    assert versions[0] == sample_version

def test_search_products(catalog, sample_product):
    """Test searching for data products."""
    catalog.register_product(sample_product)
    
    # Search by name
    results = catalog.search_products("test_product")
    assert len(results) == 1
    assert results[0] == sample_product
    
    # Search by description
    results = catalog.search_products("Test data")
    assert len(results) == 1
    assert results[0] == sample_product
    
    # Search by tag
    results = catalog.search_products("sample")
    assert len(results) == 1
    assert results[0] == sample_product
    
    # No results
    results = catalog.search_products("nonexistent")
    assert len(results) == 0

def test_get_product_lineage(catalog, sample_product):
    """Test retrieving product lineage information."""
    catalog.register_product(sample_product)
    lineage = catalog.get_product_lineage(sample_product.name)
    assert lineage["product"] == sample_product.name
    assert isinstance(lineage["versions"], list)
    assert isinstance(lineage["dependencies"], list)
    assert isinstance(lineage["dependents"], list)

def test_get_product_quality(catalog, sample_product):
    """Test retrieving product quality information."""
    catalog.register_product(sample_product)
    quality = catalog.get_product_quality(sample_product.name)
    assert quality["product"] == sample_product.name
    assert quality["quality_rules"] == sample_product.quality_rules
    assert quality["policies"] == sample_product.policies
    assert "last_updated" in quality 