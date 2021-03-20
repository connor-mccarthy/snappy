FROM public.ecr.aws/lambda/python:3.7

RUN pip install --upgrade pip 

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

CMD [ "app.handler" ]