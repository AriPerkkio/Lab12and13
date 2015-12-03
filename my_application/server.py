import os
from flask import Flask, Response, request, redirect, url_for
from werkzeug import secure_filename
import urllib2
import boto
import boto.sqs
import boto.sqs.queue
from boto.sqs.message import Message
from boto.sqs.connection import SQSConnection
from boto.exception import SQSError
import sys
import json
from tempfile import mkdtemp
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route("/")
def index():
    return """
Available API endpoints:

GET /queues						List all queues
POST /queues					Create a new queue
DELETE /queues/<id>				Delete a specific queue
GET /queues/<id>/msgs			Get a message, return it to the user
GET /queues/<qud>/msg/count		Return the number of messages in a queue
POST /queues/<qid>/msgs 		Write a new message to a queue
DELETE /queues/<qid>/msgs 		Get and delete a message from the queue

"""

@app.route("/version", methods=['GET'])
def version():
	"""
	print boto version

	curl -s -X GET localhost:5000/version

	"""
	print("Boto version: "+boto.Version+ "\n")
	return "Boto version: "+boto.Version+ "\n"

@app.route("/queues", methods=['GET'])
def queues_index():
	"""
	List all queues

	curl -s -X GET -H 'Accept: application /json' http://localhost:5000/queues | python -mjson.tool

	"""
	all = []
	conn = get_conn()
	for q in conn.get_all_queues():
		all.append(q.name)
	resp = json.dumps(all)
	print json.dumps(all)
	return Response(response=resp, mimetype="application/json") 

def get_conn():
	key_id, secret_access_key = urllib2.urlopen("http://ec2-52-30-7-5.eu-west-1.compute.amazonaws.com:81/key").read().split(':')
	print "\nKey id: " +key_id
	print "Secret access key: " + secret_access_key + "\n"
	return boto.sqs.connect_to_region("eu-west-1", aws_access_key_id=key_id ,aws_secret_access_key=secret_access_key)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)