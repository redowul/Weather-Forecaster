## Requirements

Create a basic weather app using Django web framework. Requirements:

-   Users can enter any US address and get daily high/low temperature forecast for the next 5 days.
-   Set up an API connection to bring in weather data from any open weather API.
-   All views/forms/etc. should have tests.

---

## INSTRUCTIONS TO RUN:

1. Go to openweathermap.org and sign up to receive an API key. You'll need one for this application to work!
2. cd to /backend and, using pip, enter "pip install -r requirements.txt" to install all required python packages this
   project uses.
3. cd into /backend and enter "python manage.py runserver"
    - Django should now be running at the following URL: "http://127.0.0.1:8000/"
4. Using NPM package manager, enter "npm i axios" ; this is what the frontend uses to communicate with the backend.
5. In a different terminal window, cd into /frontend and enter "npm run start"
    - React should now be running at the following URL: "http://localhost:3000/"

Enjoy!
