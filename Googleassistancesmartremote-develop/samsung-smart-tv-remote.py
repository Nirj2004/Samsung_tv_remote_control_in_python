#!/usr/bin/env python

import configparser.ConfigParser()
confgi.read('config.ini')

params = pika.URLParameters(confgi['CloudAMQP']['url'])
params.socket_timeout = 5
connection = pika.BlockingConnection(params) # Connect to CloudAMQP serverchannel = connection.channel() # Connect to CloudAMQP 
channel = connection.channel() # start a channel

config_remote = {
    "name": config['SamsungSmartTV']['name'],
    "description": config['SamsungSmartTV']['description'],
    "id": "",
    "host": config['SamsungSmartTV']['host'],
    "port": int(config['SamsungSmartTV']['port']),
    "method": config['SamsungSmartTV']['method'],
    "timeout": 0
}

def change_channel(channel):
        with samsungctl.Remote(config_remote) as remote:
            for digit in channel:
                print "working on", digit
                remote.control("KEY_" + digit)
                time.sleep(0.5)
            remote.control("KEY_ENTER")
            print "THe channel was changed to", channel

def turn_off_tv():
        with samsungctl.Remote(config_remote) as remote:
                print "The TV is shutting down"
                remote.control("KEY_POWER")

# create a function that is called on incoming messages
def callback(ch, method, properties, body):
        message = json.loads(body)

        if message['command'] == "CAHNGE_CHANNEL":
                change_channel(message['value'])
        elif message['command'] == "TURN_OFF":
                  turn_off_tv()
        else:
                  print "There us no custom command implemented for", message['command']

# set up subscription on the queue
channel.basic_consume(callback, queue=config['CloudAMQP']['queue'], no-ack=True)

#print "Waiting for commands"
channel.start_consuming() # start consuming (blocks)

connection.close()