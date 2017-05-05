from flask import Flask, render_template, session, redirect, request, url_for, g
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from bbc_utils import get_bbc_headlines
from sentiment2 import get_sentiment
from collections import Counter

app = Flask(__name__)
app.secret_key = '1234'
Database.initialise(host='localhost', database='learning', user='slogan', password='0m3gaNZ1')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_from_db_by_screen_name(session['screen_name'])


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token'] = request_token

    # redirect user to twitter to confirm authorization
    return redirect(get_oauth_verifier_url(request_token))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def search():
    # user_ip = '59.167.65.183' # request.remote_addr
    # r = requests.get('http://freegeoip.net/json/{}'.format(user_ip))
    # r_json = r.json()
    # lat = r_json['latitude']
    # long = r_json['longitude']
    # weather = requests.get('http://api.wunderground.com/api/{}/conditions/q/{},{}.json'.format(constants.WEATHER_KEY, lat, long))
    # w_json = weather.json()
    # print(w_json)

    tweets = g.user.twitter_request(
        'https://api.twitter.com/1.1/statuses/home_timeline.json?screen_name={}'.format(g.user))
    tweet_texts = [tweet['text'] for tweet in tweets]
    tweet_sentiment = Counter(get_sentiment(tweet_texts))
    bbc_sentiment = Counter(get_sentiment(get_bbc_headlines()))

    print("Tweet sentiment is:\n{}\n".format(tweet_sentiment))
    print("BBC sentiment is:\n{}\n".format(bbc_sentiment))
    print("All up sentiment is\n{}\n".format(tweet_sentiment + bbc_sentiment))
    return render_template('search.html', content=tweet_texts)


app.run(port=4995, debug=True)
