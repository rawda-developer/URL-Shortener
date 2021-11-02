from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json
import os
from werkzeug.utils import secure_filename

bp = Blueprint('urlshort', __name__)

@bp.route('/')
def home():
    return render_template('home.html', codes=session.keys())


@bp.route('/your-url', methods=['POST', 'GET'])
def your_url():
    if request.method == 'POST':
        urls = {}
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls = json.load(url_file)
        if request.form['code'] in urls.keys():
            flash('This short name already exists. Please choose another short name')
            return redirect(url_for('urlshort.home'))
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            file_name = secure_filename(request.form['code'] + f.filename)
            file_path = os.getcwd() + '/urlshort/static/user_files/'
            # file_path = ''
            f.save(file_path + file_name)
            urls[request.form['code']] = {'file': file_name}
        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['code']] = True
        return render_template('your_url.html', code=request.form['code'])
    return redirect(url_for('urlshort.home'))


@bp.route('/<string:code>')
def get_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as url_file:
            urls = json.load(url_file)
            print(urls)
            if code not in urls.keys():
                abort(404)
            if 'url' in urls[code].keys():
                return redirect(urls[code]['url'])
            else:
                return redirect(url_for('static', filename='user_files/'+urls[code]['file']))
    else:
        return redirect(url_for('urlshort.home'))


@bp.route('/api')
def get_api():
    return jsonify(list(session.keys()))

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
