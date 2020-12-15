import pymongo
import os
import json
import io

import datetime

from bson.objectid import ObjectId

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify, send_file, abort
)


bp = Blueprint('recipeapp', __name__)


# @bp.route('/', methods=('GET', 'POST'))
# def index():
#
#     client = pymongo.MongoClient(os.environ['MONGODB_URI'])
#
#     db = client.get_default_database()
#
#     recipe_collection = db['recipes']
#
#     recipes_cursor = recipe_collection.find()
#
#     recipe_list = list()
#
#     for recipe_doc in recipes_cursor:
#         recipe_list.append(recipe_doc)
#
#     return render_template('recipeapp/index.html', recipes=recipe_list)

@bp.route('/', defaults={'page': 'index.html'}, methods=('GET', 'POST'))
@bp.route('/pages/<page>', methods=('GET', 'POST'))
def show_page(page):

    if page == 'index.html':
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']
        # Get the latest recipes added to the database for home page display
        recipe_cursor = recipe_collection.find().sort('date', pymongo.ASCENDING).limit(9)

        recipe_list = []
        for recipe in recipe_cursor:
            recipe_list.append(recipe)

        client.close()
        return render_template(
            'recipeapp/{}'.format(page),
            recipe_list=recipe_list
        )

    return render_template(
        'recipeapp/{}'.format(page)
    )

@bp.route('/recipe/create', methods=('POST',))
def create_recipe():
    client = None
    try:
        recipe_data = request.form

        # Build data dictionary
        image_data = ''
        if request.files.get('file', None):
            image_data = request.files['file'].read()

        recipe_record_dict = {
            "creation_time": datetime.datetime.now().isoformat(),
            "name": recipe_data['name'],
            "type": recipe_data['type'],
            "picture":  image_data,
            "prep_time": recipe_data['prep_time'],
            "short_description": recipe_data['recipe_desc'],
            "cook_time": recipe_data['cook_time'],
            "calories": recipe_data['calories'],
            "portions": recipe_data['portions'],
            "ingredients": json.loads(recipe_data['ingredients']),
            "instructions": json.loads(recipe_data['instructions'])
        }

        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        recipe_collection.insert(recipe_record_dict)

        client.close()
        client = None

        return jsonify(dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    finally:
        if client:
            client.close()

@bp.route('/recipe/image/<obj_id>', methods=('GET',))
def download_image(obj_id):
    client = None
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        recipe_cursor = recipe_collection.find({'_id': ObjectId(obj_id)})

        for recipe in recipe_cursor:
            return send_file(io.BytesIO(recipe['picture']),
                             attachment_filename='{}'.format(obj_id),
                            )
        else:
            raise ValueError('Image not found for Object Id: {}'.format(obj_id))

    except:
        abort(404)
    finally:
        if client:
            client.close()