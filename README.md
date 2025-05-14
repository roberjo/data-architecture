# Data Mesh Implementation

A modern data architecture implementation using data mesh principles, focusing on data quality, governance, and integration.

## Features

- Data Quality Framework
  - Quality rule engine
  - Quality monitoring
  - Quality reporting
  - Prometheus metrics
- REST API Service
  - Quality rule management
  - Quality checks
  - Quality reports
  - Health monitoring

## Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

## Installation

1. Clone the repository:
```powershell
git clone https://github.com/yourusername/data-mesh.git
cd data-mesh
```

2. Create and activate a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```powershell
pip install -e .
```

## Running the Service

Start the data quality service:
```powershell
python -m data_mesh.main
```

The service will be available at http://localhost:8000

## API Documentation

Once the service is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Usage

1. Add a quality rule:
```powershell
$rule = @{
    name = "not_null_rule"
    description = "Check for non-null values"
    rule_type = "not_null"
    parameters = @{}
    severity = "high"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/rules" -Method Post -Body $rule -ContentType "application/json"
```

2. Check data quality:
```powershell
$data = @{
    data = @{
        field1 = "test"
        field2 = $null
    }
    domain = "test_domain"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/check" -Method Post -Body $data -ContentType "application/json"
```

3. Get quality report:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/report/test_domain" -Method Get
```

## Running Tests

Run the test suite:
```powershell
pytest
```

Run tests with coverage:
```powershell
pytest --cov=data_mesh
```

## Project Structure

```
data-mesh/
├── data_mesh/
│   ├── api/
│   │   └── quality_service.py
│   │   
│   ├── quality/
│   │   ├── engine.py
│   │   └── monitor.py
│   └── main.py
├── tests/
│   └── test_quality.py
├── pyproject.toml
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 