## 🍽 "Жрачка топ" Check Printing Service

The renowned "Жрачка топ" delivery restaurant chain now introduces a modern approach to streamline the check generation process for both our valued customers and diligent kitchen staff. This service not only aids in generating these checks but ensures a seamless experience.

---

### 📋 Features

- **Order Processing**: On receiving a new order, checks are created for all the printers at the specified point.
- **PDF Generation**: Asynchronous tasks will generate PDF files for these checks.
- **Order Validation**: If an order is duplicated or a point lacks a printer, appropriate error messages are returned.
- **Efficient Polling Mechanism**: A programmatic approach to request a list of receipts for a specific printer, followed by PDF download and printing.

---

### 🛠 Technical Stack

- **Programming Language**: Python
- **Web Framework**: Django
- **Database**: PostgreSQL
- **PDF Generation**: `wkhtmltopdf` docker container

---


### 🛠 Setup & Installation
### For windows

1. **Clone the Repository:**
    ```
    git clone https://github.com/yourusername/priesttop-check-service.git
    cd priesttop-check-service
    ```
   
2. **Set Up Environment Variables**:
    ```
   cp .env.example .env
    ```
3. **Launch Docker Services**:
    ```
    docker-compose up -d
    ```
4. **Virtual environment activation:**
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
5. **Install Python Dependencies:**
    ```
    pip install -r requirements.txt
    ```
6. **Initialize the Database:**
    ```
    python manage.py migrate
    ```
7. **Load Initial Data:**
    ```
    python manage.py loaddata printer_fixtures.json
    ```
8. **Run the Server:**
    ```
    python manage.py runserver
    ```
---


© 2023 Жрачка топ. All Rights Reserved.