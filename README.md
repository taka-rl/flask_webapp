# About
This is a web app where I have been utilizing gained skills and knowledge in Flask, Database, RESTful API and Python while learning them by myself.

## Stacked tech
- Python
- Flask
- HTML/CSS/Bootstrap
- Flask-WTF/WTForm
- SQLite
- Flask-Login

## Preparation to use
1. Run the following command for the libraries:
   
   On Windows type:
   ```python -m pip install -r requirements.txt```  
   On MacOS type:
   ```pip3 install -r requirements.txt```

2. Create API Keys if you would like to use "Useful Information function" in the useful_info.html.  
   OpenWeather API: https://openweathermap.org/api  
   ExchangeRate API: https://www.exchangerate-api.com/

3. Get an App password if you would like to use Email sender function in contact.html  
   
4. Create .env file including the following variables:
   ```
   SQLALCHEMY_DATABASE_URI=sqlite:///XXXXX.db  # Database
   SECRET_KEY=Type Your Secret Key  # Flask Secret Key
   WEATHER_API_KEY = 'Replace Your API Key set at 2'  # OpenWeather API
   ExchangeRate_API_KEY = 'Replace Your API Key set at 2'  # ExchangeRate API
   MYEMAIL = 'Your Email Address set at 3'
   EMAIL_PASSWORD = 'App Password set at 3'
   ```


## Design
### Database
The ERD is as follows:  
![image](https://github.com/user-attachments/assets/68e1780e-5b8a-4942-bcf1-afad40384a81)


## Current development:  
- Store my favorite cafes in the database(SQLAlchemy)
- Show you the weather information through OpenWeather API
- Get the currency exchange rate between JPY and HUF through ExchangeRate API
- Add pages such as Blog posts, hobby, contact, about, register/login/logout
- Show some posts/create a post
- Add register/login/logout function
- Design database considering Place, BlogPost, User and Comment
- Add user authentication function for adding/editing/deleting places (only admin can)

## Future development:
- Improve the web page design
- Make sure all the functionality
- Introduce a chatbot
- Deploy the web page
