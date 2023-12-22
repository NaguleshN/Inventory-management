FROM python:3.11

WORKDIR /inventory

RUN mkdir static

COPY requirements.txt /inventory/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /inventory/

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]