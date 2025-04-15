# TravelLex - Travel Planning Platform

A modern web application for planning trips and exploring travel destinations.

## Project Structure

The project follows a standard Flask application structure:

```
travellex/
├── app.py                  # Main Flask application
├── wsgi.py                 # WSGI entry point for production
├── Procfile                # Heroku deployment configuration
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── css/                # CSS files
│   ├── js/                 # JavaScript files
│   ├── img/                # Images and graphics
│   └── vendor/             # Third-party libraries
├── templates/              # HTML templates
│   ├── index.html          # Main landing page
│   ├── login.html          # User login page
│   ├── register.html       # User registration page
│   └── plan-trip.html      # Trip planning functionality
└── .gitignore              # Git ignore file
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/travellex.git
cd travellex
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the application**

```bash
python app.py
```

5. **Access the website**

Open your browser and navigate to:
```
http://localhost:5000
```

## Features

- Beautiful responsive design 
- User registration and authentication
- Trip planning functionality
- Destination exploration
- Travel services showcase

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Backend**: Flask (Python)
- **Deployment**: Heroku-ready

## Deployment

This application is ready to be deployed on Heroku or any other platform that supports WSGI applications.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
