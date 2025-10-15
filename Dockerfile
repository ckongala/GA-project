FROM python:3.10.9
WORKDIR /src
COPY src /src
COPY .env /src/.env
COPY requirements.txt /src
COPY swagger.json /src
RUN pip install --upgrade -r requirements.txt
RUN apt-get update && apt-get install libgl1 -y
RUN apt-get install -y ffmpeg
EXPOSE 5001
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]