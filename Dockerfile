# Use the official Python runtime image
FROM ghcr.io/astral-sh/uv:python3.14-alpine

# Create the app directory
RUN mkdir /app

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Copy the Django project to the container
COPY . /app/

RUN uv sync

# Expose the Django port
EXPOSE 8000

# Run Django’s development server
CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
