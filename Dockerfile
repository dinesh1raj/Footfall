FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install opencv dependencies
RUN apt-get update -y && apt-get install -y gcc
RUN apt-get install -y libgl1 libglib2.0-0
RUN apt-get install build-essential -y

# Install python dependencies
RUN pip install wheel cmake
RUN pip install -r requirements.txt

# Make port 8001 available to the world outside this container
EXPOSE 8002

# Define environment variable
ENV NAME footfall

# Run app.py when the container launches
CMD ["python3","main.py"]