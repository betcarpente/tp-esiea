from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)

@main.route('/')
def index():
    name = request.args.get('name', 'Monde')
    return render_template('index.html', name=name)