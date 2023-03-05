FROM python:3.10

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends &&  \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "-p", "8000"]
