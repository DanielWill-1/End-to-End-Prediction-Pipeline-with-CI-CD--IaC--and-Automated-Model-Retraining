# Stage 1: Use an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file *first* to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of your application code into the container
# This includes the 'app' folder and the 'artifacts' folder
COPY ./app /code/app
COPY ./artifacts /code/artifacts

# Expose the port the API will run on (FastAPI default is 8000)
EXPOSE 8000

# Define the command to run your API when the container starts
# uvicorn app.main:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]