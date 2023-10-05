# Ecommerce-Dashboard-API-s

#Overview

This FastAPI-based API serves as the backend for an Ecommerce Dashboard application. It provides endpoints to retrieve sales data, perform revenue analysis, view inventory status, update inventory levels, and manage products.

Setup Instructions
To run the Ecommerce Dashboard API locally, follow these setup instructions:

Clone the Repository

Clone this repository to your local machine:

bash
Copy code
git clone https://github.com/yourusername/ecommerce-dashboard-api.git
Install Dependencies

Navigate to the project directory and install the required Python dependencies using pip:

bash
Copy code
cd ecommerce-dashboard-api
pip install -r requirements.txt
Database Configuration

Create a MySQL database named ecom_dashboard and update the database configuration in the main.py file with your MySQL credentials:

python
Copy code
connection = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="ecom_dashboard"
)
Run the Application

Start the FastAPI application using the following command:

css
Copy code
uvicorn main:app --host 0.0.0.0 --port 8000
This will start the API server at http://127.0.0.1:8000.

Dependencies
FastAPI: A modern, fast web framework for building APIs with Python.
uvicorn: ASGI server for running FastAPI applications.
mysql-connector-python: MySQL connector for Python to interact with the database.
Endpoints
The Ecommerce Dashboard API provides the following endpoints:

GET /sales/: Retrieve sales data.

GET /revenue/{analysis_type}/{start_date}/{end_date}: Calculate revenue based on the analysis type (weekly, monthly, annual) and date range.

GET /revenue/daily/{start_date}: Calculate daily revenue for a specific date.

GET /compare-revenue/{start_date}/{end_date}/{category_id}: Compare revenue across different periods and categories.

GET /sales-data/product/{start_date}/{end_date}/{product_id}: Get sales data by product within a date range.

GET /sales-data/category/{start_date}/{end_date}/{category_id}: Get sales data by category within a date range.

GET /inventory-status/: View inventory status, including products with low stock.

GET /inventory/: Get all inventory data.

GET /inventory/update-add/{product_id}: Update product quantity in inventory by adding.

GET /inventory/update-subtract/{product_id}: Update product quantity in inventory by subtracting.

POST /products/: Register a new product.

Usage
You can interact with the API by sending HTTP requests to the provided endpoints. Make sure to include valid request parameters and data when necessary.

For example, to retrieve sales data, make a GET request to /sales/:

arduino
Copy code
GET http://127.0.0.1:8000/sales/
Author
Your Name
Email: your.email@example.com
