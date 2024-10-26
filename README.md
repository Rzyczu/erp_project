
# ERP Project

A Django-based ERP (Enterprise Resource Planning) system designed to manage and automate various business processes, including finance, inventory, human resources, and more.

## Demo live

https://erp-django-project.onrender.com/

## Features

- **User Registration and Authentication**: Users can create accounts and log in to the system.
- **Team Management**:
  - After logging in, users can create a new team or join an existing team using its unique 6-digit ID.
  - Each team is assigned a random 6-digit identifier for easy identification.
  - The user who creates a team automatically becomes its Project Manager (PM).
  - When joining a team, users can select their role within the team.
- **Project and Task Management**:
  - Project Managers (PMs) can create projects within their team.
  - For each project, tasks can be created, assigned, and tracked.
  - Tasks have various statuses to indicate progress and can be assigned to any team member.
- **Team Composition Management**: The Project Manager has the authority to manage the team's composition, including assigning or changing roles of members.
- **Profile Management**: Users can update their personal details through the profile settings in the menu.
"""

## Project Structure

- `erp_app/`: Main application code, including models, views, and templates.
- `erp_project/`: Django project settings and configurations.
- `db.sqlite3`: SQLite database file for development and testing.
- `static/`: Static files like JavaScript, CSS, and images.
- `manage.py`: Django management script for running the server, migrations, etc.

## Detailed Functionality of `erp_app`

The `erp_app` is a core module of the ERP system, responsible for managing various aspects of business processes. Below is a detailed description of the application's functionality:

### Main Components

- **Models (`models.py`)**:
  - Define the structure of the data stored in the database. This may include models related to user management, products, invoices, orders, and other key business entities.
  - Models are the basis for automatic form generation and the admin panel.

- **Views (`views.py`)**:
  - Handle the application's logic, processing HTTP requests and passing data to templates.
  - Example views include:
    - Displaying lists of products, customers, orders.
    - Detailed views of individual entities, such as order details.
    - Handling the creation and editing of data through forms.

- **Forms (`forms.py`)**:
  - Contain Django forms for validating and processing user-input data.
  - Enable the creation, editing, and deletion of records such as products, customers, or orders.

- **Decorators (`decorators.py`)**:
  - Custom decorator functions that can restrict access to certain resources based on user roles (e.g., admin, staff).
  - Allow for easy addition of authorization logic to views.

- **Context Processors (`context_processors.py`)**:
  - Functions that add global variables to the template context, making them available in every view.
  - Useful for adding data like global app settings or dynamic menu elements.

- **Admin Panel (`admin.py`)**:
  - Registers models with Django's admin panel, enabling data management directly from the admin interface.
  - May include custom configurations such as displaying additional columns or filtering data.

### URL Structure (`urls.py`)

- Maps various views to URLs, allowing for navigation through the application.
- Supports creating user-friendly URLs for specific features, such as viewing order lists or editing products.

### Templates (`templates/`)

- Contain HTML files rendered by views.
- Used to display data attractively and provide the user interface for different features.
- Example templates include product lists, order forms, and reports.

### Custom Template Tags (`templatetags/`)

- Extend Django templates' capabilities by adding new tags or filters.
- Useful for processing data directly in templates, allowing for better control over data presentation.

### Migrations (`migrations/`)

- Store database migration files that are generated automatically as models change.
- Enable easy management of database schema changes and are an integral part of managing the application's data.

### Tests (`tests.py`)

- Contains unit tests for the application, ensuring that each functionality works as expected.
- Tests may include validation of forms, views, and model functions.

## Getting Started

### Prerequisites

- Python 3.8+
- Django 4.x
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd erp_project
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   Access the project at `http://127.0.0.1:8000/`.

## Usage

1. Log in using the admin credentials you set up.
2. Navigate through the modules like Inventory, Finance, and Reports.
3. Add, update, or delete records as needed.

## Contributing

Contributions are welcome! To get started:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

## Screens

![image](https://github.com/user-attachments/assets/74a6aedb-59a1-4824-a218-d9e70fc0d7ab)
View of landing page

![image](https://github.com/user-attachments/assets/c0e8cd18-50e9-4c41-a0fd-add9b7a99f54)
View of dashboard 

![image](https://github.com/user-attachments/assets/bd3005ff-ffbf-4ad9-82e0-9ee4a0bdd5c8)
View of team named "team test 1" on project manager account

![image](https://github.com/user-attachments/assets/333d2e47-4083-4186-adc7-52c79e6eb0c5)
View of team named "team test 1" on others users account

![image](https://github.com/user-attachments/assets/e14cc9e8-2392-465a-85ed-f87aecac1f61)
View of project page

![image](https://github.com/user-attachments/assets/97a04df7-a6d4-4b4d-9767-8963f549cd0d)
View of task detail


## License

This project is licensed under the terms of the LICENSE file.
