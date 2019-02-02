"""Defines the views to be presented to the user."""
"""File management functions for managing user uploaded image files."""
"""Basic Imports """
import os
import random
import string
import json
import httplib2
import requests
"""from flask module imports"""
from flask import Flask, jsonify, make_response
from flask import request, redirect, url_for, render_template
from flask import flash, send_from_directory
from flask import session as login_session
"""sqlalchemy imports"""
from sqlalchemy import create_engine, asc
from sqlalchemy import desc, literal
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.pool import QueuePool
""" File processing module """
from werkzeug import secure_filename
"""Catalog project database imports """
from database_setup import Base, User, Category, Item
""" goole oauth id_token module imports """
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

""" Initialise the Flask app object """
app = Flask(__name__)


# function to call catalog home page displays 10 recently added items
@app.route('/')
@app.route('/catalog/')
def showCatalogHome():
    """Show the homepage displaying the women clothings and latest items.
    Returns:
        A web page with the 10 latest items that have added.
    """
    session = dbconnect()
    categories = session.query(Category).all()
    latest_items = session.query(Item).order_by(desc(Item.id))[0:10]
    session.close()
    return render_template('catalog_homepage.html',
                           categories=categories,
                           latest_items=latest_items)


# function to display all the items for particular category on the menu
@app.route('/catalog/<category_name>/items/')
def showCatalogItems(category_name):
    """Show items belonging to a specified category.
    Args:
        category_name (str): The name of the category to which the item
            belongs.
    Returns:
        A web page showing all the items in the specified category.
    """
    session = dbconnect()
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % category_name)
        return redirect(url_for('showCatalogHome'))

    categories = session.query(Category).all()
    items = (session.query(Item).filter_by(category=category).
             order_by(Item.name).all())

    session.close()
    if not items:
        flash("There are currently no items in this category.")
    return render_template('show_catalog_item.html',
                           categories=categories,
                           category=category,
                           items=items)


# function to MyCollection page which shows items added by
# currently logined User
@app.route('/catalog/myitems/')
def showMyCatalogItems():
    """If logged in, show the user the items they have added."""
    if 'username' not in login_session:
        return redirect('/login')

    userid = getUserID(login_session['email'])

    session = dbconnect()
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(user_id=userid).all()
    session.close()

    if not items:
        flash("You haven't add any items yet.")
        redirect(url_for('showCatalogHome'))
    return render_template('show_my_catalog_items.html',
                           categories=categories,
                           items=items)


# function to show the details of an item
@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    """Show details of a particular item belonging to a specified category.
    Args:
        category_name (str): The name of the category to which the item
            belongs.
        item_name (str): The name of the item.
    Returns:
        A web page showing information of the requested item.
    """
    session = dbconnect()
    try:
        category = session.query(Category).filter_by(name=category_name).one()
    except NoResultFound:
        flash("The category '%s' does not exist." % category_name)
        session.close()
        return redirect(url_for('showCatalogHome'))

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("The item '%s' does not exist." % item_name)
        session.close()
        return redirect(url_for('showCatalogItems',
                                category_name=category_name))

    user = session.query(User).filter_by(id=item.user_id).one()
    ower_name = user.name

    categories = session.query(Category).all()
    session.close()
    return render_template('show_item.html',
                           categories=categories,
                           category=category,
                           item=item,
                           ower_name=ower_name)


