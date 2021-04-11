#Project Setup

- Install `python3.8` (If not already present)
- Install pip first
    : RUN `sudo apt-get install python3-pip`
- Then install virtualenv using pip3
    : RUN `sudo pip3 install virtualenv`
- Create "virtual environment" on the machine for the project
    :RUN `python3 -m venv virtual_environment_name`
- Activate virtual environment.
    :RUN `source virtual_environment_name/bin/activate`
- Run `pip install -r requirements.txt` to configure a python virtual environment for the project and install the requirements.
- To final check application is successfully setup or not
    : RUN `python manage.py runserver`
