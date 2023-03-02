FROM python:3.9

WORKDIR /api

# Install dependencies
COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY ./ /api/app
CMD ["python3", "main.py"]

