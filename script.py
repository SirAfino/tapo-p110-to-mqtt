import paho.mqtt.client as mqtt
import asyncio
import yaml
from TapoLogger import logger
from TapoPlugMonitor import TapoPlugMonitor

APP_NAME = "Tapo to MQTT"

def loadConfig(path):
    config = None
    logger.debug('Loading configuration from: ' + path)
    try:
        with open(path, "r") as file:
            config = yaml.safe_load(file)
            logger.debug('Configuration loaded')
    except Exception as e:
        logger.error("Invalid configuration file: " + e)
    return config


def connectToMQTT(host: str, user: str, password: str) -> mqtt.Client:
    logger.debug('Creating MQTT Client')
    mqttClient = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        user
    )
    mqttClient.username_pw_set(user, password)
    mqttClient.connect(host)
    logger.debug('Connected to MQTT Broker')
    return mqttClient


async def main():
    logger.info(APP_NAME)

    config = loadConfig('config.yaml')
    if config is None:
        return

    mqttClient = connectToMQTT(
        config['mqtt']['host'],
        config['mqtt']['user'],
        config['mqtt']['password']
    )

    monitors = []
    tasks = []
    for plug in config['plugs']:
        monitor = TapoPlugMonitor(
            plug["id"],
            plug["ip"],
            plug["username"],
            plug["password"],
            mqttClient,
            config['mqtt']['topic_prefix'] + plug["id"],
            plug["scan_interval"]
        )
        monitors.append(monitor)
        tasks.append(asyncio.create_task(monitor.run()))
        logger.info("Monitoring plug '{0}' on IP {1}".format(plug["id"], plug["ip"]))

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
