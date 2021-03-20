FROM public.ecr.aws/lambda/python:3.7

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y git-all

COPY . .

RUN pip install -r requirements.txt

CMD [ "app.handler" ]