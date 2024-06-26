# REST API FOR AI CLINIC

# at http://0.0.0.0:8000/api/docs you will see documentation for all your endpoints. This is the default path to access 
the automatically generated API documentation in FastAPI.

# Start a project using Poetry:

1. Make sure you have Poetry installed. If not, install it with the following command:

https://python-poetry.org/docs/

2. Activate the Poetry virtual environment: 

poetry shell

3. In .env file specify your data for the configuration.

For example if u wanna use poetry - U need wirite DB_HOST = localhost and in another variable u need set up your data

4. Also u can see the certs dir. I didn't write this dir in .gitignore cos I generated for you private and public key 
for HASH_ALGORITHM = HS256 so if u wanna u can set up your secret key.

5. "Next, an important step before running my project involves Alembic for migrations and revisions. Here are the actions you can take:

If you want to apply the latest migration only, please run "alembic upgrade head".

If you want to start fresh with a new migration:

First, run "alembic downgrade base". This command clears all revisions.
Next, delete my revision from the versions directory.
Then, create your own revision with "alembic revision --autogenerate -m "your message here"".
Finally, apply the new revision with "alembic upgrade head".
If you encounter errors after running "alembic upgrade head", please create a new database as this issue is not related to my code."


6. Start the project:

/home/anton/.cache/pypoetry/virtualenvs/pythonproject-pflyVAO5-py3.10/bin/python /home/anton/flask_project/pythonProject/start.py


# Start a project using Docker Compose:

1. Install Docker and Docker Compose if they are not already installed.

https://docs.docker.com/compose/install/

2. Go to the root directory of the project (where locate docker-compose.yml).

3. In .env file specify your data for the configuration.

For example if u wanna use docekr - U need write DB_HOST = postgres and in another variable u need set up your data

4. Also u can see the certs dir. I didn't write this dir in .gitignore cos I generated for you private and public key 
for HASH_ALGORITHM = HS256 so if u wanna u can set up your secret key.

5. "Next, an important step before running my project involves Alembic for migrations and revisions. Here are the actions you can take:

If you want to apply the latest migration only, please run "docker-compose exec backend  upgrade head".

If you want to start fresh with a new migration:

First, run "docker-compose exec backend  alembic downgrade base". This command clears all revisions.
Next, delete my revision from the versions directory.
Then, create your own revision with "docker-compose exec backend alembic revision --autogenerate -m "your message here"".
Finally, apply the new revision with "docker-compose exec backend alembic upgrade head".
If you encounter errors after running "docker-compose exec backend alembic upgrade head", please create a new database as this issue is not related to my code."


6. Start the project using Docker Compose:

docker-compose up --build

Note: Before using Docker Compose, make sure you have Docker and Docker Compose installed on your system.


# Run tests:

So u need to go in test folder and after this just write in your console - "pytest"
I'm so sorry that i haven't written a lot of tests but i promise that i tested my project.
U can see that i test some endpoint with test_db and they work)

# API Endpoints

# SighUP:

Method: POST
Path: /auth/signup

Description: Signs up a new user.

Actions: Creates a new user in the database, generates access and update tokens, stores the update in the user session,
and returns the access tokens.

# Login:

Method: POST

Path: /auth/login

Description: Logs the user into the system.

Actions: Creates access and refresh tokens for an existing user, stores them in the user's session, and returns 
the access token.

# Refresh:

Method: POST

Path: /auth/refresh

Description: Refreshes the access token.

Actions: Checks the validity of the refresh token, retrieves user data from the token, creates a new access token, and returns it.

# Logout:

Method: GET

Path: /auth/logout

Description: Logs the user out of the system.

Actions: Removes access and update tokens from the user's session, terminates the current session.

Translated with DeepL.com (free version)


# GET /api/users/

Description: Get a list of all users.

Response: A list of users with their basic data.

# GET /api/users/me

Description: Get the data of the current authorized user.

Response: The data of the current user.

# PATCH /api/users/change/profile

Description: Change the profile of the current user.

Query Parameters: New profile data.

Response: Updated user data.

# POST /api/users/make/password_reset_token

Description: Create a token to reset the current user's password.
Response: Successful creation of a new password reset token.


# POST /api/users/reset_password

Description: Reset the current user's password.

Request parameters: New password.

Response: Successful execution of the password reset.

# DELETE /api/users/delete/me

Description: Delete the current user.

Response: Successful deletion of the user.

# GET /api/users/admin

Description: Get the data of the current authorized administrator.

Response: Current authorized administrator data.

# DELETE /api/users/delete

Description: Delete a user by name (administrator only).

Query Parameters: Name of the user to delete.

Response: Successful deletion of the user.


# POST /teams/create

Description: Create a new team.

Query Parameters: Data about the new team.

Response: Data about the created team.

# PUT /teams/update

Description: Update team data.

Query parameters: Updated team data.

Response: Updated team data.

# PATCH /teams/add_user

Description: Add a u to the team.

Query parameters: Update data (user and team).

Response: Updated team data with u.

# POST /teams/add_user_to_team

Description: Add a user to a team by username.

Query parameters: User name and team ID.

Response: Updated team data with users.

# PATCH /teams/remove_me

Description: Remove the current user from the team.

Query Parameters: Data to update (user and team).

Response: Updated team data with users.

# PATCH /teams/remove_user

Description: Remove the current user from the team by user ID.

Query parameters: User ID and team ID.

Response: Updated team data with users.

# DELETE /teams/delete_team

Description: Delete a team.

Query Parameters: The name of the team to delete.

Response: Status code 204 (Successful deletion).

# GET /teams/team/{team_name}

Description: Get team data by team name.

Query Parameters: Team name.

Response: Team data with users.

# GET /teams/teams

Description: Get a list of all teams.

Response: List of all teams with users.