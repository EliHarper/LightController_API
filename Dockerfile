# Containerized API image:

FROM debian:latest

LABEL Author="Eli Harper"


RUN apt update && apt upgrade ; \
	apt install python3 python3-venv python3-pip git -y


RUN mkdir -p /app/env
RUN mkdir /app/log

WORKDIR /app/

# Add the program files and their supporting env info:
COPY ["./*", "/app/"]
COPY ["./env/", "/app/env/"]

RUN ls -la /app

# Start the virtualenv:
RUN cd /app && \
	pip3 install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org && \
	pip3 install --upgrade google-api-python-client  --trusted-host pypi.org --trusted-host files.pythonhosted.org && \
	pip3 install -r ./requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org


EXPOSE 5001

RUN cd /app ; ls -l /app && . /app/env/bin/activate
ENV PYTHONPATH /app
# Run the program:
CMD [ "python3", "api.py" ]

