# Excellent CRM

An **Excellent Customer Relationship Management (CRM)** application built with **Django** to streamline customer interactions and sales processes. It offers a **modern, intuitive interface** and powerful automation features.

---

## 🚀 Features

- **Multi-Factor Authentication (MFA)** for enhanced security 🔐  
- **Customizable Sales Forms** – Users can design and modify form fields dynamically  
- **Email Notifications** – Stay updated with automated email alerts  
- **User Roles & Permissions** – Assign sales agents and manage contacts effectively  
- **Modern UI/UX** – A responsive, clean interface for seamless interactions  

---

## 🛠 Installation

Clone the repository and install dependencies including geospacial Libraries:

```bash
git clone https://github.com/elliot-hacks/ExcellentCRM.git
cd ExcellentCRM
pip install -r requirements.
sudo apt-get install binutils libproj-dev gdal-bin
```
For any errors on Geospacial libraries check Django documentation [GIS](https://docs.djangoproject.com/en/5.1/ref/contrib/gis/install/geolibs/)

Install google-auth pip libraries
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```


Run migrations:

python manage.py makemigrations
python manage.py migrate

Start the development server:

python manage.py runserver

⚙️ Configuration

    Set up environment variables in .env:

    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    EMAIL_HOST_USER=your_email@example.com
    EMAIL_HOST_PASSWORD=your_password

    Configure SMTP for email notifications in settings.py.


🤝 Contributing

Contributions are welcome! for Excellent Team

    Fork the repo
    Create a new branch (feature-xyz)
    Commit changes
    Submit a Pull Request

📄 License

This project is licensed under the MIT License. See LICENSE for details.
📧 Contact

For queries, reach out via excellence@gmail.com.

🚀 Start managing your customers efficiently with Excellent CRM!


---
