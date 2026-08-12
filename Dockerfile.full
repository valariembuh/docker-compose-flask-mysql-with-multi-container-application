FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
COPY templates/ templates/
CMD ["python", "app.py"]
EXPOSE 5000
