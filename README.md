# UMAMS – University of Mpumalanga Asset Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x%2B-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Educational%20%2F%20Organizational-lightgrey)](#license)

**UMAMS** is a web-based asset management system created to help universities and similar institutions track, assign, maintain, and report on physical assets with improved accountability and transparency.

The system supports barcode generation, real-time camera-based barcode scanning, staff–asset assignment, PDF reporting with Matplotlib graphs, and automated email notifications.

## ✨ Key Features

- **Asset Management**  
  Register, update, view and track assets (name, serial number, barcode, status, location, assignment history)

- **Staff / User Management**  
  Add staff members, assign/unassign assets, view per-person asset lists

- **Barcode Generation & Printing**  
  One-click bulk barcode generation (using `python-barcode`)  
  Download / print-ready barcode images

- **Camera Barcode Scanning**  
  Instant asset lookup using device camera (powered by **html5-qrcode**)

- **Reporting & Analytics**  
  PDF exports with tables and graphs  
  Monthly performance overview (Matplotlib bar/line charts)  
  Staff–asset assignment summaries

- **Email Notifications**  
  Automated alerts (new assignment, return reminder, etc.) via SMTP

- **Secure Authentication**  
  Django built-in auth + role-based access (admin, technician, viewer)

## 🏗 System Architecture

Modular Django application layout:

umams/
├── administration/     # Core asset logic, dashboards, reports
├── auth_app/           # Custom user & login handling
├── staff/              # Staff profiles & asset assignment
├── technician/         # Maintenance / repair logging
├── notification/       # Email sending logic
├── homepage/           # Public landing & documentation pages
├── static/             # CSS, JS, images
├── templates/          # Base & app-specific templates
└── manage.py

## 🛠 Technologies Used

| Layer         | Technology                          |
|---------------|-------------------------------------|
| Backend       | Python • Django                     |
| Frontend      | HTML • CSS • JavaScript • Bootstrap |
| Barcode       | python-barcode                      |
| Scanning      | html5-qrcode (browser camera)       |
| Graphs        | Matplotlib                          |
| PDF           | (likely xhtml2pdf / weasyprint)     |
| Database      | SQLite (dev) • PostgreSQL (prod rec.) |
| Static files  | WhiteNoise                          |
| Deployment    | Heroku / Railway / Render / VPS     |

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.10+
- Git
- Virtualenv / venv

### Steps

1. **Clone repository**

```bash
git clone https://github.com/YOUR-USERNAME/umams.git
cd umams

Create & activate virtual environment

bash

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

Install dependencies

bash

pip install --upgrade pip
pip install -r requirements.txt

Apply migrations & create superuser

bash

python manage.py migrate
python manage.py createsuperuser

Run development server

bash

python manage.py runserver

Open →  http://127.0.0.1:8000/Default login: the superuser you just created Screenshots<!-- You can replace these with real images later -->

Dashboard
DashboardBarcode Scanning
ScannerAsset Report Example
Report Configuration – Email SetupEdit umams/settings.py:python

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your.email@gmail.com"
EMAIL_HOST_PASSWORD = "your-16-char-app-password"   # ← App Password, not normal password
DEFAULT_FROM_EMAIL = "UMAMS <your.email@gmail.com>"

Tip: Use Gmail App Passwords (2FA must be enabled). Production Deployment NotesSwitch to PostgreSQL
Set DEBUG = False
Configure ALLOWED_HOSTS
Use environment variables for secrets (python-decouple / django-environ recommended)
Collect static files: python manage.py collectstatic
Consider gunicorn + whitenoise or a proper web server

 LicenseThis project is provided for educational and organizational (non-commercial) use by University of Mpumalanga and associated parties. AuthorFortune Ben
Project Manager & Full-Stack Developer
 Python | Django | Web Applications | Asset Management SystemsFeel free to open issues or submit pull requests.Made with  for better institutional asset visibility & accountability.

### Recommendations / Optional Improvements

1. Replace `FortuneBenn` with your actual GitHub username
2. Add real screenshots (create a `screenshots/` folder)
3. Consider adding badges for build status, coverage, etc. if you add CI later
4. Add a small **Contributing** section if you want collaborators
5. Use environment variables library → mention in README
6. Add `.env.example` file with dummy values

This version is more GitHub-friendly, looks professional, and gives quick value to anyone landing on the repo.

Good luck with the project! 🚀
