# Select the base image that is best for our application
FROM python:3

# Install any operating system junk
# why don't we need this?

# Set the working directory to copy stuff to
WORKDIR /app

# Copy relevant code from the local directory into the image
COPY accounts accounts
COPY attendees attendees
COPY common common
COPY conference_go conference_go
COPY events events
COPY presentations presentations
COPY requirements.txt requirements.txt
COPY manage.py manage.py

# Install any language dependencies
RUN pip install -r requirements.txt

# Set the command to run the application
CMD gunicorn --bind 0.0.0.0:8000 conference_go.wsgi

# CMD gunicorn conference_go.wsgi
# Your Django app is now running inside another virtual computer
# It starts up and reports Listening at: http://127.0.0.1:8000
# The application is only listening to the local computer inside the virtual computer
# We're making a request with Insomnia from a whole different computer!
