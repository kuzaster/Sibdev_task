# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.8.3-alpine

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# create root directory for our project in the container
RUN mkdir /sibdev_app

# Set the working directory to /sibdev_app
WORKDIR /sibdev_app

# Copy the current directory contents into the container at /sibdev_app
ADD . /sibdev_app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt