# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

RUN apt-get update;apt-get upgrade -y 
RUN apt-get install -y python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN apt-get install -y libguestfs-tools python3-guestfs
RUN apt-get install -y python3-tk
RUN mkdir /app

WORKDIR /app

#COPY ../requirements.txt /app/
COPY ../ /app/

RUN pip install -r requirements.txt

#COPY ../ /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
