# E-commerce Dashboard API

This is a FastAPI-based RESTful API for an E-commerce dashboard, allowing you to retrieve sales data, analyze revenue, manage inventory, and more.

## Getting Started

### Prerequisites

- Python 3.6+
- MySQL Server
- Git (optional)

### Installation

1. Clone the repository:

    git clone https://github.com/yourusername/ecom-dashboard-api.git
   
2. Install the required packages:

    pip install -r requirements.txt

3. Database Configuration

Update the database configuration in the main.py file with your MySQL credentials:

    mysql.connector.connect(
        host="localhost",
        user="yourusername",
        password="yourpassword",
        database="ecom_dashboard"
    )
    
4. Create Database
   
Open MySQL shell in the project directory and run the sql script through following command

    mysql -u [yourusername] -p < database.sql

5. Install Dependencies

Navigate to the project directory and install the required Python dependencies

    pip install -r requirements.txt

6. Run the Application

Start the FastAPI application using the following command:

    uvicorn main:app --host 0.0.0.0 --port 8000

## Endpoints

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

GET /products/{product_name}/{price}/{category_id}: Register a new product.

## Usage

You can interact with the API by sending HTTP requests to the provided endpoints. Make sure to include valid request parameters and data when necessary.

For example, to retrieve sales data, make a GET request to /sales/:

##Author
Jawad Afzal



