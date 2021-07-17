Django Rest Framework API
================================
This is Python REST API that calls an external API service to get information about books. Additionally, it implements a simple CRUD (Create, Read, Update, Delete) API with a local sql database.

Compatibility
-------------
This project is developed and tested with `python3.8`

Prerequisites
-------------
In order to set up this project, make sure you have python's `pip` package installed on your system.


Makefile
---
The project adds a make file for running most common commands. These commands
should be run inside the virtualenv.

Getting Started
---------------
1. Clone the Repo in your local machine.

       git clone https://github.com/awaisdar001/Django-DRF-API.git

2. Create a python3 virtualenv and activate it.

       python3 -m venv ~/venvs/pjvenv
       source ~/venvs/pjvenv/bin/activate

3. Install requirements inside of the virtual env
   
       make requirements

4. Run migrations and set up the database locally.
   
       make update_db

8. Run the development server
   
       make dev.up

| Service             | URL                                       |
| -------------       | -------------                             |
| Outcode Endpoint    | http://localhost:9000/api/outcode/M28/    |
| Nearest to Outcode  | http://localhost:9000/api/nexus/M28/      |



