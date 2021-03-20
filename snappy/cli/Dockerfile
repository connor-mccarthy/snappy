FROM public.ecr.aws/lambda/python:3.7

RUN pip install --upgrade pip 

COPY . .

RUN pip install -r requirements.txt

CMD [ "app.handler" ]