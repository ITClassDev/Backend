FROM python:3.11

WORKDIR /api

# Install dependencies
COPY ./requirements.txt /api/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /api/requirements.txt
# Copy source
COPY ./. /api/

# Remove following shit later
# Delete migrations
# RUN rm -r /api/migrations/versions/*.py
# Delete all migrations
# RUN alembic -c /api/app/alembic_docker.ini revision --autogenerate -m 'Init' 
# RUN alembic init alembic
# RUN alembic -c /api/app/alembic_docker.ini upgrade head
# RUN "rm -r /api/app/alembic/versions/* && && alembic -c /api/app/alembic_docker.ini upgrade head"
# Run (for single start without docker-compose)
#CMD ["python3", "/api/app/main.py"]
