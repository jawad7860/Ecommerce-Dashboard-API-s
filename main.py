from fastapi import FastAPI, HTTPException, Depends
import mysql.connector
from mysql.connector import Error
from typing import List
from datetime import datetime, timedelta

# Create a function to establish a database connection
def get_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ecom_dashboard"
        )
        return connection  # Return the connection object if successful
    except Error as e:
        print(f"Failure to connect to Database: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")

app = FastAPI()

# Endpoint to retrieve sales data
@app.get("/sales/")
async def read_sales():
    try:
        conn = get_db()
        cursor = conn.cursor()
        query = "SELECT * FROM Sales"
        cursor.execute(query)
        sales_data = cursor.fetchall()
        cursor.close()
        conn.close()
        if not sales_data:
            raise HTTPException(status_code=404, detail="Sales data not found")
        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

## Endpoint for revenue analysis
@app.get("/revenue/{analysis_type}/{start_date}/{end_date}")
async def calculate_revenue(
    analysis_type: str,
    start_date: datetime,
    end_date: datetime
):
    try:
        conn = get_db()
        cursor = conn.cursor()

        query = None
        if analysis_type == "weekly":
            # Calculate weekly revenue
            query = """
            SELECT DATE(s.sale_date) AS sale_day, SUM(s.quantity * p.price) AS daily_revenue
            FROM Sales s
            JOIN Products p ON s.product_id = p.product_id
            WHERE s.sale_date BETWEEN %s AND %s
            GROUP BY sale_day
            """
        elif analysis_type == "monthly":
            # Calculate monthly revenue
            query = """
            SELECT YEAR(s.sale_date) AS year, MONTH(s.sale_date) AS month, SUM(s.quantity * p.price) AS monthly_revenue
            FROM Sales s
            JOIN Products p ON s.product_id = p.product_id
            WHERE s.sale_date BETWEEN %s AND %s
            GROUP BY year, month
            """
        elif analysis_type == "annual":
            # Calculate annual revenue
            query = """
            SELECT YEAR(s.sale_date) AS year, SUM(s.quantity * p.price) AS annual_revenue
            FROM Sales s
            JOIN Products p ON s.product_id = p.product_id
            WHERE s.sale_date BETWEEN %s AND %s
            GROUP BY year
            """

        if query:
            cursor.execute(query, (start_date, end_date))
            revenue_data = cursor.fetchall()
            cursor.close()
            conn.close()

            return {"revenue_data": revenue_data}
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis_type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
        
