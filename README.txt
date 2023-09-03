Basic information regarding the program.

In the folder you will find a python scripth called logic.py. This is what you you need to excecute in order to run the program.

The code in logic is for a Flask web application that interacts with a SQLite database to store and retrieve information about elements and reactions.
Here's a breakdown of the key components and what you'll need to execute it:

1) Flask Installation: Flask is a web framework for Python. Before running the code, you need to have Flask installed.

2) SQLite Database: The code interacts with an SQLite database named "Reactions_DB.db". Ensure you have SQLite installed, which is a built-in library in Python and doesn't require separate installation.

3) Running the Application:

	Make sure you run the requirements.txt file before running the app. It will install the necessary modules to launch the app. You can do it by using
	"pip install requirements.txt".

	The code creates a Flask app instance with the name app. It defines several routes using the @app.route decorator. These routes define the URLs that 	the application can handle. The main routes include /, /input, /reactioninput, and /results, each corresponding to different functionality in the 	application. The if __name__ == "__main__": block at the end of the code ensures that the Flask development server is started only when the script is 	executed directly, not when it's imported as a module.

4) Templates: The application uses HTML templates to render views. The templates are expected to be in a folder named templates in the same directory as your script. The templates include files like "Reaction_identifier.html", "Input.html", "Reaction_Input.html", and "results.html".

5) SQL Queries: The application uses SQL queries to interact with the SQLite database. It performs INSERT and SELECT operations to store and retrieve data related to elements, reactions, gamma, and x-ray values.

6) Rendering Templates: The "render_template" function is used to render HTML templates with data passed from the Python code.

7) The Flask development server will start, and you can access the application in a web browser by navigating to http://localhost:5000.

UPDATING THE DATABASE:

	The different excel files function as the csv files needed to create the original database. The database can be updated in three ways. From the csv files directly by updating those and executing the base.py file. This will update the database with the changes made to the csv files. Make sure that the information you are trying to input does not exist in the databse, otherwise it will create multiple copies of the same information, leading to the presentations of redundant results. You can update five different tables: Elements, Gamma, XRAY, REACTIONS and CROSS SECTION. Each has different information that are related to each other through queries in logic.py. To have a overview of all the elements in the database and the different tables you can use a viesualiser such as "BD Browser", where you can directly input the data in columns of the different tables. This can fucntion as another way to input data. Make sure to follow the format of the other inputs as it is necessary in order to present the data in the application. Lastly in the database page has two links that redirect the user to two different pages. One to input elements and one to input reactions.

NOTE: You cant enter two elements with the same name, for example you cant enter two times 54Fe. I will try to make so it can detect if the element exist and give an error message but for now there needs to be caution in the input of elements in the database. 

INFORMATION ON THE DIFFERENT ASPECTS OF THE ALSO EXIST IN THE CODE ITSELF TO BETTER EXPLAIN THE DIFFERENT FUCNTIONS.



