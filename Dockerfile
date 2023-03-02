FROM python:3.9

WORKDIR /api

# Install dependencies
COPY ./app/requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

# Copy source
COPY ./app /api/app

# Import env vars
# Hardcoded
#CMD ["source", "/api/app/.env"]

ENV ITC_DATABASE_URL="postgresql://root:root@db:5432/itc_system"
ENV ITC_SERV_PORT=8080
ENV ITC_SERV_HOST="0.0.0.0"
ENV ITC_SECRET_KEY="hasyadyfysdyfsdfsdu723772s"
ENV ITC_ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENV ITC_USERS_STORAGE="/api/app/static/users_data/uploads/"
ENV ITC_API_VER="0.0.2"


# Run
#CMD ["python3", "/api/app/main.py"]

