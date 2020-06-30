# Containerized API image:

FROM debian:latest

LABEL Author="Eli Harper"


RUN apt update && apt upgrade ; \
	apt install python3 python3-venv python3-pip git -y


RUN mkdir /app

WORKDIR /app/

# Add the program files and their supporting env info:
COPY ["./api.py", "./.env", "./env", "./application.py", "./requirements.txt", "/app/"]

RUN ls -la /app

# Start the virtualenv:
RUN cd /app && pip3 install -r ./requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

RUN ls -la /app ; pwd

EXPOSE 5001

RUN cd /app
# Run the program:
CMD [ "python3", "api.py" ]

