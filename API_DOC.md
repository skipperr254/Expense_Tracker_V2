# Expense Tracker API Documentation

Welcome to the Expense Tracker API documentation. This document provides an overview of the available API endpoints, their functionality, and how to use them when building the frontend of our application.

## Table of Contents

1. [API Endpoints](#api-endpoints)
2. [Authentication](#authentication)
3. [API Usage](#api-usage)

## 1. API Endpoints

### Categories

#### Global Categories

- `GET /api/global-categories/`
  - Description: Retrieve a list of all global expense categories.
  - Usage: Fetch global categories to display in dropdowns for expense categorization.

- `POST /api/global-categories/`
  - Description: Create a new global expense category.
  - Request Body:
    ```json
    {
        "name": "Category Name"
    }
    ```
  - Usage: Add custom global categories (Admin only).

#### User-Specific Categories

- `GET /api/user-categories/`
  - Description: Retrieve a list of user-specific expense categories.
  - Usage: Fetch user-specific categories to display in dropdowns for expense categorization.

- `POST /api/user-categories/`
  - Description: Create a new user-specific expense category.
  - Request Body:
    ```json
    {
        "name": "Category Name"
    }
    ```
  - Usage: Allow users to add their custom categories.

### Income Tracking

- `GET /api/incomes/`
  - Description: Retrieve a list of income records for the authenticated user.
  - Usage: Fetch user's income history to display on the dashboard.

- `POST /api/incomes/`
  - Description: Create a new income record for the authenticated user.
  - Request Body:
    ```json
    {
        "amount": 1000.0,
        "source": "Income Source"
    }
    ```
  - Usage: Record user's income.

### Expense Management

- `GET /api/expenses/`
  - Description: Retrieve a list of expense records for the authenticated user.
  - Usage: Fetch user's expense history to display on the dashboard.

- `POST /api/expenses/`
  - Description: Create a new expense record for the authenticated user.
  - Request Body:
    ```json
    {
        "amount": 100.0,
        "description": "Expense Description",
        "category": 1  # Use category ID or leave blank for uncategorized expenses
    }
    ```
  - Usage: Record user's expenses.

## 2. Authentication

- To access the API, you need to include an "Authorization" header in your requests.
- Use Token Authentication with the token provided during user registration or login.

## 3. API Usage

- Make HTTP requests to the specified endpoints as per your frontend requirements.
- Use the appropriate HTTP methods (GET, POST, PUT, DELETE) for CRUD operations.
- Include request data in JSON format in the request body, where necessary.
- Review the API endpoints' specific documentation for more details.

Feel free to reach out if you have any questions or need further assistance with integrating the API into the frontend of our application.
