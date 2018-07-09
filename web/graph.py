# -*- coding: utf-8 -*-
import os
import datetime
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, send_from_directory
)


bp = Blueprint('graph', __name__, url_prefix='/graph')


def get_img(img_dir, img_name):
    if not os.path.join(img_dir, img_name):
        return 'Not Found'
    return send_from_directory(img_dir, img_name)


@bp.route('/min/<date>/<code>.gif')
def get_min_graph(code, date):
    graph_dir = os.path.join(current_app.config['MIN_GRAPH_DIR'], date)
    file_name = '{}.gif'.format(code)
    return get_img(graph_dir, file_name)
    

@bp.route('/<g_type>/<code>.gif')
def get_graph(g_type, code):
    graph_dir = current_app.config['GRAPH_DIRS'].get(g_type)
    file_name = '{}.gif'.format(code)
    return get_img(graph_dir, file_name)


@bp.route('/min/<code>/<date>/')
def show_min_graph(code, date):
    graph_dir = os.path.join(current_app.config['MIN_GRAPH_DIR'], date)
    file_name = '{}.gif'.format(code)
    if not os.path.exists(os.path.join(graph_dir, file_name)):
        return 'Not Found'
    data = {
        'code': code,
        'date': date
    }
    return render_template('graph/img.html', data=data)


@bp.route('/<g_type>/<code>')
def show_graph(g_type, code):
    graph_dir = current_app.config['GRAPH_DIRS'].get(g_type, '')
    file_name = '{}.gif'.format(code)
    if not os.path.exists(os.path.join(graph_dir, file_name)):
        return "Not Found"
    data = {
        'g_type': g_type,
        'code': code
    }
    return render_template('graph/img.html', data=data)
