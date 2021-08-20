FROM python:3-slim

RUN mkdir -p /custom
WORKDIR /custom

COPY ./requirements.txt /custom/requirements.txt
RUN pip install -r requirements.txt
COPY ./push_service.py /custom

CMD [ "python" , "push_service.py"]