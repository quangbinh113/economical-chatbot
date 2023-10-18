# Use the official Python 3.10 Slim image as the base image
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    python3-dev \
    gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
RUN pip install python-multipart
COPY . .
RUN chmod +x start_backend.sh
CMD ["bash", "./start_backend.sh"]