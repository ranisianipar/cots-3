import flask
from flask import request, jsonify

import threading
import pika
import sys
import os

import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

RABBITMQ_HOST = '152.118.148.95'
RABBITMQ_PORT = 5672
RABBITMQ_WEBSOCKET_PORT = 15674
RABBITMQ_USER = '0806444524'
RABBITMQ_PASSWORD = '0806444524'
RABBITMQ_VHOST = '/0806444524'

# development
# RABBITMQ_HOST = 'localhost'
# RABBITMQ_PORT = 5672
# RABBITMQ_WEBSOCKET_PORT = 15674
# RABBITMQ_USER = 'guest'
# RABBITMQ_PASSWORD = 'guest'
# RABBITMQ_VHOST = '/'

NPM = '1606885025'
ROUTING_KEY = 'cots3'

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST, 
                port=RABBITMQ_PORT, 
                virtual_host=RABBITMQ_VHOST,
                credentials=credentials)

# RabbitMQ
class MessageService:
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        # Declare exchange, push message directly to the queue is forbidden
        self.channel.exchange_declare(exchange=NPM, exchange_type='direct')

    def send_message(self, message):
        self.channel.basic_publish(exchange=NPM, routing_key=ROUTING_KEY, body=message)
        print(f'Publishing exchange={NPM} routing_key={ROUTING_KEY} body={message}')
            
    def close_channel(self):
        self.channel.close()

# Download remotely using wget
def download_remotely(url):
    ms = MessageService()

    # do download file
    downloaded_file = os.system(f'wget "{url}" -o cots.log')

    # haven't figured the way out to get the progress
    for x in range(10):
        ms.send_message(f'[{x+1}] test')
        time.sleep(2)
    ms.close_channel()

# Download in Background
def download_async(url):
    thread = threading.Thread(target=download_remotely, args=(url,))
    thread.start()

@app.route('/', methods=['GET'])
def home():
    return "Hello"

@app.route('/download', methods=['POST'])
def download():
    url = request.args.get('url')

    download_async(url)

    data = {
        'rabbitmq_host':RABBITMQ_VHOST,
        'rabbitmq_user':RABBITMQ_USER,
        'rabbitmq_password':RABBITMQ_PASSWORD,
        'subscription_topic':f'/exchange/{NPM}/{ROUTING_KEY}',
        'websocket_url':f'http://{RABBITMQ_HOST}:{RABBITMQ_WEBSOCKET_PORT}/stomp',
        'download_url':url
    }
    return jsonify(data)

app.run(port=5001)