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
1. Make sure the config_name as an argument of create_app function in main.py  
      ```app = create_app(config_name='development')```  
   Since it is still under development, 'production' has not been supported yet.

2. Run the following command for the libraries:  
   On Windows type:
   ```python -m pip install -r requirements.txt```  
   On MacOS type:
   ```pip3 install -r requirements.txt```

3. Create API Keys if you would like to use "Useful Information function" in the useful_info.html.  
   OpenWeather API: https://openweathermap.org/api  
   ExchangeRate API: https://www.exchangerate-api.com/

4. Get an App password on Google if you would like to use email sender function in contact.html  
   How to create App password → https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237?hl=ja

5. Create .env file including the following variables:
   ```
   SECRET_KEY=Type Your Secret Key  # Flask Secret Key
   WEATHER_API_KEY = 'Replace Your API Key set at 2'  # OpenWeather API
   ExchangeRate_API_KEY = 'Replace Your API Key set at 2'  # ExchangeRate API
   MYEMAIL = 'Your Email Address set at 3'  
   EMAIL_PASSWORD = 'App Password set at 3'
   SUPER_ADMIN = 'admin@email.com'  # The SUPER_ADMIN is the one that can change user's role such as admin and user and delete users.
   ```
6. Run main.py
7. Use one of the accounts written as below to Login
- Super admin user:  
   email: admin@email.com  
   password: admin  
- user:     
   email:test@email.com  
   password: test@email.com
8. Register a new user

9. Change user's role on ('/admin-dashboard') route.



## Design
### Directory structure
    ├── instance                # database file
    ├── static                  # static files
    │   ├── assets              # img files
    │   ├── css                 # css file related to bootstrap
    │   ├── js                  # js file related to bootstrap
    │   └── translations        # language json files
    ├── templates               # route html files
    ├── tests                   # tests
    │   ├── conftest.py         # set up for testing
    │   ├── test_auth.py        # test for auth routes
    │   └── other routes        # will be committed later
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
    │       ├── admin.py        # Admin routes
    │       └── useful_info.py  # Useful_info-related routes
    ├── main.py                 # Run the app
    ├── .gitignore
    ├── Procfile                 
    ├── requirements.txt
    └── README.md

### Database
The ERD is as follows:  
![image](https://github.com/user-attachments/assets/9d89c929-c464-4739-babe-ab8b95710c22)


### User Role
There are three roles:  
Super admin:
- It is the one set the email on .env file as "SUPER_ADMIN".
- It can switch user's role such as admin and user and delete users on ('/admin-dashboard') route.
- It also contains admin features.  

Admin:
- It can post a new post/place, edit a post/place and delete a post/place.
- It can comment on posts.

User: 
- When you register, the user role is user.
- It can see the web page
- It can comment on posts.


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
- Add functions to change user role and delete users by admin
 
## Current development
- Testing
- Documentation
- Add github actions, which is python-app.yml to execute pytest

## Future development:
- Improve the web page design
- CI/CD pipelines
- Introduce a chatbot
- Deploy the web page


## Testing
The section will be updated as it is under development.  
pytest-flask is used for testing.
