FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /project/main
COPY . .
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 5000
CMD ["python", "./manage.py"]
