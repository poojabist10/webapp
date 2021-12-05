# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, session
from flask_login import login_required
from jinja2 import TemplateNotFound
import os
import csv
import pandas as pd
from sqlalchemy import create_engine, types


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


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



@blueprint.route('/index', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        uploaded_file.save(os.path.join(session['username'],filename))
        mysqlpush(filename)

    return redirect(url_for('home_blueprint.index'))
    

def mysqlpush(filename):
    engine = create_engine('mysql+pymysql://flszhwhgye:5Q36145E87LWYMIQ$@cloudprojects-mysqlserver.mysql.database.azure.com/testing')

    df = pd.read_csv(os.path.join(session['username'],filename),sep=',',quotechar='\'',encoding='utf8') 

    df.columns = df.columns.str.strip()

    if 'transactions' in filename:

        df.to_sql('transactions',con=engine,index=False,if_exists='append',method='multi',chunksize=100000) 


