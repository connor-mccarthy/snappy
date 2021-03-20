FROM public.ecr.aws/lambda/python:3.7

RUN pip install --upgrade pip

RUN yum upgrade -y && yum install git -y

COPY . .

RUN pip install -r requirements.txt

CMD [ "app.handler" ]