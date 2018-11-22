FROM python:3.6.6

# Add catalog web-app
ADD . /catalog

# Change to working directory
WORKDIR /catalog

# Environment varialble
ARG DB_URL
ARG PIPENV_CONFIG

ENV DATABASE_URL=$DB_URL
ENV PIPENV_VENV_IN_PROJECT=$PIPENV_CONFIG

# Install package
RUN git clone https://github.com/vishnubob/wait-for-it.git /wait-for-it

RUN pip3 install uwsgi pipenv && pipenv install

EXPOSE 3031
