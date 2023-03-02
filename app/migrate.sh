# Script to autogenerate alembic revision and apply it to db
alembic revision --autogenerate -m "$1" 
alembic upgrade head