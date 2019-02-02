# Item Catalog Project

Item Catalog project is a web application developed by utilizing the Flask framework which accesses a SQL database to populate data. It also uses third party authentication like OAuth2 for google and facebook application.

# About
This application provides Women Exclusive Store details that stores the details of women's clothing and accessories. Currently it contains 6 categories. The user can login via Facebook or google in order to create new Items. They can create, edit and delete the data if they are logged in. It also restricts from deleting other's data.

# Features
	Google and facebook oauth authentication and authorisation check.
	Full CRUD support using SQLAlchemy and Flask framework.
	JSON endpoints.

# Project Structure
	.
	├── g_client_secrets.json
	├── fb_client_secrets.json
	├── database_setup.py
	├── populate_data.py
	├── womenswearcatalog.db
	├── views.py
	├── README.md
	├── item_images
	├── static
	│   └── css 
	│       └── cssstyle.css
	│   └── js
	│       └── js.cookie-2.0.4.min.js
	│   └── mdl
	│       └── material.css
	│       └── material.js
	│       └── material.min.css
	│       └── material.min.css.map
	│       └── material.min.js
	│       └── material.min.js.map
	└── templates
		├── add_item_button.html
		├── catalog_homepage.html
		├── create_new_item.html
		├── delete_item.html
		├── edit_item.html
		├── layout.html
		├── login.html
	    ├── show_catalog_item.html
	    ├── show_item.html
	    ├── show_my_catalog_items.html

# Required Libraries and Dependencies
The project code requires the following software:

	Python 2.7.x
	SQLAlchemy 0.8.4 or higher (a Python SQL toolkit)
	Flask 0.10.1 or higher (a web development microframework)
	HTML, CSS, Bootstrap, SQLite

The following Python packages:
	requests
	httplib2

# How to Run the Project

	1. Download and install Vagrant.

	2. Download and install VirtualBox.

	3. Clone or download the Vagrant VM configuration file from here.

	4. Open the above directory and navigate to the vagrant/ sub-directory.

	5. Open terminal, and type

	   vagrant up
	   
	   This will cause Vagrant to download the Ubuntu operating system and install it. This may take quite a while depending on how fast your Internet connection is.

	6. After the above command succeeds, connect to the newly created VM by typing the following command:

	 	vagrant ssh

		Type cd /vagrant/ to navigate to the shared repository.

	7. Download or clone this repository, and navigate to it.

	8. Install or upgrade Flask:

		sudo python3 -m pip install --upgrade flask

	9. Install httplib2
		sudo pip install httplib2

	10. Install request package

		sudo pip install requests

	11. Run the following command to set up the database:

		python database_setup.py

	12. Run the following command to populate some data in the database

	    python populate_data.py

	    This will create a file called womenswearcatalog.db in the catalog folder

	13. Run this application

		python3 views.py

	14. Open http://localhost:5000/ in your favourite Web browser.

# JSON Endpoints
The following are open to the public:

## Returns the whole catalog. It displays all items belongs to all catagory
  /items/JSON - 

## Returns all items belongs to a specific category
   /<int:category_id>/items/JSON

## Returns all items belongs to a specific user
  /items/<user_id>/JSON 
  - 
## Displays all user details
   /users/JSON 


