FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /src

RUN apt-get update  \
    && apt-get install --no-install-recommends --no-install-suggests -y \
    curl \
    gpg \
    git

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip  \
    && pip install -r requirements.txt

COPY /src .

EXPOSE 5000

CMD bash -c "python main.py"
