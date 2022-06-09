# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps import db
from apps.authentication.models import Users, Posts, Tags


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/jaco')
@login_required
def jaco():

    # create a dummy post with tags
    post = Posts(title='This is a test pest', body='test', user_id=1)
    db.session.add(post)
    db.session.commit()

    tags = ['dog', 'test', 'cat', 'good food']

    for tag in tags:
        t = Tags(tag=tag, post_id=1)
        db.session.add(t)
        db.session.commit()

    return "Hello Jaco boy"

@blueprint.route('/show')
@login_required
def show():
    # load the latest post from the database
    post = Posts.query.filter_by(id=1).first()

    # print the tags
    print(post.tags)

    return jsonify({'title': post.title, 'body': post.body, 'type': post.type, 'timestamp': post.timestamp, 'author': post.author.username, 'tags': [tag.tag for tag in post.tags]})


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
