# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask import current_app
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "hello world\n" + current_app.config['BASE_DIR']

    from . import stat
    app.register_blueprint(stat.bp)

    from . import graph
    app.register_blueprint(graph.bp)

    from . import tick
    app.register_blueprint(tick.bp)

    Bootstrap(app)
    return app