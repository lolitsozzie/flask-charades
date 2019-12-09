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
    category = ''
    correctlyAdded = False
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        categories = [c.name for c in Category.get_all()]
        category = form_dict['category']
        if form_dict['category'] not in categories:
            category = Category(
                name=form_dict['category']
            )
            correctlyAdded = True
            db.session.add(category)
            db.session.commit()
    return render_template('addCategory.html', category=category, correctlyAdded=correctlyAdded)


@demo_bp.route('/addWord', methods=['GET', 'POST'])
def addWord():
    categories = Category.get_all()
    sameWord = False
    correctlyAdded = False
    previousWord = ''
    categoryId = 1000
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        categoryId = int(form_dict['category'])
        words = [x.text for x in Word.get_all()]
        word = Word(
            text=form_dict['word'],
            categoryId=categoryId
        )
        previousWord = word.text
        if word.text in words:
            sameWord = True
        if word.text not in words:
            correctlyAdded = True
            db.session.add(word)
            db.session.commit()
    return render_template('addWord.html', categories=categories, sameWord=sameWord, correctlyAdded=correctlyAdded,
                           word=previousWord, categoryId=categoryId)


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

@demo_bp.route('/play', methods=['GET', 'POST'])
def play():
    categories = Category.get_all()
    playWords = []
    words = Word.get_all()
    category = 1000
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        play_categories = [int(x) for x in form_dict.values() if x.isdigit()]
        for x in play_categories:
            for y in words:
                if y.id == x:
                    playWords.append(y)
    return render_template('play.html', category=category, categories=categories, playWords=playWords)
