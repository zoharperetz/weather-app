FROM python:3.8
WORKDIR /weatherapp
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY ./ ./
EXPOSE 5000
CMD [ "python3", "app.py" ] 
#CMD gunicorn --bind 0.0.0.0:5000 app:app 

