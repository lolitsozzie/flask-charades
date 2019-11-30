import json
from flask import Blueprint, render_template, request
from demo.models import Word, Category
from ..extensions import db

demo_bp = Blueprint('demo_bp', __name__)


@demo_bp.route('/')
def index():
    categories = Category.get_all()
    return render_template('index.html', categories=categories)


@demo_bp.route('/addCategory', methods=['GET', 'POST'])
def addCategory():
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        categories = [c.name for c in Category.get_all()]
        if form_dict['category'] not in categories:
            category = Category(
                name=form_dict['category']
            )
            db.session.add(category)
            db.session.commit()
    return render_template('addCategory.html')


@demo_bp.route('/addWord', methods=['GET', 'POST'])
def addWord():
    categories = Category.get_all()
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        words = Word.get_all()
        word = Word(
            text=form_dict['word'],
            categoryId=int(form_dict['category'])
        )
        if word not in words:
            db.session.add(word)
            db.session.commit()
    return render_template('addWord.html', categories=categories)


@demo_bp.route('/viewWords', methods=['GET', 'POST'])
def viewWords():
    category = 1000
    categories = Category.get_all()
    words = Word.get_all()
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        category = int(form_dict['category'])
        words = [x for x in words if x.categoryId == category]
        pass
    return render_template('viewWords.html', categories=categories, words=words, category=category)
