FROM python:3.12.7-slim

WORKDIR /api

COPY ./ /api

RUN pip3 install -r requirements.txt

CMD ["fastapi", "run", "/api/main.py", "--host", "0.0.0.0", "--port", "80"]
