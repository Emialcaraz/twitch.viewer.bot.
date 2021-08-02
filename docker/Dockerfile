FROM python:3.8.5-slim-buster

RUN apt update -y
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
WORKDIR /workspace/
COPY requirements/requirements.txt ./
RUN pip install -r requirements.txt
ARG INSTALL_DEV=false
COPY ./src/ ./

CMD ["python", "main.py"]
