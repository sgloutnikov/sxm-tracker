FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8080

CMD ["python3", "sxm_collect.py"]
