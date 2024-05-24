# Django Application with PostgreSQL and Celery

This repository contains a Django application configured to use PostgreSQL as the database backend and Celery for background task processing using Redis as the message broker.

## Prerequisites

Before running the application, ensure you have the following dependencies installed:

- Python
- PostgreSQL
- Redis

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   ```

2. **Navigate to the project directory:**

   ```bash
   cd <project_directory>
   ```

3. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Create a `.env` file:**

   Create a `.env` file in the project directory and configure the following environment variables:

   ```plaintext
    DATABASE_NAME=socialmedia
    DATABASE_USER=brutalrayuser
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    
    # sender email creds
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=testemail@gmail.com
    EMAIL_HOST_PASSWORD=testpass
    EMAIL_RECIPIENTS=email1@gmail.com,email2@gmail.com,email3@gmail.com
   ```

   Replace with your actual values.

2. **Update `settings.py`:**

   Update `settings.py` to load environment variables for Django and Celery configurations.
   ```plaintext
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   ```
## Migrations
1. ```bash
   python manage.py makemigrations
   ```
2. ```bash
   python manage.py migrate
   ```

## Usage

1. **Run the Celery worker:**

   ```bash
   celery -A hotstuff worker -l info -B
   ```

2. **Run the Django application:**

   ```bash
   python manage.py runserver
   ```

3. **Access the application:**

   Access the application in your web browser at `http://localhost:8000`.
