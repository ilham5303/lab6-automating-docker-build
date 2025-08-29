# Step 1: Choose a base image with Python
FROM python:3.9-alpine

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
# Explanation: We copy requirements.txt and install Python libraries.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the rest of the application code
# Explanation: Copy app.py and the templates folder into the container.
COPY . .

# Step 5: Expose the port the Flask app will run on
EXPOSE 5000

# Step 6: Define the command to run the Flask application
CMD ["python", "app.py"]

