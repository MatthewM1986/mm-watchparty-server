Watch Party

Watch Party is an app where a user can select an upcoming sporting event and either create a watch party for that event or search for a watch party already created that they can join.

Getting Started
The following instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Python on Mac xcode-select --install

Pyenv and Python on Mac brew install pyenv pyenv install 3.9.1 pyenv global 3.9.1

Pipenv 3rd Party Tool pip3 install --user pipenv

Virtual Environment pip3 install --user pipx pipx install pipenv

Start Virtual Project pipenv shell

Third-Party Packages pipenv install django autopep8 pylint djangorestframework django-cors-headers pylint-django

Migrate data ./seed.sh

Start the Server python manage.py runserver