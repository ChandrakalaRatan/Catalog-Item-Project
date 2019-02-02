"""Database setup is for Udacity Nano Degree Item Catalog project.
This script should be run first  to create tables in the database.
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# Get the base class mapper from SQLalchemy
Base = declarative_base()


class User(Base):
    """This database table to stored registered users.
    Column Names:
        __tablename__: A string naming the underlining SQL table.
        id: A column in the database for the user ID.
        name: A column for the name of the user.
        email: A column for the user's email.
        picture:  A column to store the URL of the user's profile picture.
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    picture = Column(String(250))
    @property
    def serialise(self):
        """Returns category data in an easily serialiseable format."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


class Category(Base):
    """This database table is to store categories that an Items will belong to.
    Column Names:
        __tablename__: A string naming the underlining SQL table.
        id: A column in the database for the category ID.
        name: A column for the name of the category.
        items: A relationship with Items.

        user_id: A column to store the user ID of the owner of an item.
        user: Make a one-to-one relationship to the User class.
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    items = relationship('Item', cascade="save-update, merge, delete")

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialise(self):
        """Returns category data in an easily serialiseable format."""
        return {
            'id': self.id,
            'name': self.name,
            'items': [i.serialise for i in self.items]
        }


class Item(Base):
    """This database table is to store all the items for a
            particular category on a particular section.
    Column Names:
        __tablename__: A string naming the underlining SQL table.
        id: A column in the database for the item ID.
        name: A column to store the name of the item.
        description: A column to store a description of the item.
        quantity: Number of items.
        price: A column to store the price of an item

        category_id: A column to store the ID of the category that the item
            belongs to.
        category: Makes a one-to-one relationship to the Category class.

        user_id: A column to store the user ID of the owner of an item.
        user: Make a one-to-one relationship to the User class.
    """
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String)
    quantity = Column(Integer)
    price = Column(String(8), nullable=False)

    image_filename = Column(String(100))
    image_url = Column(String(250))

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialise(self):
        """Returns item data in an easily serialiseable format."""
        return {
            'id': self.id,
            'category_id': self.category_id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'user_id': self.user_id
        }


engine = create_engine('sqlite:///womenswearcatalog.db')
Base.metadata.create_all(engine)
