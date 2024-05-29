# Using basic python
FROM python:3.11

# Set work directory
WORKDIR /app

# Copy in container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Open the port for flask
EXPOSE 5000

# Define command to lauch the application
CMD ["python", "app.py"]
