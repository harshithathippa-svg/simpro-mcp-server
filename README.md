# Simpro MCP Server

## Endpoints Used

### Customers
GET /companies/{companyId}/customers/

### Jobs
GET /companies/{companyId}/jobs/

### Quotes
GET /companies/{companyId}/quotes/

## Installation

```bash
pip install -r requirements.txt
```

## Run Server

```bash
python -m uvicorn server:app --reload
```

## Swagger UI

http://127.0.0.1:8000/docs

## MCP Tool Discovery

GET /tools/list

## MCP Tool Execution

POST /tools/call

### Example Request

```json
{
  "name": "customers"
}
```