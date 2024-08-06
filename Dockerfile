FROM python:3.9.6

WORKDIR /api_todo

COPY ./requirements.txt /api_todo/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api_todo/requirements.txt

COPY ./src /api_todo/src

CMD ["fastapi", "run", "src/main.py", "--port", "80"]