FROM python:3.10-slim

# Install MySQL client dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev pkg-config build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install werkzeug
RUN pip install "fastapi[standard]"

# Copy the rest of the application code
COPY . .

# Start the application
CMD ["fastapi", "run", "./application/main.py"]
