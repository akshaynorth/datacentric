import pymongo
import os

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
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
@bp.route('/<page>', methods=('GET', 'POST'))
def show_page(page):

    if page == 'index.html':
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client.get_default_database()
        recipe_collection = db['recipes']
        # Get the latest recipes added to the database for home page display
        recipe_cursor = recipe_collection.find().sort('date', pymongo.DESCENDING).limit(9)

        recipe_list = []
        for recipe in recipe_cursor:
            recipe_list.append(recipe)

        client.close()
        return render_template(
            'recipeapp/{}'.format(page),
            repipe_list=recipe_list
        )

    return render_template(
        'recipeapp/{}'.format(page)
    )
