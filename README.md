# GymBuddy
## GitHub Link
Link to GitHub repo - https://github.com/CTKogstrom/GymBuddyApp

## Project Description
GymBuddy is a web application for anyone who is committed to pursuing a healthier lifestyle. GymBuddy helps the user keep track of the numerous aspects of their lives: through logging macros, calories, exercises, meals, and weight. The information is tracked over time and portrayed in the form of graphs to visually display the progress you have made over time.

**Sidenote: We have the backend working where you can save exercises and meal recipes into the database, and also be able to filter and search through both exercises and meal recipes in the database, but could not get it working with pypy. Therefore, it will not be a part of this submission.

## Product Release

### Install Dependencies
```
pip install GymBuddy
```
```
launch migrate
```
```
launch from server
```

## Git Clone Set Up
In summary, you'll need to run the following 3 commands in the root directory to get set up
### Creating a virtual environment
```
python3 -m venv venv/ 
```
Don't add your venv folder to git, the directory remain untracked 
### Activating virtual environment
```
source venv/bin/activate
```
### Installing necessary packages to run project
```
pip install -r requirements.txt
```
Check this [link](https://towardsdatascience.com/virtual-environments-104c62d48c54) out for a more in depth explanation  
  In order to start the project, run this command:
```
python3 manage.py runserver
```
