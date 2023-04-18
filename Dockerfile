FROM python:3.9

WORKDIR /api

# Install dependencies
COPY ./app/requirements.txt /api/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /api/requirements.txt

# Copy source
COPY ./app /api/app

# Run (for single start without docker-compose)
#CMD ["python3", "/api/app/main.py"]
