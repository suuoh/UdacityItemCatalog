from flask import Flask, render_template, request
from flask import redirect, url_for, flash, jsonify

# Import CRUD
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Genre, Game

# Import OAuth
from flask import session
import random
import string
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from datetime import date

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Video Game Catalog"

# Create session and connect to database
engine = create_engine('sqlite:///videogamecatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template('login.html', STATE=state)

# @app.route('/fbconnect', methods=['POST'])


# Google Login
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # Upgrade authorization code into credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there are errors, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                   'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']
    session['provider'] = 'google'

    # See if user exists, if not then make a new one
    user_id = getUserID(session['email'])
    if not user_id:
        user_id = createUser(session)
    session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += session['username']
    output += '!</h1>'
    output += '<img src="'
    output += session['picture']
    output += '" style="width:300px; height:300px; border-radius: 150px;'
    output += '-webkit-border-radius:150px; -moz-border-radius:150px;"> '
    flash("You are now logged in as %s" % session['username'])
    print "Logged in via Google"
    return output


# Disconnect and revoke current user's token and reset login_sesion
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user
    access_token = session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps(
                   'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP Get request to revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?'
    url += 'token=%s' % session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Sucessfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # If the given token was invalid
        response = make_response(json.dumps(
                   'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in session:
        if session['provider'] == 'google':
            gdisconnect()
            del session['gplus_id']
            del session['access_token']
        if session['provider'] == 'facebook':
            fbdisconnect()
            del session['facebook_id']
        del session['username']
        del session['email']
        del session['picture']
        del session['user_id']
        del session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


# JSON API endpoint for genres
@app.route('/genres/JSON')
def genresJSON():
    genres = dbsession.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genres])


# JSON API endpoint for games
@app.route('/games/JSON')
def gamesJSON():
    games = dbsession.query(Game).all()
    return jsonify(games=[g.serialize for g in games])


# Show all genres
@app.route('/')
@app.route('/genres')
def showGenres():
    genres = dbsession.query(Genre).order_by(asc(Genre.name)).all()
    return render_template('genres.html', genres=genres)


# Show all games in genre
@app.route('/genres/<int:genre_id>')
def showGames(genre_id):
    genre = dbsession.query(Genre).filter_by(id=genre_id).one()
    games = dbsession.query(Game).filter_by(genre_id=genre_id).all()
    return render_template('games.html', genre=genre, games=games)


# Create new game
@app.route('/genres/<int:genre_id>/new', methods=['GET', 'POST'])
def newGame(genre_id):
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'POST':
        rdate = request.form['release_date'].split('-')
        newGame = Game(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       developer=request.form['developer'],
                       release_date=date(int(rdate[0]), int(rdate[1]),
                                         int(rdate[2])),
                       platform=request.form['platform'],
                       genre_id=genre_id,
                       user_id=session['user_id'])
        dbsession.add(newGame)
        dbsession.commit()
        flash('New game created successfully!')
        return redirect(url_for('showGames', genre_id=genre_id))
    else:
        genre = dbsession.query(Genre).filter_by(id=genre_id).one()
        return render_template('newgame.html', genre=genre)


# Edit existing game
@app.route('/genres/<int:genre_id>/<int:game_id>/edit',
           methods=['GET', 'POST'])
def editGame(genre_id, game_id):
    if 'username' not in session:
        return redirect('/login')
    currentGame = dbsession.query(Game).filter_by(id=game_id).one()
    if currentGame.user_id != session['user_id']:
        notAuthScript = "<script>function notAuth() {alert('You are not "
        notAuthScript += "authorized to edit this. Please create a new game in"
        notAuthScript += " order to edit.');}</script><body "
        notAuthScript += "onload='notAuth()'>"
        return notAuthScript
    if request.method == 'POST':
        rdate = request.form['release_date'].split('-')
        currentGame.name = request.form['name']
        currentGame.description = request.form['description']
        currentGame.price = request.form['price']
        currentGame.developer = request.form['developer']
        release_date = date(int(rdate[0]), int(rdate[1]), int(rdate[2])),
        currentGame.platform = request.form['platform']
        dbsession.add(currentGame)
        dbsession.commit()
        flash('Game edited successfully!')
        return redirect(url_for('showGames', genre_id=genre_id))
    else:
        genre = dbsession.query(Genre).filter_by(id=genre_id).one()
        return render_template('editgame.html', genre=genre, game=currentGame)


# Delete existing game
@app.route('/genres/<int:genre_id>/<int:game_id>/delete',
           methods=['GET', 'POST'])
def deleteGame(genre_id, game_id):
    if 'username' not in session:
        return redirect('/login')
    currentGame = dbsession.query(Game).filter_by(id=game_id).one()
    if currentGame.user_id != session['user_id']:
        notAuthScript = "<script>function notAuth() {alert('You are not "
        notAuthScript += "authorized to edit this. Please create a new game in"
        notAuthScript += " order to edit.');}</script><body "
        notAuthScript += "onload='notAuth()'>"
        return notAuthScript
    if request.method == 'POST':
        dbsession.delete(currentGame)
        dbsession.commit()
        flash('Game deleted successfully!')
        return redirect(url_for('showGames', genre_id=genre_id))
    else:
        return render_template('deletegame.html', game=currentGame)


# User helper functions
def createUser(session):
    newUser = User(name=session['username'], email=session['email'],
                   picture=session['picture'])
    dbsession.add(newUser)
    dbsession.commit()
    user = dbsession.query(User).filter_by(email=session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = dbsession.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = dbsession.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Main method
if __name__ == '__main__':
    app.secret_key = 'my_favourite_game'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
