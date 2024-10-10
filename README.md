# AODMS
Annual Oil Data Management System

This project provides an API that calculates annual oil, gas, and brine production data for wells based on quarterly data, stores this information in a local SQLite database, and allows users to query this data via a Flask API.

#Features

**Quarterly Data Summation**: The script sums up quarterly production data (oil, gas, brine) for each well based on its API well number and calculates the annual production.

**Data Population**: 

	Method-1 : Python scripts are provided to populate this data into an SQLite database.
	Method-2 : And also you can use  '/insert_data' api to populate data using flask app
	
**API Endpoints**:

GET '/data?well=': Returns the annual oil, gas, and brine production for a specific well number.



#Setup Instructions
**Clone the repository**:

	git clone git@github.com:mathewjoseph2811/AODMS.git

**Create a virtual environment**:

	python3 -m venv flask_env
	source flask_env/bin/activate   
	
**Install the required dependencies**:

	pip install -r requirements.txt
	requirements.txt file is attached in the project directory
	
#Run the Flask API:

Start the Flask server by running:

	python main.py
	
	This will start the Flask API on http://localhost:8080
	
#Usage Example:
**For database and table creation and populate excel data to table**:

	http://localhost:8080/insert_data
	
	Or you can populate using the script upload_annual_data_script.py by running python 
		python upload_annual_data_script.py
		
		
**For fetching data based on well number**:

	http://localhost:8080/data?well={well number}
	
	Eg:
		http://localhost:8080/data?well=3405924254000015
		
		
		


