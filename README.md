# Scalora – Online Appointment Scheduling & Business Support Platform

A full-stack Django web application with authentication, booking system,
ebook store, blog, careers, testimonials, dashboards, and email notifications.

---

## ⚡ Quick Start (5 Minutes)

### 1. Create & Activate Virtual Environment
```bash
python -m venv venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
# OR use the pre-seeded admin:
#   Username: admin
#   Password: admin123
```

### 5. Seed Demo Data (optional but recommended)
The app ships with a seed script — paste into `python manage.py shell`:
```python
# Run: python manage.py shell < seed_data.py
# Or run migrations from a fresh db — demo data is auto-seeded via shell command
```

### 6. Collect Static Files (production)
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## 🔑 Pre-Seeded Credentials

| Role  | Username | Password  | Access                      |
|-------|----------|-----------|-----------------------------|
| Admin | `admin`  | `admin123`| Full admin dashboard        |
| Client| Register at `/accounts/register/` | Any | Client dashboard |

---

## 📧 Configure Email (Gmail)

Edit `scalora_project/settings.py`:

```python
EMAIL_HOST_USER     = 'your-gmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-16-char-app-password'  # Google App Password
ADMIN_EMAIL         = 'admin-notifications@yourdomain.com'
DEFAULT_FROM_EMAIL  = 'Scalora <your-gmail@gmail.com>'
```

To generate a Gmail App Password:
1. Go to Google Account → Security → 2-Step Verification → App Passwords
2. Create a password for "Mail" on "Other device"
3. Paste the 16-character password above

---

## 🗂️ Project Structure

```
scalora/
├── scalora_project/       # Core settings, URLs, main views
│   ├── settings.py
│   ├── urls.py
│   └── views.py           # Home + About pages
│
├── accounts/              # Auth: register, login, logout, profile
├── services/              # Service CRUD + admin schedule / availability API
├── bookings/              # Appointment booking, cancellation, status update
├── testimonials/          # Client testimonials
├── blogs/                 # Blog posts with slugs
├── careers/               # Job postings
├── ebooks/                # eBook store + orders + receipts
├── dashboard/             # Admin & client dashboards
│
├── templates/             # All Django HTML templates
│   ├── base.html          # Public site base (navbar + footer)
│   ├── home.html          # Landing page with 3D hero
│   ├── about.html
│   ├── accounts/          # Login, register, profile
│   ├── bookings/          # Booking form with live slot picker
│   ├── services/
│   ├── blogs/
│   ├── careers/
│   ├── ebooks/            # Store, detail, order, receipt
│   ├── testimonials/
│   └── dashboard/
│       ├── base_dashboard.html
│       ├── admin/         # Admin: overview, bookings, services, blogs, etc.
│       └── client/        # Client: overview, bookings, orders
│
├── static/
│   ├── css/
│   │   ├── scalora.css    # Full design system (glassmorphism + 3D)
│   │   └── dashboard.css  # Dashboard-specific styles
│   └── js/
│       ├── scalora.js     # Animations, tilt effects, counter
│       └── hero3d.js      # Three.js particle field background
│
├── media/                 # User-uploaded files (avatars, covers, blog images)
├── requirements.txt
├── manage.py
└── db.sqlite3             # SQLite database (auto-created)
```

---

## 🌐 URL Map

| URL                        | View                              |
|----------------------------|-----------------------------------|
| `/`                        | Home (landing page)               |
| `/about/`                  | About page                        |
| `/accounts/register/`      | User registration                 |
| `/accounts/login/`         | Login                             |
| `/accounts/logout/`        | Logout                            |
| `/accounts/profile/`       | Edit profile (login required)     |
| `/services/`               | Services listing                  |
| `/services/add/`           | Add service (admin)               |
| `/services/<id>/edit/`     | Edit service (admin)              |
| `/services/api/slots/`     | JSON: available time slots        |
| `/bookings/book/`          | Book appointment (login required) |
| `/bookings/<id>/cancel/`   | Cancel booking (owner)            |
| `/bookings/<id>/status/`   | Update status (admin)             |
| `/testimonials/`           | Testimonials page                 |
| `/testimonials/add/`       | Add testimonial (admin)           |
| `/blogs/`                  | Blog listing                      |
| `/blogs/<slug>/`           | Blog detail                       |
| `/blogs/add/`              | New blog post (admin)             |
| `/careers/`                | Job listings                      |
| `/careers/<id>/`           | Job detail                        |
| `/careers/add/`            | Post job (admin)                  |
| `/ebooks/`                 | eBook store                       |
| `/ebooks/<id>/order/`      | Order ebook (login required)      |
| `/ebooks/order/<id>/receipt/`| Download receipt               |
| `/dashboard/`              | Auto-redirect by role             |
| `/dashboard/admin/`        | Admin overview                    |
| `/dashboard/admin/bookings/`| Manage all bookings              |
| `/dashboard/admin/services/`| Manage services + schedule      |
| `/dashboard/client/`       | Client overview                   |
| `/dashboard/client/bookings/`| My appointments                |
| `/dashboard/client/orders/`| My ebook orders                  |

---

## 🎨 Design System

**Colors:**
- Primary Dark: `#0F1E40`
- Primary: `#1B3673`
- Primary Light: `#4A5D8A`
- Gold Accent: `#c9b37e`
- Secondary: `#8C92AC`

**Typography:**
- Display: Playfair Display (headings, brand)
- Body: DM Sans (all copy)

**UI Patterns:**
- Glassmorphism cards with blur backdrop
- 3D tilt hover effects on cards
- Three.js animated particle hero background
- Scroll-triggered reveal animations
- Counter animations on statistics

---

## 🔒 Security Features

- `@login_required` on all booking, order, and dashboard views
- CSRF protection on all forms
- Staff/admin role checks on all CRUD operations
- Password hashing via Django's built-in PBKDF2
- Double-booking prevention at model + form level

---

## 📦 Deployment Checklist

```python
# settings.py changes for production:
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-strong-random-secret-key-here'

# Use PostgreSQL:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scalora_db',
        'USER': 'scalora_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Serve media files via nginx/S3 in production
```

Install additional production deps:
```bash
pip install gunicorn psycopg2-binary whitenoise
```

Run with gunicorn:
```bash
gunicorn scalora_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```
