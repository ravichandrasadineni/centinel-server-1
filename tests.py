import flask
from flask import Flask
from flask.ext.testing import TestCase

from server import app, db, Client
import config
#for tests
from cStringIO import StringIO
import unittest
import uuid
import base64
import io

class MyTest(TestCase):
	
    testUsername = str(uuid.uuid4())
    testPassword = 'testingpassword'

    def create_app(self):
		self.app = Flask(__name__)
		self.app.config.from_object('config.testingConfig')
		return app

    def setUp(self):
    	db.create_all()
    	user = Client(username=self.testUsername)
    	user.hash_password(self.testPassword)
    	db.session.add(user)
    	db.session.commit()

    def tearDown(self):
    	db.session.remove()
    	db.drop_all()

    def open_with_auth(self, url, method, username, password):
        return self.client.open(url,
            method=method,
            headers={
                'Authorization': 'Basic ' + base64.b64encode(username + \
                ":" + password)
            }
        )	

    def test_version(self):
    	url = '/version'
    	response = self.client.get(url)
    	self.assert_200(response)
        self.assertEquals(response.json, {"version" : config.recommended_version})

    def test_results_GET(self):
    	url = '/results'	
    	#Check for broken auth ->
        response = self.client.get(url)
        self.assert_401(response)
        self.assertTrue('WWW-Authenticate' in response.headers)
        self.assertTrue('Basic' in response.headers['WWW-Authenticate'])
        #Check working auth ->
        response = self.open_with_auth(url,'GET',self.testUsername, self.testPassword)
        self.assert_200(response)

    def test_results_POST(self):
		pass 
    
    def test_experiments(self):
    	url = '/experiments'
    	response = self.client.get(url)
    	self.assert_200(response)
    	#XXX: Could be expanded?
    	for experiment in response.json["experiments"]:
    		url = '/experiments/{0}'.format(experiment)
    		response_ = self.client.get(url)
    		self.assert_200(response)

    def test_clients(self):
    	url = '/clients'
    	#Check for broken auth ->
        response = self.client.get(url)
        self.assert_401(response)
        self.assertTrue('WWW-Authenticate' in response.headers)
        self.assertTrue('Basic' in response.headers['WWW-Authenticate'])
        #Check working auth ->
        response = self.open_with_auth(url,'GET',self.testUsername, self.testPassword)
        self.assert_200(response)
        self.assertEquals(response.json, {"clients" : [self.testUsername]})

    def test_log(self):
    	#XXX: TODO
    	pass
    
    def test_register(self):
    	url = '/register'
    	testUsername = str(uuid.uuid4())
    	testPassword = 'somepassword'
    	response = self.client.post(url, \
    		data = flask.json.dumps({'username': testUsername, 'password': testPassword}),\
    	    content_type='application/json')
        self.assertEquals(response.json, {"status" : "success"})
        self.assert_status(response,201)


if __name__ == '__main__':
	unittest.main()