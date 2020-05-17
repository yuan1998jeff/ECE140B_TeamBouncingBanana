from wsgiref.simple_server import make_server
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse
from pyramid.response import Response
from pyramid.config import Configurator
import requests
import json
import mysql.connector as mysql
import os
import time
import datetime
from datetime import datetime
# from flask import request

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

#-# API #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#  
def show_kvp(req):
    return render_to_response('templates/KVP_page.html', {}, request=req)


def show_signup(req):
    return render_to_response('templates/signUp.html', {}, request=req)

def post_signup(req):
    fname = req.POST.getone('fname')
    lname = req.POST.getone('lname')
    email = req.POST.getone('email')

    # Connect to the database and inset new subscriber
    # insert subscriber info into DB
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
    cursor = db.cursor()
    query = "insert into TSubscribers (first_name, last_name, email, created_at) values (%s, %s, %s, %s)"    
    ts = time.time()
    ts = ts-(7*60*60)
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    values = (fname, lname, email, st)
    cursor.execute(query, values)
    db.commit()
    db.close()

    return render_to_response('templates/signUp.html', {}, request=req)

def show_aboutUs(req):
    return render_to_response('templates/aboutUs.html',{},request=req)


#-# Routing #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-# 
if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    # routes for showing kvp page
    config.add_route('welcome', '/kvp')
    config.add_view(show_kvp, route_name='welcome')

    # show signup and check signup
    config.add_route('sign_up', '/signup')
    config.add_view(post_signup, route_name='sign_up', request_method='POST') 
    config.add_view(show_signup, route_name='sign_up') 


    # routes for aboutUs page
    config.add_route('info', '/aboutUs')
    config.add_view(show_aboutUs, route_name='info')


    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 5000, app) #?????????????
    server.serve_forever()


  

