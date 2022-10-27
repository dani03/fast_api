FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8000 

CMD ["uvicorn", "main:app", "--reload"]