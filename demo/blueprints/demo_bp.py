import json
from flask import Blueprint, render_template, request
from demo.models import Word, Category
from ..extensions import db

demo_bp = Blueprint('demo_bp', __name__)


@demo_bp.route('/')
def index():
    # words = dict(Word.get_all())
    category_objects = Category.get_all()
    categories = {}
    words = Word.get_all()
    for category in category_objects:
        wordDict = {}
        for word in words:
            if(word.categoryId == category.id):
                wordDict[word.id] = {
                    'word': word.text,
                    'id': str(word.id)
                }
        categories[category.id] = {
            'name': str(category.name),
            'wordList': wordDict
        }

    return render_template('index.html', categories=json.dumps(categories))


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
    playWords = None
    words = Word.get_all()
    category = 1000
    if request.method == 'POST':
        form_dict = request.form.to_dict()
        play_categories = [int(x) for x in form_dict.values() if x.isdigit()]
        playWords = {}
        for x in play_categories:
            for y in words:
                if y.categoryId == x:
                    playWords[y.id] = {
                        'cat_id': y.categoryId,
                        'id': y.id,
                        'text': y.text,
                        'played': 0
                    }
    return render_template('play.html', category=category, categories=categories,
                           playWords=(json.dumps(playWords) if playWords else None))
