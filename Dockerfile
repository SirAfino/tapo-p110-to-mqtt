FROM python:3.9.18-bullseye

RUN pip install git+https://github.com/almottier/TapoP100.git@main
RUN pip install paho-mqtt
RUN pip install asyncio
RUN pip install pyyaml

WORKDIR /usr/src/app
COPY *.py .

ENTRYPOINT [ "python", "script.py" ]
