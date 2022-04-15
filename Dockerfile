FROM python:3.10
RUN apt-get update && apt-get install -y iputils-ping
RUN pip install kubernetes
COPY . .
CMD ["python","-u","main.py"]