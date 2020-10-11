import pymongo
import os

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)


bp = Blueprint('recipeapp', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():

    client = pymongo.MongoClient(os.environ['MONGODB_URI'])

    db = client.get_default_database()

    recipe_collection = db['recipes']

    recipes_cursor = recipe_collection.find()

    recipe_list = list()

    for recipe_doc in recipes_cursor:
        recipe_list.append(recipe_doc)

    return render_template('recipeapp/index.html', recipes=recipe_list)
