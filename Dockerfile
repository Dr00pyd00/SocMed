
FROM python:3.14-slim


# empeche les .pyc inutile en container ( inutile )
ENV PYTHONDONTWRITEBYTECODE=1

# empeche le buffering comme ca les logs sont ecrits directs
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY requirements.txt .
# pas de cache: moins encombrant
RUN pip install --no-cache-dir  -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

COPY . .
# CMD ["gunicorn","config.wsgi:application","--bind","0.0.0.0:8000","--reload"]
CMD ["./entrypoint.sh"]


