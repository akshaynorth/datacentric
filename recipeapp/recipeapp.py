import pymongo
import os
import json
import io
import re
import logging

import datetime

from bson.objectid import ObjectId
from bson.regex import Regex

from flask import (
    Blueprint, redirect, render_template, request, url_for, jsonify, send_file, abort
)


bp = Blueprint('recipeapp', __name__)
logger = logging.getLogger(__name__)

@bp.route('/', defaults={'page': 'index.html'}, methods=('GET', 'POST'))
@bp.route('/pages/<page>', methods=('GET', 'POST'))
def show_page(page):
    """Renders the provided HTML page to the user of the site

    Parameters
    ----------
    page : str
        string representation of the HTML template name representing a web page to render

    Returns
    -------
    str
        string representation HTML web page
    """

    # For the home page pass a list of recipes to display to be displayed in the latest recipes section
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

    # For all other pages just render them
    return render_template(
        'recipeapp/{}'.format(page)
    )

@bp.route('/recipe/create', methods=('POST',))
def create_recipe():
    """Create a recipe on the MongoDB database

    Returns
    -------
    str
        JSON with result of the create recipe request. When a request fails, an HTTP error code is sent along with
        the returned JSON contains the error text in the 'error' key. For example:
        {
            "error": "Invalid credentials provided"
        }
        When no error occurs an empty JSON is sent with the HTTP 200 code
    """
    client = None
    try:
        recipe_data = request.form

        # Build data dictionary
        image_data = ''
        if request.files.get('file', None):
            # Read the image data provided by the user uploaded image
            image_data = request.files['file'].read()

        # Create a recipe document dictionary
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

        # Connect to the MongoDB database
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        # Insert the recipe document into the MongoDB database
        recipe_collection.insert(recipe_record_dict)

        return jsonify(dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    finally:
        if client:
            client.close()

@bp.route('/recipe/search', methods=('POST',))
def search_recipe():
    """Search for a recipe in the MongoDB database

    Returns
    -------
    str
        The string representation of the search results web page to be sent to the Web client
    """
    client = None
    try:
        recipe_data = request.form

        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        query_dict = dict()

        recipe_type = recipe_data.get('type', None)
        # Only filter the recipe results based on the recipe category when it is not set to ALL
        if recipe_type and recipe_type.upper() != 'ALL':
            query_dict.update({
                'type': recipe_type
            })

        ingredient_search_type = recipe_data.get('ingredient_search_type', None)
        if ingredient_search_type and ingredient_search_type.upper() == 'ALL':
            # The user has specified to filter based on for all ingredients provided
            ingredient_search_op = '$all'
        else:
            # The user has specified to filter based on any of the ingredients provided
            ingredient_search_op = '$in'

        ingredient_list = recipe_data.get('ingredient_list', None)
        if ingredient_list and len(ingredient_list) > 0:
            # Add the ingredient-based filter when ingredients for search have been provided
            query_dict.update({
                'ingredients': {
                    ingredient_search_op: [
                        Regex.from_native(re.compile(ing_str.replace('-','\s'), re.I)) for ing_str in ingredient_list
                    ]
                }
            })

        # Issue the recipe find request based on the constructed rich query
        recipe_cursor = recipe_collection.find(query_dict)

        # Create a list of recipes found to be passed in the context of the JinJa template
        recipe_list = []
        for recipe in recipe_cursor:
            recipe_list.append(recipe)

        return render_template(
            'recipeapp/browse-recipes.html',
            recipe_list=recipe_list
        )
    except Exception:
        logger.exception('Could not search recipe')
        abort(404)
    finally:
        if client:
            client.close()

@bp.route('/recipe/edit/<obj_id>', methods=('GET',))
def edit_recipe(obj_id):
    """Stores updated information of a recipe in the MongoDB database

    Parameters
    ----------
    obj_id : str
        document object id of the recipe to be edited

    Returns
    -------
    str
        HTML of edit recipe page a signal of success
    """
    client = None
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        query_dict = {
            '_id': ObjectId(obj_id)
        }

        recipe_cursor = recipe_collection.find(query_dict)
        recipe = next(recipe_cursor)

        if not recipe:
            raise ValueError('Recipe not found')

        return render_template(
            'recipeapp/edit-recipe.html',
            recipe=recipe
        )
    except Exception:
        logger.exception('Could not search recipe')
        abort(404)
    finally:
        if client:
            client.close()

@bp.route('/recipe/image/<obj_id>', methods=('GET',))
def download_image(obj_id):
    """Obtains the binary of a recipe image

    Parameters
    ----------
    obj_id : str
        the document object id of the recipe whose image is to be downloaded

    Returns
    -------
    str
        the binary information representing the image data. The image type is automatically detected by the Web client

    """
    client = None
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        recipe_cursor = recipe_collection.find({'_id': ObjectId(obj_id)})

        for recipe in recipe_cursor:
            # Send the image byte data. The file name is set to the document object id
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


@bp.route('/recipe/view/<obj_id>', methods=('GET',))
def view_recipe(obj_id):
    """Obtain the read-only details of a recipe

    Parameters
    ----------
    obj_id : str
        the document object id of the recipe to obtain details for

    Returns
    -------
    str
        the HTML page representing the details of the recipe
    """
    client = None
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        query_dict = {
            '_id': ObjectId(obj_id)
        }

        # Find the recipe on the MongoDB database based on the document object id
        recipe_cursor = recipe_collection.find(query_dict)
        recipe = next(recipe_cursor)

        if not recipe:
            # The document object id provided did not result in any recipes found consider it an invalid object id
            # and raise an error
            raise ValueError('Recipe not found')

        return render_template(
            'recipeapp/recipe-view.html',
            recipe=recipe
        )
    except Exception:
        logger.exception('Could not search recipe')
        abort(404)
    finally:
        if client:
            client.close()

@bp.route('/recipe/edit_submit/<obj_id>', methods=('POST',))
def edit_submit(obj_id):
    """Updates a recipe in the Mongo DB database

    Parameters
    ----------
    obj_id : str
        the document object id of the recipe to be updated

    Returns
    -------
    str
        JSON with result of the edit recipe request. When a request fails, an HTTP 404 error code is sent along with
        the returned JSON contains the error text in the 'error' key. For example:
        {
            "error": "Invalid credentials provided"
        }
        When no error occurs an empty JSON is sent with the HTTP 200 code

    """
    client = None
    try:
        recipe_data = request.form

        # Build data dictionary
        image_data = ''
        if request.files.get('file', None):
            # When a user provides an image in the request, obtain the data for it to be updated in the database
            # otherwise keep the pre-existing image
            image_data = request.files['file'].read()

        # Create a MongoDB document representation of the recipe for update
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

        # Update the recipe in the MongoDB database based on the object id and recipe data provided
        recipe_collection.update({'_id': ObjectId(obj_id)}, recipe_record_dict)

        return jsonify(dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404
    finally:
        if client:
            client.close()

@bp.route('/recipe/delete/<obj_id>', methods=('POST',))
def delete_recipe(obj_id):
    """Delete a recipe from the MongoDB database

    Parameters
    ----------
    obj_id : str
        the document object id of the recipe to be deleted

    Returns
    -------
        JSON with result of the delete recipe request. When a request fails, an HTTP 404 error code is sent along with
        the returned JSON contains the error text in the 'error' key. For example:
        {
            "error": "Invalid credentials provided"
        }
        When no error occurs an empty JSON is sent with the HTTP 200 code
    """
    client = None
    try:
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']

        recipe_collection.remove({'_id': ObjectId(obj_id)})

        return jsonify(dict()), 200
    except Exception as e:
        logger.exception('Could not delete recipe')
        return jsonify({'error': str(e)}), 404
    finally:
        if client:
            client.close()
