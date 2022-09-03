FROM python:3.9-slim-bullseye


# Set enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERD=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set work directory
WORKDIR /usr/src/app

# copy the dependencies file to the working directory
COPY ./requirements.txt /usr/src/app/requirements.txt

# install python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY ./advertising_board /usr/src/app