# function to create a new item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def createNewItem():
    """Allow users to create a new item in the catalog."""
    if 'username' not in login_session:
        return redirect('/login')

    session = dbconnect()

    if request.method == 'POST':
        if not request.form['name']:
            flash("New item not created: No name provided.")
            return redirect(url_for('showCatalogHome'))

        if request.form['name'] == "items":
            flash("Error: Can't have an item called 'items'.")
            return redirect(url_for('showCatalogHome'))

        # make sure item names are unique
        qry = session.query(Item).filter(Item.name == request.form['name'])
        already_exists = (session.query(literal(True)).
                          filter(qry.exists()).scalar())
        if already_exists is True:
            flash("Error: There is already an item with the name '%s'"
                  % request.form['name'])
            session.close()
            return redirect(url_for('showCatalogHome'))

        category = (session.query(Category)
                    .filter_by(name=request.form['category']).one())
        add_new_item = Item(category=category,
                            name=request.form['name'],
                            description=request.form['description'],
                            quantity=request.form['quantity'],
                            price=request.form['price'],
                            user_id=login_session['user_id'])

        try:
            createimagefile = request.files['file']
        except Exception:
            createimagefile = None
        try:
            createimageurl = request.form['image_url']
        except Exception:
            createimageurl = None

        if createimagefile and allowedFile(createimagefile.filename):
            filename = secure_filename(createimagefile.filename)
            if os.path.isdir(app.config['UPLOAD_FOLDER']) is False:
                os.mkdir(app.config['UPLOAD_FOLDER'])
            createimagefile.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                              filename))
            add_new_item.image_filename = filename

        elif createimageurl:
            add_new_item.image_url = request.form['image_url']

        session.add(add_new_item)
        session.commit()

        flash("New Item successfully created!")
        category_name = category.name
        item_name = add_new_item.name
        session.close()
        return redirect(url_for('showItem',
                                category_name=category_name,
                                item_name=item_name))
    else:
        categories = session.query(Category).all()

        # See, if any, which category page new item was click on.
        ref_category = None
        if request.referrer and 'catalog' in request.referrer:
            ref_url_elements = request.referrer.split('/')
            if len(ref_url_elements) > 5:
                ref_category = ref_url_elements[4]

        session.close()
        return render_template('create_new_item.html',
                               categories=categories,
                               ref_category=ref_category)


# function to edit an item
@app.route('/catalog/<category_name>/<item_name>/edit/',
           methods=['GET', 'POST'])
