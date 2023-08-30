alembic downgrade base
alembic stamp base
alembic revision --autogenerate -m "$1" 
alembic upgrade head

# 
# 
# alembic -c alembic_docker.ini revision --autogenerate -m 'Init'
# alembic -c alembic_docker.ini upgrade head