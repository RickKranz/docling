# Dockerfile

# 1. Start with an official Python base image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy all your project files into the container
COPY . .

# 4. Run the Dockling installation using the method we know works
RUN pip install -e .

# 5. Install the web server components
RUN pip install fastapi uvicorn[standard]

# 6. Expose the port the server will run on
EXPOSE 8080

# 7. Define the command to run when the container starts
# This tells uvicorn to run the 'app' object from the 'main.py' file
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
