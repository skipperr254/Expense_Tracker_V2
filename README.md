# Expense Tracker Web App

## Introduction

The Expense Tracker Web App is a web-based application built with Django and Django Rest Framework (DRF) that allows users to manage their expenses, track income, and categorize their spending. This README provides an overview of the project, instructions for installation and usage, and other essential information.

- **Demo**: [Expense Tracker Web App Demo](https://your-expense-tracker-app-demo.com)
- **Author**: [Your Name](https://www.linkedin.com/in/your-linkedin-profile/)
- **Final Project Blog Article**: [Read the Blog Article](https://your-blog-article-link.com)

## Installation

To set up the Expense Tracker Web App locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/expense-tracker-web-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd expense-tracker-web-app
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Perform database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser account to access the admin panel:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

9. Access the web app at `http://127.0.0.1:8000/` in your web browser.

## Usage

- **User Registration**: Register a new user account to start using the app.
- **User Login**: Log in with your registered account to access the app's features.
- **User Dashboard**: View your income summary, total expenses, remaining income, and expense breakdown by category.
- **Expense Management**: Add, update, and delete your expenses, categorizing them as needed.
- **Income Tracking**: Record your income sources to keep track of your financial inflow.
- **Category Management**: Manage global categories available to all users and create custom categories for personal use.

## Contributing

Contributions are welcome! If you would like to contribute to the Expense Tracker Web App, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and test thoroughly.
4. Commit your changes and create a pull request.
5. Provide a clear and descriptive pull request title and description.

## Related Projects

Here are some related projects that may interest you:

- [Frontend Repository](https://github.com/yourusername/expense-tracker-frontend): The frontend part of the Expense Tracker web app.

## Licensing

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.