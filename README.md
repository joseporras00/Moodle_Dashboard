# Moodle Dashboard

This web application allows visualize data of students, differents graphs and also you can create and train predictions model to use for future students.

Built with Python and Dash, this application will provide users an in-depth look at Moodle's data.

Dash is an open-source Python framework that is used for building data visualization applications - this application offers a useful, interactive platform for teachers wich use Moodle. 

The application will be divided into four pages:

* Home
* Dashboard
* Train Model
* Predict

## Home
The Home page will display:

* A upload component to upload the file for dashboard and train model pages
* A table with the data uploaded

## Dashboard
This page will feature interactive graphs about the students' marks and other variables, also you can filter each graph with the number of the course you want to study. Then you could see a correlation matrix and the importance of the variables of the dataset.

## Train Model
The train model page will allow you to create a prediction model:

* Train and test size
* Select target and independent variables
* Select kfold splits
* Select the type of the model
* Results

## Predict
The predict page will show the prediction of a file uploaded in a table. Then you could download it as a CSV file.

## Running The Script

In order to access the application, open up Terminal and make sure to change the working directory to exactly where you saved this folder:

* Create a virtual environment and activate it
* Run __pip install -r requirements.txt__
* Run __python3 index.py__ on Terminal
* Your app will be accesible on any web browswer at the address: 127.0.0.1:8050

## Built With
* [Dash](https://dash.plot.ly)

## Authors
* [Jose Manuel Porras](https://github.com/joseporras00)


