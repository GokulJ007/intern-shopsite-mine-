# 🛍️ Shopping Store (FakeDB E-Commerce)

A full-stack, role-based e-commerce platform built using **FastAPI** for the backend, **Streamlit** for the frontend, and a **MySQL** database. It includes a custom LLM-powered AI customer assistant chatbot that dynamically translates natural language customer queries into safe MySQL commands to perform inventory and order lookups.

---

## 🚦 Terminal Quick Start Guide

Run the following commands in your terminal to set up, migrate, and start the application.

### 1. Database Setup
Create a MySQL database named `fakedb` (configured on port `3030` by default). Run these queries in your MySQL shell:
```sql
CREATE DATABASE IF NOT EXISTS fakedb;
USE fakedb;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) DEFAULT NULL,
    role VARCHAR(50) DEFAULT 'user'
);

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    image_url VARCHAR(500) DEFAULT NULL,
    category VARCHAR(100) DEFAULT NULL
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    delivery_status VARCHAR(50) DEFAULT 'Pending',
    delivery_person_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (delivery_person_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
```

### 2. Environment Configuration
Create a `.env` file in the project root folder with the following configuration:
```env
GROQ_API_KEY="your_groq_api_key"
XAI_API_KEY="your_xai_api_key"

DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="your_mysql_password"
DB_NAME="fakedb"
DB_PORT=3030
```

### 3. Installation, Migrations, & Seeding
Open your terminal in the project root directory:
```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (Add columns for passwords, categories, images, and delivery status)
python migrate_db.py
python migrate_delivery.py
python migrate_users_db.py

# Seed the database with 50 products
python seed_products.py
```

### 4. Running the Servers
Ensure the virtual environment is activated, then launch both servers:

* **Terminal 1: Start FastAPI Backend**
  ```bash
  uvicorn backend.main:app --reload --port 8000
  ```
* **Terminal 2: Start Streamlit Frontend Client**
  ```bash
  streamlit run frontend/app.py
  ```

*Note: For local development, open [frontend/app.py](file:///c:/Users/tojay/OneDrive/code/Desktop/intern/fetchapi/frontend/app.py) and change `API_URL` (line 12) from `https://shopsite-streamlit.onrender.com` to `http://localhost:8000`.*

---

## 👥 Role-Based Workflow Guide

Here is a step-by-step walkthrough of how each section of the application operates:

### 1. 🛒 User (Customer) Workflow
This portal allows customers to register, browse products, purchase items, and query catalog data using natural language.
* **Sign Up / Log In**: 
  - Navigate to the frontend page, click **"Register here"** to create a new user profile (Name, Email, Password). 
  - Log in using the **User Portal** form with your name and password.
* **Shopping & Checking Out**:
  1. Under the **Shop** tab, browse products. Use the search bar, price slider, or select a category filter (e.g. *Electronics*, *Fashion*, *Beauty*, *Home and Kitchen*).
  2. Select a quantity and click **"Add to Cart"**.
  3. Go to the **Cart** tab to review your items, change quantities, or click **"Checkout"** to place the order.
* **Tracking Deliveries**:
  - In the **Orders** tab, view all of your past orders. You will see a breakdown of products, prices, and the live **Delivery Status** (e.g., *Confirmed*, *Out for Delivery*, *Delivered*).
* **AI Support Assistant (Chatbot)**:
  - Scroll to the bottom of the User Portal to find the chat interface.
  - Ask questions naturally (e.g., *"Show me all beauty products under $20"* or *"Are any products out of stock?"*). The assistant routes your request to a MySQL query, executes it safely, and answers you in natural language.

---

### 2. 🚚 Delivery Personnel Workflow
This portal allows delivery drivers to check their delivery queues, verify ordered products, and update order statuses.
* **Accessing the Portal**:
  - Click on **"Delivery Personnel Portal"** at the login screen.
  - Log in using your driver username and password (e.g., username: `Delivery Person 1`, password: `1234`).
* **Managing Assigned Tasks**:
  1. Once logged in, you will see the **"Your Assigned Deliveries"** screen. Click **"Refresh Deliveries"** to check for new orders.
  2. Look at each assigned order block. It shows the customer's name, email, date, and a complete table of products and quantities to be packaged.
  3. Change the order status along the route:
     - Click **"Mark Out for Delivery"** when leaving the store (changes status: `Confirmed` ➔ `Out for Delivery`).
     - Click **"Mark Delivered"** when the package reaches the customer (changes status: `Out for Delivery` ➔ `Delivered`).

---

### 3. 📊 Manager Workflow
This section enables managers to manage the inventory catalog, adjust pricing, and restock products.
* **Accessing the Panel**:
  - Log in using your manager credentials through the **Manager Portal** (accessible from the link in the login form).
* **Catalog Management**:
  1. Click on the **"Manager Panel"** tab at the top.
  2. Select **"👥 Manage Users"** to view user accounts and managers registered in the store.
  3. Select **"📝 Manage Products"** to view all catalog items.
     - Expand any product block to view its stock and pricing details.
     - Update the **Price ($)**, **Stock Quantity**, or **Product Category**.
     - Modify the product image: paste a web URL, upload a new image from your PC, or remove the image.
     - Click **"Save"** to apply changes or **"Delete"** to remove the product from the catalog.

---

### 4. 👨‍💼 Admin Workflow
This dashboard provides complete control over users, product catalogs, order files, and system promotions.
* **Accessing the Panel**:
  - Log in using administrative credentials via the **Admin Portal** link.
* **Platform Administration**:
  1. Click on the **"Admin Panel"** tab.
  2. **👥 Manage Users**: 
     - View a complete list of users, roles, and ID numbers.
     - Promote a standard user to a new role (e.g. promoting them to `manager`, `delivery_person`, or `admin`).
     - Delete user profiles entirely.
  3. **🔍 View All Orders**: 
     - Audit all order tickets created across the store, including totals, customer details, and delivery statuses.
  4. **➕ Add Product**:
     - Fill in Name, Price, and Stock.
     - Choose an image method: *Auto-suggest stock image* (generates a beautiful context-relevant photo), *Provide Web URL*, or *Upload from computer*.
     - Click **"Add Product"** to register it in the live store database.
  5. **📝 Manage Products**:
     - Full edit and delete permissions for all active products.