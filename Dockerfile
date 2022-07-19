FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV APP_HOME /app

WORKDIR $APP_HOME
COPY . ./

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN pip install -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --timeout 0 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app

# deploy cmd
#gcloud builds submit --tag gcr.io/composed-garden-355604/ocr_fastapi
# gcloud run deploy --image gcr.io/composed-garden-355604/ocr-fastapi --platform managed