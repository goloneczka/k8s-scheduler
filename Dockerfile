FROM python:3.10-alpine
RUN pip install kubernetes
COPY scheduler.py /scheduler.py
CMD python /scheduler.py