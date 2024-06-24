FROM python:3.11-slim

RUN mkdir /app

WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y tzdata && \
    pip install -r requirements.txt

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

LABEL version ="1.0"

EXPOSE 8501

CMD ["streamlit", "run", "Taximetro.py"]

