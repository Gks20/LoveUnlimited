# Love Unlimited - Non-Profit Management System

A public-facing Django website for Love Unlimited non-profit organization.

## 🌟 Features

### Public Frontend
- **Homepage** with mission statement and upcoming events
- **About Us** page with organization information
- **Events Calendar** with public event listings and registration
- **News & Updates** for announcements and past event write-ups
- **Community Resources** page with public support information
- **Donation Page** with Zeffy integration for secure donations
- **Contact Information** and volunteer opportunities
- **Spanish / English** language switcher
- **Responsive Design** for mobile and desktop users

### Staff CMS (Staff Portal)
- Manage events, registrations, posts, site content, resources, and donation settings at `/staff/`

## 📁 Project Structure

```
LoveUnlimited/
├── loveunlimited/          # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── frontend/              # Public website app
├── calendar_app/          # Event data used by the public calendar
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project** to your local machine

2. **Create a virtual environment:**
   ```bash
   py -m venv .venv
   ```

3. **Activate the virtual environment:**
   - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
   - Windows (cmd): `.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`

4. **Install dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

5. **Create environment file:**
   Create a `.env` file in the root directory with:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

6. **Run database migrations:**
   ```bash
   python manage.py migrate
   python manage.py bootstrap_site
   ```

7. **Create a staff account:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - Public site: http://127.0.0.1:8000/
   - Staff portal: http://127.0.0.1:8000/staff/

### Tests

Run the test suite:

```bash
python -m pytest
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
```

### Zeffy Integration
To integrate Zeffy for donations:

1. Create an account at [Zeffy.com](https://zeffy.com)
2. Create a donation form
3. Get the embed code from Zeffy
4. Replace the placeholder in `templates/frontend/donate.html` with your Zeffy form

### Green Geeks Deployment
For deployment on Green Geeks hosting:

1. Update `ALLOWED_HOSTS` in settings.py with your domain
2. Set `DEBUG = False` for production
3. Configure static files serving with WhiteNoise (already included)
4. Update database settings if using PostgreSQL instead of SQLite

## 📊 Database Models

### Events & Calendar
- **Event**: Manage public and private events
- **EventCategory**: Organize events by type
- **EventRegistration**: Track event registrations

### Community Resources
- **ResourceCategory**: Organize public resource listings
- **Resource**: Publish addresses, hours, phone numbers, and links for local help

## 🛡️ Security Features

- Django's built-in security features
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password validation

## 📱 Mobile Responsive

The entire application is built with Bootstrap 5 for mobile-first responsive design, ensuring a great experience on all devices.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support with this application:
- Check the Django documentation: https://docs.djangoproject.com/
- Review the code comments and docstrings
- Contact the development team

## 📝 License

This project is created for Love Unlimited non-profit organization. Please respect the organization's mission and use this code responsibly.

## 🚀 Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Update `SECRET_KEY` with a secure value
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL/HTTPS
- [ ] Configure static files serving (run `collectstatic`, confirm hashed filenames)
- [ ] Compile translation messages (`django-admin makemessages -l es` then `compilemessages`)
- [ ] Test language switch by appending `?lang=es` or setting `Accept-Language`
- [ ] Set up backup procedures
- [ ] Test all functionality
- [ ] Configure monitoring and logging

## 📈 Future Enhancements

Potential features for future development:
- Volunteer management system
- Mobile app for field workers
- Multi-language support

---

Built with ❤️ for Love Unlimited Non-Profit Organization
