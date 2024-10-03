# About
This is a Flask web app example where I have been utilizing gained skills and knowledge in Flask, sqlalchemy, RESTful API and Python while learning them by myself.

## Stacked tech
- Python
- Flask
- HTML/CSS/Bootstrap
- Flask-WTF/WTForm
- sqlalchemy
- PosgreSQL (for deploy)
- Flask-Login
- Jinja


## Preparation to use
1. Run the following command for the libraries:
   
   On Windows type:
   ```python -m pip install -r requirements.txt```  
   On MacOS type:
   ```pip3 install -r requirements.txt```

2. Create API Keys if you would like to use "Useful Information function" in the useful_info.html.  
   OpenWeather API: https://openweathermap.org/api  
   ExchangeRate API: https://www.exchangerate-api.com/

3. Get an App password on Google if you would like to use email sender function in contact.html  
   How to create App password → https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237?hl=ja

4. Create .env file including the following variables:
   ```
   SQLALCHEMY_DATABASE_URI=sqlite:///posts.db  # Database
   SECRET_KEY=Type Your Secret Key  # Flask Secret Key
   WEATHER_API_KEY = 'Replace Your API Key set at 2'  # OpenWeather API
   ExchangeRate_API_KEY = 'Replace Your API Key set at 2'  # ExchangeRate API
   MYEMAIL = 'Your Email Address set at 3'
   EMAIL_PASSWORD = 'App Password set at 3'
   ```
5. Run main.py
6. Use one of the accounts written as below to Login
- admin user:  
   email: admin@email.com  
   password: admin  
- non admin user:     
   email:test@email.com  
   password: test@email.com  
Note: You can register a new account but admin user is the admin as the id of User is 1 .


## Design
### Directory structure
    ├── instance                # database file
    ├── static                  # static files
    │   ├── assets              # img files
    │   ├── css                 # css file related to bootstrap
    │   ├── js                  # js file related to bootstrap
    │   └── translations        # language json files
    ├── templates               # route html files
    ├── flask_app               
    │   ├── __init__.py         # Initialize Flask app and extensions
    │   ├── forms.py            # Forms
    │   ├── models.py           # Database models
    │   ├── utils.py            # Utility functions such as decorators, email sender
    │   └── route               
    │       ├── about.py        # About-related routes
    │       ├── auth.py         # Auth-related routes
    │       ├── blog.py         # Blog-related routes
    │       ├── collection.py   # Collection-related routes
    │       ├── contact.py      # Contact-related routes
    │       ├── others.py       # Other (language switcher)
    │       └── useful_info.py  # Useful_info-related routes
    ├── main.py                 # Run the app
    ├── .gitignore
    ├── Procfile                 
    ├── requirements.txt
    └── README.md

### Database
The ERD is as follows:  
![image](https://github.com/user-attachments/assets/68e1780e-5b8a-4942-bcf1-afad40384a81)


## Finished development:  
- Store my favorite cafes in the database(SQLAlchemy)
- Show you the weather information through OpenWeather API
- Get the currency exchange rate between JPY and HUF through ExchangeRate API
- Add pages such as Blog posts, hobby, contact, about, register/login/logout
- Show some posts/create a post
- Add register/login/logout function
- Design database considering Place, BlogPost, User and Comment
- Add user authentication function for adding/editing/deleting places (only admin can)
- Add a send_email function in the contact.html
- Add a language switcher
- Organize main.py (See Directory structure)
- Add Error handling

## Current development
- Testing
- Documentation

## Future development:
- Improve the web page design
- CI/CD pipelines
- Add functions to add/delete users by admin
- Introduce a chatbot
- Deploy the web page
