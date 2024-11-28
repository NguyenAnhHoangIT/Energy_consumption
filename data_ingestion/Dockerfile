FROM python:latest

# Install required Python packages
RUN pip install mysql-connector-Python

RUN pip install requests
# Set the working directory inside the container
WORKDIR /data_ingestion

# Copy the contents of the local data folder into the container
COPY . /data_ingestion/


