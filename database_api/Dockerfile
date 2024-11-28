FROM python:latest

# Install required Python packages
RUN pip install mysql-connector-Python

RUN pip install requests
# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the local data folder into the container
COPY . /app/

# Command to run the application
CMD ["python", "api.py"]
