FROM python:3.9
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
EXPOSE 8080
CMD ["poetry", "run","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]