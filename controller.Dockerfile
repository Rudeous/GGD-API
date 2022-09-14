FROM python:3.8.5-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY controller.py seed_db.py model.py schema.py helper.py db.py ./
COPY templates ./templates
CMD ["python", "controller.py"]