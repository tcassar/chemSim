import logging
import time

def startLogger():
    logging.basicConfig(filename=f'../logs/runs/SIM@{time.localtime()[4:-5]}')
    logging.info("TEST")

startLogger()
