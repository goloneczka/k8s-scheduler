FROM python:3.10
RUN pip install kubernetes
COPY . .
CMD ["python","-u","main.py"]