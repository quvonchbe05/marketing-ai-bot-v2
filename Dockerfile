FROM python:3.9

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /marketing_bot

WORKDIR /marketing_bot

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh

