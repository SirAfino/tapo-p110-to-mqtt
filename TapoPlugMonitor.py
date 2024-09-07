import json
from PyP100 import PyP110
import paho.mqtt.client as mqtt
from TapoLogger import logger
import asyncio

# In seconds
DEFAULT_SCAN_INTERVAL = 5

class TapoPlugMonitor():
    _id: str
    _ip: str
    _username: str
    _password: str
    _scan_interval: int
    _plug: PyP110.P110
    _mqtt_client: mqtt.Client
    _mqtt_topic: str

    def __init__(self, id, ip, username, password, mqtt_client, mqtt_topic, scan_interval=DEFAULT_SCAN_INTERVAL):
        self._id = id
        self._ip = ip
        self._username = username
        self._password = password
        self._mqtt_client = mqtt_client
        self._mqtt_topic = mqtt_topic
        self._scan_interval = scan_interval
        self._plug = PyP110.P110(self._ip, self._username, self._password)
        logger.debug("{0}: Created".format(self._mqtt_topic))

    def connect(self):
        try:
            self._plug.login()
            return True
        except Exception as e:
            logger.error("{0}: Login error {1}".format(self._mqtt_topic, e))
            return False

    async def run(self):
        logger.info("{0}: Trying to connect...".format(self._mqtt_topic))
        while not self.connect():
            await asyncio.sleep(60)
        logger.info("{0}: Connected".format(self._mqtt_topic))

        while True:
            try:
                while not self.connect():
                    await asyncio.sleep(60)
                data = self._plug.getEnergyUsage()
                logger.debug("{0}: Publishing data {1}".format(self._mqtt_topic, data))
                self._mqtt_client.publish(self._mqtt_topic, json.dumps(data))
            except:
                pass
            
            await asyncio.sleep(self._scan_interval)
