# Data Mesh Architecture Implementation

A comprehensive implementation of a data mesh architecture with data quality, lineage tracking, and catalog management capabilities.

## Overview

This project implements a data mesh architecture that enables organizations to manage their data as a product. It provides services for data quality management, lineage tracking, and data catalog management, all following data mesh principles.

## Features

### Data Catalog Service
- Product registration and versioning
- Schema management
- Quality rules and policies
- Search and discovery
- Lineage tracking
- Domain-based organization

### Data Quality Service
- Rule-based quality checks
- Multiple check types (completeness, accuracy, consistency, timeliness)
- Quality metrics and reporting
- Check history tracking
- Configurable severity levels

### Data Lineage Service
- Graph-based lineage tracking
- Impact analysis
- Upstream/downstream dependency tracking
- Transformation tracking
- Graph visualization support

## Project Structure

```
data_mesh/
├── api/
│   └── catalog_service.py      # FastAPI service for catalog operations
├── catalog/
│   └── catalog.py             # Core catalog implementation
├── quality/
│   └── quality_service.py     # Data quality service implementation
├── lineage/
│   └── lineage_service.py     # Data lineage service implementation
├── governance/
│   └── policy_engine.py       # Policy enforcement engine
└── tests/
    ├── test_catalog_service.py
    ├── test_quality_service.py
    └── test_lineage_service.py
```

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```powershell
git clone https://github.com/yourusername/data-architecture.git
cd data-architecture
```

2. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

### Running Tests

Run the test suite using pytest:
```powershell
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=data_mesh

# Run specific test file
pytest tests/test_quality_service.py

# Run tests with verbose output
pytest -v
```

### Running Services

Start the services using uvicorn:
```powershell
# Start catalog service
uvicorn data_mesh.api.catalog_service:app --reload

# Start quality service
uvicorn data_mesh.quality.quality_service:app --reload

# Start lineage service
uvicorn data_mesh.lineage.lineage_service:app --reload
```

## API Documentation

### Catalog Service Endpoints

- `POST /products` - Register new data product
- `PUT /products/{name}` - Update existing product
- `GET /products/{name}` - Get product details
- `GET /products` - List all products
- `POST /products/{name}/versions` - Add new version
- `GET /products/{name}/versions` - Get version history
- `GET /search` - Search products
- `GET /products/{name}/lineage` - Get lineage information
- `GET /products/{name}/quality` - Get quality information

### Quality Service Endpoints

- `POST /rules` - Add quality rule
- `DELETE /rules/{name}` - Remove quality rule
- `POST /check` - Run quality checks
- `GET /rules/{name}/history` - Get check history
- `GET /metrics` - Get quality metrics

### Lineage Service Endpoints

- `POST /nodes` - Add node
- `POST /edges` - Add edge
- `GET /nodes/{node_id}` - Get node details
- `GET /nodes/{node_id}/upstream` - Get upstream nodes
- `GET /nodes/{node_id}/downstream` - Get downstream nodes
- `GET /lineage/{source_id}/{target_id}` - Get lineage path
- `GET /impact/{node_id}` - Get impact analysis
- `GET /summary` - Get graph summary

## Development

### Adding New Features

1. Create feature branch:
```powershell
git checkout -b feature/your-feature-name
```

2. Implement changes and add tests
3. Run test suite
4. Submit pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all functions and classes
- Keep functions small and focused

## Testing

The project includes comprehensive test coverage for all components:

### Test Categories

1. **Unit Tests**
   - Individual component testing
   - Mock dependencies
   - Test edge cases

2. **Integration Tests**
   - Component interaction testing
   - End-to-end workflows
   - API endpoint testing

3. **Quality Tests**
   - Rule validation
   - Check execution
   - Metrics calculation

4. **Lineage Tests**
   - Graph operations
   - Path finding
   - Impact analysis

## Documentation

Additional documentation is available in the `docs/` directory:

- `docs/additional/data-quality-framework-implementation.md`
- `docs/additional/data-mesh-migration-implementation.md`
- `docs/additional/data-mesh-security.md`
- `docs/additional/data-mesh-operations.md`
- `docs/additional/data-mesh-testing.md`
- `docs/additional/data-mesh-governance.md`
- `docs/additional/data-mesh-integration.md`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments

- Data Mesh Architecture principles
- FastAPI framework
- Pydantic for data validation
- Pytest for testing framework 