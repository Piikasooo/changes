# changes_in_exchange_rates

deploy project on your local machine:

1 - To deploy project on your local machine create new virtual environment and execute this command:

pip install -r requirements.txt

2 - Rename example.env to .env and change config.

3 - Migrate db models to PostgreSQL:

python3 manage.py migrate

4 - Run app:

python3 manage.py runserver
