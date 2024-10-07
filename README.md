# FastAPI Inventory Management (F.I.M.)

This repository provides a fully functional FastAPI application for managing inventory data. It demonstrates essential functionalities like querying, adding, updating, and deleting items while maintaining efficient data storage and retrieval practices.

## Features:

* Item Model: Defines a Category enum for TOOLS and CONSUMABLES, along with name, price, count, and id attributes for each item.
* CRUD Operations:
    * GET Methods:
"/": Returns all items in JSON format.
"/items/{item_id}": Queries an item by its ID and returns details.
"/items/" (with optional query parameters): Filters items based on name, price, count, and category.
    * POST Method: "/": Adds a new item to the inventory with proper validation for duplicate IDs.
    * PUT Method: "/items/{item_id}": Updates existing items, enforcing that at least one field is modified.
    * DELETE Method: "/items/{item_id}": Removes an item by its ID.
* Error Handling: Leverages FastAPI's built-in exception handling with appropriate HTTP status codes for informative error messages (e.g., 404 for non-existent items).
* Data Persistence: Although this example uses an in-memory dictionary for simplicity, you can easily switch to a more robust persistent storage mechanism like a database for production deployments.

## Getting Started:

1. Clone the Repository:

```bash
git clone https://github.com/your-username/fastapi-inventory-management.git
```

2. Install Dependencies:

```bash
cd fastapi-inventory-management
pip install fastapi pydantic
```

3. Run the Application:

```bash
uvicorn main:app --reload
```

## Usage Examples:

* Listing All Items:

```
GET http://localhost:8000/
```

* Fetching an Item by ID:

```
GET http://localhost:8000/items/0
```

* Adding a New Item:

```json
POST http://localhost:8000/
Content-Type: application/json

{
  "name": "Screwdriver Set",
  "price": 7.99,
  "count": 15,
  "category": "TOOLS"
}
```