# Endpoint for daily revenue analysis with user-specified date in path
@app.get("/revenue/daily/{start_date}")
async def calculate_daily_revenue(
    start_date: datetime
):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Calculate daily revenue
        query = """
        SELECT DATE(s.sale_date) AS sale_day, SUM(s.quantity * p.price) AS daily_revenue
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        WHERE DATE(s.sale_date) = %s
        GROUP BY sale_day
        """

        cursor.execute(query, (start_date,))
        revenue_data = cursor.fetchall()
        cursor.close()
        conn.close()

        return {"revenue_data": revenue_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# Endpoint for comparing revenue across different periods and categories
@app.get("/compare-revenue/{start_date}/{end_date}/{category_id}")
async def compare_revenue(
    start_date: datetime ,
    end_date: datetime ,
    category_id: int 
):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Calculate revenue for the specified period and category
        query = """
        SELECT SUM(s.quantity * p.price) AS revenue
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        WHERE s.sale_date BETWEEN %s AND %s
        AND p.category_id = %s
        """

        cursor.execute(query, (start_date, end_date, category_id))
        revenue_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if revenue_data[0] is not None:
            return {"revenue": revenue_data[0]}
        else:
            return {"revenue": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
        

# Endpoint to provide sales data by product 
@app.get("/sales-data/product/{start_date}/{end_date}/{product_id}")
async def get_sales_data_by_product(
    start_date: str,
    end_date: str,
    product_id: int
):
    try:
        # Parse start_date and end_date as datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

        conn = get_db()
        cursor = conn.cursor()

        # Query to retrieve sales data for a specific product and within the date range
        product_query = """
        SELECT s.sale_date, s.quantity, p.price
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        WHERE s.sale_date BETWEEN %s AND %s
        AND s.product_id = %s
        """

        cursor.execute(product_query, (start_date, end_date, product_id))
        product_sales_data = cursor.fetchall()

        cursor.close()
        conn.close()

        if not product_sales_data:
            # Handle the case when no sales data is found
            return {"message": "No sales data found for the specified product and date range"}

        return {"product_sales_data": product_sales_data}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

# Endpoint to provide sales data by category 
@app.get("/sales-data/category/{start_date}/{end_date}/{category_id}")
async def get_sales_data_by_category(
    start_date: str,
    end_date: str,
    category_id: int
):
    try:
        # Parse start_date and end_date as datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")

        conn = get_db()
        cursor = conn.cursor()

        # Query to retrieve sales data for all products within a specific category and within the date range
        category_query = """
        SELECT s.sale_date, s.quantity, p.price
        FROM Sales s
        JOIN Products p ON s.product_id = p.product_id
        WHERE s.sale_date BETWEEN %s AND %s
        AND s.product_id IN (
            SELECT product_id
            FROM Products
            WHERE category_id = %s
        )
        """

        cursor.execute(category_query, (start_date, end_date, category_id))
        category_sales_data = cursor.fetchall()

        cursor.close()
        conn.close()

        if not category_sales_data:
            # Handle the case when no sales data is found
            return {"message": "No sales data found for the specified category and date range"}

        return {"category_sales_data": category_sales_data}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

  
@app.get("/inventory-status/")
async def view_inventory():
    try:
        conn = get_db()
        cursor = conn.cursor()
        

        
        # Main query to fetch inventory data for products with low stock
        query = """
  SELECT p.name AS product_name, i.stock_quantity, i.low_stock_threshold
        FROM Products p
        JOIN Inventory i ON p.product_id = i.product_id
        
          WHERE i.stock_quantity < i.low_stock_threshold
    
        """
        
        cursor.execute(query)
        inventory_data = cursor.fetchall()
        cursor.close()
        conn.close()

       	return inventory_data
    except Exception as e:
        
        raise HTTPException(status_code=500, detail="Internal server error")
        
#Endpoint to get all inventory        
@app.get("/inventory/")
async def view_inventory():
    try:
        conn = get_db()
        cursor = conn.cursor()
        

        
        # Main query to fetch inventory data for products with low stock
        query = """
  SELECT p.name AS product_name, i.stock_quantity, i.low_stock_threshold
        FROM Products p
        JOIN Inventory i ON p.product_id = i.product_id
        
          
    
        """
        
        cursor.execute(query)
        inventory_data = cursor.fetchall()
        cursor.close()
        conn.close()

       	return inventory_data
    except Exception as e:
        
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoints to update inventory levels

@app.get("/inventory/update-add/{product_id}")
async def update_product_quantity(
    product_id: int,
    quantity_diff: int
):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get current inventory quantity
        cursor.execute("SELECT stock_quantity FROM Inventory WHERE product_id = %s", (product_id,))
        current_quantity = cursor.fetchone()

        if current_quantity is None:
            raise HTTPException(status_code=404, detail="Product not found in inventory")

        # Calculate new stock quantity
        new_quantity = current_quantity[0] + quantity_diff

        # Update inventory quantity
        cursor.execute("UPDATE Inventory SET stock_quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": f"Inventory for product {product_id} updated successfully", "new_quantity": new_quantity}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.get("/inventory/update-subtract/{product_id}")
async def update_product_quantity(
    product_id: int,
    quantity_diff: int
):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get current inventory quantity
        cursor.execute("SELECT stock_quantity FROM Inventory WHERE product_id = %s", (product_id,))
        current_quantity = cursor.fetchone()

        if current_quantity is None:
            raise HTTPException(status_code=404, detail="Product not found in inventory")

        # Calculate new stock quantity
        new_quantity = current_quantity[0] -quantity_diff

        # Update inventory quantity
        cursor.execute("UPDATE Inventory SET stock_quantity = %s WHERE product_id = %s", (new_quantity, product_id))
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": f"Inventory for product {product_id} updated successfully", "new_quantity": new_quantity}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



# Endpoint to register a new product
@app.get("/products/{product_name}/{price}/{category_id}")
async def create_product(product_name: str, price: float, category_id: int):
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Insert new product into the Products table
        cursor.execute("INSERT INTO Products (name, price, category_id) VALUES (%s, %s, %s)",
                       (product_name, price, category_id))
        product_id = cursor.lastrowid
        conn.commit()

        cursor.close()
        conn.close()

        return {"message": "Product created successfully", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
