import logging
import sys
from pathlib import Path

Path("./logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename='./logs/app.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s'
)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

logger = logging.getLogger("app")
logger.addHandler(consoleHandler)
