# Recommendation-System
A recommendation system

To run the application: Do the following to make it run on you machine
Run:
1)      python install requirement.txt # This installs all the dependencies for the application to work fine
2)      python run.py db init          # This will add a migrations folder to your application
3)      python run.py db migrate       # This is to check for changes in the model and create the database schema
4)      python run.py db upgrade       # This effect the changes to the dataase 

After the above commands, Run the below to start the application: 
python run.py runserver --port = 8081 --debug #to run the application.
 