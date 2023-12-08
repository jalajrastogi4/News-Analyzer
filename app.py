from flask import Flask, render_template, session, jsonify
from flask_session import Session
from datetime import datetime
import requests
from plot_utils import linguistic_plot, word_count_distribution_plot

app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Index Page View : World category
@app.route('/')
def index():
    url = "https://us-central1-news-analyzer-403505.cloudfunctions.net/get_news?freshness=any&categories=world&max_results=10&stats=1"
    categories = ['business', 'entertainment', 'environment', 'food', 'health', 'politics', 'science', 'sports', 'world', 'tourism']
    
    response = requests.get(url)
    response_json = response.json()
    session['current_article'] = response_json

    for item in response_json:
        datetime_str = item['pubDate']
        date_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        item['pubDate'] = date_obj.strftime("%d %b, %Y %H:%M")

    
    return render_template('index_new_v2.html', news_objects=response_json, categories=categories)

# Category Page View : World category
@app.route('/categories/<category>')
def index_category(category):
    category_name = category
    url = f"https://us-central1-news-analyzer-403505.cloudfunctions.net/get_news?freshness=any&categories={category_name}&max_results=10&stats=1"
    categories = ['business', 'entertainment', 'environment', 'food', 'health', 'politics', 'science', 'sports', 'world', 'tourism']

    response = requests.get(url)
    response_json = response.json()
    session['current_article'] = response_json

    for item in response_json:
        datetime_str = item['pubDate']
        date_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        item['pubDate'] = date_obj.strftime("%d %b, %Y %H:%M")

    
    return render_template('index_new_v2.html', news_objects=response_json, categories=categories)

# Single article Page View
@app.route('/article/<article_name>')
def single_article(article_name):
    article = {}
    for item in session['current_article']:
        if item['article_id'] == article_name:
            article = item
            break
    if article:
        linguistic_figure = linguistic_plot(article)
        word_dist_figure = word_count_distribution_plot(article)
        article['linguistic_figure'] = linguistic_figure
        article['word_dist_figure'] = word_dist_figure
    return render_template('singlearticle.html', article=article)

# Single article Chart on Indedx View
@app.route('/article_chart/<article_name>')
def single_article_chart(article_name):
    # print([i['article_id'] for i in session['current_article']])
    article = {}
    for item in session['current_article']:
        if item['article_id'] == article_name:
            article = item
            break
    # print(article)
    json_response = {}
    if article:
        linguistic_figure = linguistic_plot(article)
        word_dist_figure = word_count_distribution_plot(article)
        json_response['linguistic_figure'] = linguistic_figure
        json_response['word_dist_figure'] = word_dist_figure
    return jsonify(json_response)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')