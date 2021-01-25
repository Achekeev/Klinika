FROM python:3.8
#RUN pip install pipenv
ENV PYTHONUNDUFFERED 1
WORKDIR /klinika
#COPY Pipfile Pipfile.lock ${PROJECT_DIR}/
#RUN pipenv install --system --deploy
COPY requirements.txt ./
RUN pip3 install django-cors-headers
RUN pip3 install -r requirements.txt

