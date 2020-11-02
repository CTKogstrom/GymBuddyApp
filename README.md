# Virtual Environment Setup
In summary, you'll need to run the following 3 commands in the root directory to get set up
## Creating a virtual environment
```
python3 -m venv venv/ 
```
Don't add your venv folder to git, the directory remain untracked 
## Activating virtual environment
```
source venv/bin/activate
```
## Installing necessary packages to run project
```
pip install -r requirements.txt
```
Check this [link](https://towardsdatascience.com/virtual-environments-104c62d48c54) out for a more in depth explanation  
  In order to start the project, run this command:
```
python3 manage.py runserver
```
