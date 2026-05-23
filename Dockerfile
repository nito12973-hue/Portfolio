FROM python:3.12-slim AS base

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "portfolio_project.wsgi:application", "--bind", "0.0.0.0:8000"]
