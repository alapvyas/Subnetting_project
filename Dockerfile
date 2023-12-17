# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Copy requirements file
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["python3"]

CMD ["subnetting.py"]