@app.route('/catalog/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(item_name, category_name=None):
    """Edit the details of the specified item.
    Args:
        item_name (str): Name of item to be edited.
        category_name (str): Optionally, can also specify the category to
            which the item belongs to.
    """
    if 'username' not in login_session:
        flash("You need to login to edit any item.")
        return redirect('/login')

    session = dbconnect()

    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_name)
        return redirect(url_for('showCatalogHome'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't add this item, so you can't edit it. Sorry :-(")

        category = session.query(Category).filter_by(id=item.category_id).one()
        category_name = category.name
        item_name = item.name
        session.close()
        return redirect(url_for('showItem',
                                category_name=category_name,
                                item_name=item_name))

    if request.method == 'POST':
        if request.form['name'] != item.name:
            # make sure that item names are unique
            qry = session.query(Item).filter(Item.name == request.form['name'])
            already_exists = (session.query(literal(True)).filter(qry.exists())
                              .scalar())
            if already_exists is True:
                original_category = (session.query(Category)
                                     .filter_by(id=item.category_id).one())
                flash("Error: There is already an item with the name '%s'"
                      % request.form['name'])
                session.close()
                return redirect(url_for('showCatalogItems',
                                        category_name=original_category.name))
            item.name = request.form['name']

        form_category = (session.query(Category)
                         .filter_by(name=request.form['category']).one())

        if form_category != item.category:
            item.category = form_category

        item.description = request.form['description']
        item.quantity = request.form['quantity']
        item.price = request.form['price']

        try:
            editimagefile = request.files['file']
        except Exception:
            editimagefile = None
        try:
            editimageurl = request.form['image_url']
        except Exception:
            editimageurl = None
        try:
            delete_image = request.form['delete_image']
        except Exception:
            delete_image = None

        if(delete_image and delete_image == 'delete'):
            if item.image_filename:
                deleteImage(item.image_filename)
                item.image_filename = None
                item.image_url = None
            elif item.image_url:
                item.image_filename = None
                item.image_url = None
                session.add(item)
                session.commit()

        if editimagefile and allowedFile(editimagefile.filename):
            if item.image_filename:
                delete_image(item.image_filename)
            filename = secure_filename(editimagefile.filename)

            if os.path.isdir(app.config['UPLOAD_FOLDER']) is False:
                os.mkdir(app.config['UPLOAD_FOLDER'])
            editimagefile.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                            filename))

            item.image_filename = filename
            item.image_url = None

        elif not editimagefile and editimageurl:
            item.image_url = request.form['image_url']
            if item.image_filename:
                deleteImage(item.image_filename)
                item.image_filename = None

        session.add(item)
        session.commit()

        flash("Item is successfully edited!")
        category_name = form_category.name
        item_name = item.name
        session.close()
        return redirect(url_for('showItem',
                                category_name=category_name,
                                item_name=item_name))
    else:
        categories = session.query(Category).all()
        session.close()
        return render_template('edit_item.html',
                               categories=categories,
                               item=item)


# function to delete an item
@app.route('/catalog/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(item_name):
    """Delete a specified item from the database.
    Args:
        item_name (str): Name of the item to be deleted.
    """
    if 'username' not in login_session:
        return redirect('/login')

    session = dbconnect()
    try:
        item = session.query(Item).filter_by(name=item_name).one()
    except NoResultFound:
        flash("Error: The item '%s' does not exist." % item_name)
        session.close()
        return redirect(url_for('showCatalogHome'))

    if login_session['user_id'] != item.user_id:
        flash("You didn't add this item, so you can't delete it. Sorry :-(")
        category = session.query(Category).filter_by(id=item.category_id).one()
        category_name = category.name
        item_name = item.name
        session.close()
        return redirect(url_for('showItem',
                                category_name=category_name,
                                item_name=item_name))

    if request.method == 'POST':
        if item.image_filename:
            deleteImage(item.image_filename)
        session.delete(item)
        session.commit()
        category = session.query(Category).filter_by(id=item.category_id).one()

        flash("Item successfully deleted!")
        category_name = category.name
        session.close()
        return redirect(url_for('showCatalogItems',
                                category_name=category_name))
    else:
        categories = session.query(Category).all()
        session.close()
        return render_template('delete_item.html',
                               categories=categories,
                               item=item)


# function to display the image file
@app.route('/item_images/<filename>')
def showItemImage(filename):
    """Route to serve user uploaded images.
    Args:
        filename (str): Filename of the image to serve to the client.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# function to verify the file is an allowed format
def allowedFile(filename):
    """Check if the filename has one of the allowed extensions.
    Args:
        filename (str): Name of file to check.
    """
    return ('.' in filename and filename.rsplit('.', 1)[1] in
            app.config['ALLOWED_EXTENSIONS'])


# function to delete an image from the image directory
def deleteImage(filename):
    """Delete an item image file from the filesystem.
    Args:
        filename (str): Name of file to be deleted.
    """
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except OSError:
        print "Error deleting image file %s" % filename


# function to login page
@app.route('/login')
def showLogin():
    """Show the login screen to the user."""
    # Create a state token to prevent request forgery.
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    session = dbconnect()
    categories = session.query(Category).all()
    session.close()
    return render_template('login.html', STATE=state, categories=categories)


# function to login to google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        # Upgrade the authorization one-time code into a credentials object
        oauth_flow = flow_from_clientsecrets('g_client_secrets.json',
                                             scope='email profile')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
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
    g_client_id = json.loads(
        open('g_client_secrets.json', 'r').read())['web']['client_id']
    if result['issued_to'] != g_client_id:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's."), 401)
        print "Token's client ID doesn't match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    url = ('https://www.googleapis.com/oauth2/v2/userinfo?'
           'alt=json&access_token=%s') % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # Check if the user exists in the database. If not create a new user.
    userId = getUserID(login_session['email'])

    if('name' in data):
        login_session['username'] = data["name"]
    else:
        login_session['username'] = login_session['email'].split("@")[0]

    if userId is None:
        userId = createUser(login_session)
    login_session['user_id'] = userId

    output = ''
    output += '<div class="row"><div class="col-4">'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 70%; height: 100%; border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"></div>'
    output += '<div class="col-8"><h4 class="text-muted">Welcome !<br>'
    output += login_session['username']
    output += '</h4></div></div>'
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# function to disconnect from google
def gdisconnect():
    """Revoke a current user's token and reset their login session."""
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Execute HTTP GET request to revoke current token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    http = httplib2.Http()
    result = http.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# function for authentication through facebook login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Login via Facebook OAuth"""
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data
    app_id = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/v2.12/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    # Extract the access token from response
    token = 'access_token=' + data['access_token']

    # Use token to get user info from API.
    url = ('https://graph.facebook.com/v2.12/me?%s'
           '&fields=name,id,email') % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to proplerly
    # logout, let's strip out the information before the equals sign in
    # our token.
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = ('https://graph.facebook.com/v2.12/me/picture?%s&redirect=0'
           '&height=200&width=200') % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # Check if the user exists in the database. If not create a new user.
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# function to disconnect from facebook
def fbdisconnect():
    """Logout via Facebook OAuth."""
    facebook_id = login_session['facebook_id']

    # The access token must be included to successfully logout.
    access_token = login_session['access_token']

    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s') % (facebook_id, access_token)

    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]

    if result == '{"success":true}':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


# function to logout from google or facebook
@app.route('/logout')
def logout():
    """Generic logout function that supports multiple OAuth providers."""
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']

        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']

        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalogHome'))

    else:
        flash("Please log in :)")
        return redirect(url_for('showCatalogHome'))


# function to create a new user
def createUser(login_session):
    """Create a new user in the database."""

    new_user = User(name=login_session['username'],
                    email=login_session['email'],
                    picture=ogin_session['picture'])
    session = dbconnect()
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    session.close()
    return user.id


# function to find whether user already exists by email
def getUserID(email):
    """Given an email address, return the user ID, if in the database.
    Args:
        email (str): The email address associated with the user account.
    Returns:
        The user id number stored in the database.
    """
    session = dbconnect()
    try:
        user = session.query(User).filter_by(email=email).one()
        session.close()
        return user.id
    except NoResultFound:
        session.close()
        return None


# function to open the database connection
def dbconnect():
    """Connects to the database and returns an sqlalchemy session object."""
    engine = create_engine(app.config['DATABASE_URL'])
    Base.metadata.bind = engine
    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


# JSON end points to display all category
@app.route('/categories/JSON')
def categoriesJSON():
    """Returns all the items in the catalog as a JSON file.
    The for loop in the call to jsonify() goes through each category and,
    because the Category class has a reference to the items in it, for each
    item a call to its serialise function is made. So we end up with a JSON
    array of items for each category.
    """
    session = dbconnect()
    categories = session.query(Category).all()
    session.close()
    return jsonify(categories=[c.serialise for c in categories])


# JSON end points to display all items for all catergory
@app.route('/items/JSON')
def itemsJSON():
    session = dbconnect()
    items = session.query(Item).all()
    session.close()
    return jsonify(items=[i.serialise for i in items])


# JSON end points to display all users
@app.route('/users/JSON')
def userJSON():
    session = dbconnect()
    users = session.query(User).all()
    session.close()
    return jsonify(users=[i.serialise for i in users])


# JSON end points to display items for a particular user id
@app.route('/items/<user_id>/JSON')
def userCatergoryJSON(user_id):
    session = dbconnect()
    items = session.query(Item).filter_by(user_id=user_id).all()
    session.close()
    return jsonify(items=[i.serialise for i in items])


# JSON end points to display all items for a particular catergory id
@app.route('/<category_id>/items/JSON')
def categoryItemsJSON(category_id):
    session = dbconnect()
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category=category).all()
    session.close()
    return jsonify(items=[i.serialise for i in items])


# This is the main function which has all the application configuration details
if __name__ == '__main__':
    """ App configuration """
    app.config['DATABASE_URL'] = 'sqlite:///womenswearcatalog.db'
    app.config['UPLOAD_FOLDER'] = '/vagrant/catalog/item_images/'
    app.config['OAUTH_SECRETS_LOCATION'] = '/vagrant/catalog/'
    app.config['ALLOWED_EXTENSIONS'] = set(['jpg', 'jpeg', 'png', 'gif'])
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024  # 4 MB
    app.secret_key = 'monkey'  # This needs changing in production env
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
