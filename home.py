
import os
import pymongo


def index(environ, start_response):
 """Simplest possible application object"""

 client = pymongo.MongoClient(os['MONGODB_URI'))

 db = client.get_default_database()

 recipe_collection = db['recipes']

 recipes_cursor = recipe_collection.find()

 data = b'<html><head><title>A test</title><body><ul>'


 data = data + "<h1>Recipe name: {}</h1>".format(recipe_doc['recipe_name'])

 for recipe_doc in recipes_cursor:
     data = data + \
         """
         <li>{}</li>
         """.format(
             recipe_doc['description']
         )

 data = data + '</ul></body></html>'
 
 client.close()

 """
 data = b'Hello, World!\n'
 status = '200 OK'
 response_headers = [   ('Content-type', 'text/plain'),  
 ('Content-Length', str(len(data)))  
 ]
 """

 response_headers = [   ('Content-type', 'text/html'),  
 ('Content-Length', str(len(data)))
 ]

 start_response(status, response_headers)
 return iter([data])
