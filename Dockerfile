# Use the official lightweight Python image.
FROM python:3.9-slim
# Allow statements and log 
ENV PYTHONUNBUFFERED True
# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
# Install production dependencies.
RUN pip install -r requirements.txt
# Run
# CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app
# EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# deploy cmd
#gcloud builds submit --tag gcr.io/PROJECT-ID/countries_fastapi
# gcloud run deploy --image gcr.io/composed-garden-355604/ocr-fastapi --platform managed
