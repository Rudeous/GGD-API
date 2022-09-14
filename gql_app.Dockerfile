FROM python:3.8.5-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY seed_db.py model.py schema.py helper.py db.py ./
# RUN python seed_db.py
# after running seed_db.py, copy created database.sqlite3 file to /app
# COPY database.sqlite3 ./
COPY gql_app.py .
CMD ["python", "gql_app.py"]