# Lost & Found Portal

A Django-based Lost & Found Portal designed for college campuses that enables students to report, track, search, and manage lost or found items. The system provides secure user authentication, item reporting, status management, search and filtering capabilities, and an administrative dashboard for monitoring portal activity.

---

## Features

### User Authentication

* Student Registration
* Student Login
* Student Logout
* Session-based Authentication

### Lost & Found Management

* Report Lost Items
* Report Found Items
* Upload Item Images (Optional)
* Categorize Items
* Specify Lost/Found Locations
* Record Lost/Found Dates

### Report Tracking

* View Personal Reports
* View All Reports
* Update Item Status
* Track Recovery Progress

### Search & Filtering

* Search by Item Title
* Search by Description
* Filter by Category
* Filter by Location
* Filter by Status
* Filter by Report Type

### Administration

* Manage Users
* Manage Reports
* Search Reports
* Filter Reports
* Monitor Portal Activity

---

## Technology Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* JavaScript

### Database

* SQLite

### Media Handling

* Django Media Files

### Authentication

* Django Authentication System

---

## Project Structure

```text
Lost-and-Found-Portal/
│
├── config/
├── core/
├── templates/
├── screenshots/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Workflow

```text
Student Registration
        ↓
Student Login
        ↓
Dashboard
        ↓
Report Lost / Found Item
        ↓
Store Item Information
        ↓
View Reports
        ↓
Search & Filter Reports
        ↓
Update Status
        ↓
Recover / Hand Over Item
```

---

## Item Information Captured

Each report contains:

* Item Title
* Description
* Category
* Location
* Report Type (Lost / Found)
* Event Date
* Status
* Optional Image
* Reporter Information

---

## Item Status Flow

### Lost Items

```text
Open
 ↓
Recovered
```

### Found Items

```text
Open
 ↓
Given Away
```

---

## Categories

Examples include:

* Mobile Phones
* Laptops
* Earphones
* Chargers
* Wallets
* Keys
* Watches
* Umbrellas
* Student ID Cards
* Aadhaar Cards
* Books
* Bags
* Water Bottles
* Other

---

## Locations

Examples include:

* Library
* Food Court
* Hostel
* Academic Block A
* Academic Block B
* Parking Area
* Bus Stop
* Other

---

## Installation

### Clone Repository

```bash
git clone https://github.com/jani-rose/lost-and-found-portal.git
cd lost-and-found-portal
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Screenshots

Screenshots of the application interface can be found in the `screenshots` directory.

Suggested screenshots:

* Home Page
* Registration Page
* Login Page
* Dashboard
* Report Item Form
* My Reports
* All Reports
* Search & Filters
* Admin Dashboard

---

## Future Enhancements

* Similar Item Matching
* Email Notifications
* Advanced Search
* Dashboard Analytics
* Improved UI/UX
* Responsive Design
* Automated Recovery Suggestions

---

## Author

Jani Rose Lawwellman


