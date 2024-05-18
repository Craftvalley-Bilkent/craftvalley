FROM python:3.12

ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /craftvalley

# Install dependencies
COPY requirements.txt /craftvalley/
RUN pip install -r requirements.txt

# Copy project files
COPY . /craftvalley/