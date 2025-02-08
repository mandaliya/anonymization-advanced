# Use official lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port for Streamlit
EXPOSE 8080

# Command to run the application
CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0