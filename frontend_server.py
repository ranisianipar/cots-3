import flask
import requests
from flask import request, jsonify, render_template

app = flask.Flask(__name__, template_folder='template')
app.config["DEBUG"] = True

BACKEND_URL = 'http://localhost:5001/'

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/download', methods=['POST'])
def download():
    download_url = request.form.get('url')
    print(f'DOWNLOAD URL: {download_url}')
    response = requests.post(
        BACKEND_URL+'download?url='+download_url
    ).json()
    rabbitmq_host = response['rabbitmq_host']
    rabbitmq_user = response['rabbitmq_user']
    rabbitmq_password = response['rabbitmq_password']
    websocket_url = response['websocket_url']
    subscription_topic = response['subscription_topic']
    download_url = download_url
    # routing_key?
    return render_template('download.html',
                            rabbitmq_host=rabbitmq_host,
                            rabbitmq_user=rabbitmq_user,
                            rabbitmq_password=rabbitmq_password,
                            subscription_topic=subscription_topic,
                            websocket_url=websocket_url,
                            download_url=download_url
    )

app.run(port=5002)