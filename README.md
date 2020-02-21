# changes_in_exchange_rates

deploy project on your local machine:

1 - To deploy project on your local machine create new virtual environment and execute this command:

    pip install -r requirements.txt

2 - In terminal: 

    sudo -su postgres psql
    create database db_name;
    create user user_name;
    grant all privileges on database db_name to user_name;

3 - Rename example.env to .env and change config.

4 - Migrate db models to PostgreSQL:

    python3 manage.py migrate

5 - Run app:

    python3 manage.py runserver
