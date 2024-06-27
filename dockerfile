# Using basic python
FROM python:3.11.9

# Set work directory
WORKDIR /app

# Copy requirements.txt first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Open the port for Flask
EXPOSE 5000

USER root

# Define the command to launch the application
CMD ["python", "app.py"]