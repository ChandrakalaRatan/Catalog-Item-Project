"""Populate catalog database with some initial content.
This application stores women wears of various categories.
Six categories and some items for each category are created.
This script should only be run on an empty database.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from database_setup import User, Base, Category, Item


def populateData():
    """Populate the item catalog database with some initial content."""
    engine = create_engine('sqlite:///womenswearcatalog.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    # Make sure the database is empty before running this inital data dump.
    category_count = session.query(func.count(Category.id)).scalar()
    if category_count > 0:
        session.close()
        return

    # Create the 6 categories for women clothings.
    Wcategory1 = Category(name="Western Wear")
    session.add(Wcategory1)
    session.commit()

    Wcategory2 = Category(name="Indian & Fusion Wear")
    session.add(Wcategory2)
    session.commit()

    Wcategory3 = Category(name="SportsWear")
    session.add(Wcategory3)
    session.commit()

    Wcategory4 = Category(name="Lingerie and SleepWear")
    session.add(Wcategory4)
    session.commit()

    Wcategory5 = Category(name="FootWear")
    session.add(Wcategory5)
    session.commit()

    Wcategory6 = Category(name="Accessories")
    session.add(Wcategory6)
    session.commit()

    # Create a dummy user for these initial items
    user1 = User(name="Chandrakala Null", email="justforjobs42@gmail.com")
    session.add(user1)
    session.commit()

    item1 = Item(
        user=user1,
        category=Wcategory1,
        name="Dresses & Jumpsuits",
        description=(
            "Women Printed Maxi Dress"
        ),
        quantity=3,
        price="$10",
        image_filename="PrintedMaxi.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/v1/'
                  'assets/images/7164915/2018/8/21/44d85481-0cc4-466c-'
                  '9d76-6a4e7dcf2b051534862104375-Libas-Women-Green--'
                  'Brown-Printed-A-Line-Dress-1491534862104234-1.jpg'
    )
    session.add(item1)
    session.commit()

    item2 = Item(
        user=user1,
        category=Wcategory1,
        name="Jeans & Jeggings",
        description=(
            "Women Slim Fit Solid Treggings"
        ),
        quantity=6,
        price="$15",
        image_filename="SolidTreggings.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/'
                  'v1/assets/images/4446473/2018/5/16/5f75067f-a2b1-4ae6'
                  '-abcb-0783bc7757eb1526463738968-High-Star-Women-Black'
                  '-Slim-Fit-High-Rise-Clean-Look-Jeans-3571526463738816-1.jpg'
    )
    session.add(item2)
    session.commit()

    item3 = Item(
        user=user1,
        category=Wcategory1,
        name="Tops, T-Shirts & Shirts",
        description=(
            "Printed A-Line Top"
        ),
        quantity=3,
        price="$8",
        image_filename="ALineTop.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/v1/'
                  'assets/images/5617724/2018/5/3/11525347083659-na-'
                  '9791525347083466-1.jpg'
    )
    session.add(item3)
    session.commit()

    item4 = Item(
        user=user1,
        category=Wcategory1,
        name="Trousers & Capris",
        description=(
            "Women Track Pants"
        ),
        quantity=39,
        price="$12",
        image_filename="TrackPants.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/v1/'
                  'assets/images/7188663/2018/8/24/c70d7f9e-ac4f-4c37-b5a2'
                  '-7af7ed7958011535098484143-SASSAFRAS-Women-Trousers-'
                  '6191535098484031-1.jpg'
    )
    session.add(item4)
    session.commit()

    item5 = Item(
        user=user1,
        category=Wcategory1,
        name="Shorts & Skirts",
        description=(
            "Women Printed Pencil Skirt"
        ),
        quantity=30,
        price="$19",
        image_filename="PencilSkrit.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/'
                  'v1/assets/images/7188665/2018/8/24/105cd86a-9536-'
                  '4488-833f-bad71277d5851535100643805-SASSAFRAS-Women-'
                  'Skirts-4851535100643620-1.jpg'
    )
    session.add(item5)
    session.commit()

    item6 = Item(
        user=user1,
        category=Wcategory1,
        name="Shrugs",
        description=(
            "Longline Open Front Shrug"
        ),
        quantity=6,
        price="$14",
        image_filename="FrontShrug.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/v1/'
                  'assets/images/7509718/2018/10/6/c0b28959-6664-4ef8-a128'
                  '-a4f21e8504691538817641038-Athena-Women-Shrug-'
                  '8411538817640860-1.jpg'
    )
    session.add(item6)
    session.commit()

    item7 = Item(
        user=user1,
        category=Wcategory2,
        name="Kurtas & Suits",
        description=(
            "Printed Straight Kurta"
        ),
        quantity=3,
        price="$10",
        image_filename="StraightKurta.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/'
                  'v1/assets/images/2528325/2018/3/15/11521096428996-'
                  'Libas-Women-Kurtas-871521096428801-1.jpg'
    )
    session.add(item7)
    session.commit()

    item8 = Item(
        user=user1,
        category=Wcategory2,
        name="Kurtis, Tunics & Tops",
        description=(
            "South Cotton Top with Gathers"
        ),
        quantity=6,
        price="$15",
        image_filename="Gathers.jpg",
        image_url='https://assets.myntassets.com/h_1440,q_100,w_1080/'
                  'v1/assets/images/4326336/2018/3/29/11522319305353-GERUA'
                  '-Women-Kurtis-7851522319305173-1.jpg'
    )
    session.add(item8)
    session.commit()

    item9 = Item(
        user=user1,
        category=Wcategory2,
        name="Ethnic Dresses",
        description=(
            "Women Printed Maxi Dress"
        ),
        quantity=3,
        price="$8",
        image_filename="MaxiDress.jpg",
        image_url=''
    )
    session.add(item9)
    session.commit()

    item10 = Item(
        user=user1,
        category=Wcategory2,
        name="Sarees & Blouses",
        description=(
            "Solid Kanjeevaram Saree"
        ),
        quantity=39,
        price="$12",
        image_filename="Saree.jpg",
        image_url=''
    )
    session.add(item10)
    session.commit()

    item11 = Item(
        user=user1,
        category=Wcategory2,
        name="Dupattas & Shawls",
        description=(
            "Woven Design Shawl"
        ),
        quantity=30,
        price="$19",
        image_filename="Shawl.jpg",
        image_url=''
    )
    session.add(item11)
    session.commit()

    item12 = Item(
        user=user1,
        category=Wcategory2,
        name="Lehenga Choli",
        description=(
            "Semi-Stitched Lehengas"
        ),
        quantity=6,
        price="$14",
        image_filename="Lehengas.jpg",
        image_url=''
    )
    session.add(item12)
    session.commit()

    item13 = Item(
        user=user1,
        category=Wcategory3,
        name="Sports Accessories",
        description=(
            "Unisex Solid Backpack"
        ),
        quantity=3,
        price="$10",
        image_filename="Backpack.jpg",
        image_url=''
    )
    session.add(item13)
    session.commit()

    item14 = Item(
        user=user1,
        category=Wcategory3,
        name="Sports Equipment",
        description=(
            "Unisex Unstrung Tennis Racquet"
        ),
        quantity=6,
        price="$15",
        image_filename="TennisRacquet.jpg",
        image_url=''
    )
    session.add(item14)
    session.commit()

    item15 = Item(
        user=user1,
        category=Wcategory3,
        name="Sports Foot Wear",
        description=(
            "Superfly 6 Club CR7 Football Shoes"
        ),
        quantity=3,
        price="$8",
        image_filename="FootballShoes.jpg",
        image_url=''
    )
    session.add(item15)
    session.commit()

    item16 = Item(
        user=user1,
        category=Wcategory4,
        name="Bras & Lingerie Sets",
        description=(
            "Blue solid spoers bra."
            "Signature Moisture Transport "
            "System wicks sweat to keep you dry & light."
        ),
        quantity=3,
        price="$10",
        image_filename="sportsbra.jpg",
        image_url=''
    )
    session.add(item16)
    session.commit()

    item17 = Item(
        user=user1,
        category=Wcategory4,
        name="Briefs",
        description=(
            "Pack of 2 Boy Shorts"
        ),
        quantity=6,
        price="$15",
        image_filename="BoyShorts.jpg",
        image_url=''
    )
    session.add(item17)
    session.commit()

    item18 = Item(
        user=user1,
        category=Wcategory4,
        name="Shapewear",
        description=(
            "Hour Glass Black Seamless High Hip Shapewear"
        ),
        quantity=3,
        price="$8",
        image_filename="HighHipShapewear.jpg",
        image_url=''
    )
    session.add(item18)
    session.commit()

    item19 = Item(
        user=user1,
        category=Wcategory4,
        name="Sleepwear & Loungewear",
        description=(
            "Women Checked Pyjama"
        ),
        quantity=39,
        price="$12",
        image_filename="CheckedPyjama.jpg",
        image_url=''
    )
    session.add(item19)
    session.commit()

    item20 = Item(
        user=user1,
        category=Wcategory4,
        name="Swimwear",
        description=(
            "Womens Swimwear Set"
        ),
        quantity=30,
        price="$19",
        image_filename="SwimwearSet.jpg",
        image_url=''
    )
    session.add(item20)
    session.commit()

    item21 = Item(
        user=user1,
        category=Wcategory4,
        name="Camisoles & Thermals",
        description=(
            "Women Thermal Set"
        ),
        quantity=6,
        price="$14",
        image_filename="ThermalSet.jpg",
        image_url=''
    )
    session.add(item21)
    session.commit()

    item22 = Item(
        user=user1,
        category=Wcategory5,
        name="Flats & Casual Shoes",
        description=(
            "Women Sneakers"
        ),
        quantity=3,
        price="$10",
        image_filename="CasualShoes.jpg",
        image_url=''
    )
    session.add(item22)
    session.commit()

    item23 = Item(
        user=user1,
        category=Wcategory5,
        name="Heels",
        description=(
            "Steve Madden"
        ),
        quantity=6,
        price="$15",
        image_filename="SteveMadden.jpg",
        image_url=''
    )
    session.add(item23)
    session.commit()

    item24 = Item(
        user=user1,
        category=Wcategory5,
        name="Boots",
        description=(
            "Shoetopia"
        ),
        quantity=3,
        price="$8",
        image_filename="Shoetopia.jpg",
        image_url=''
    )
    session.add(item24)
    session.commit()

    item25 = Item(
        user=user1,
        category=Wcategory6,
        name="Handbags",
        description=(
            "Solid Handheld Bag"
        ),
        quantity=39,
        price="$12",
        image_filename="HandheldBag.jpg",
        image_url=''
    )
    session.add(item25)
    session.commit()

    item26 = Item(
        user=user1,
        category=Wcategory6,
        name="Bags & Wallets",
        description=(
            "Women Colourblocked Sling Bag"
        ),
        quantity=30,
        price="$19",
        image_filename="SlingBag.jpg",
        image_url=''
    )
    session.add(item26)
    session.commit()

    item27 = Item(
        user=user1,
        category=Wcategory6,
        name="Watches & Wearables",
        description=(
            "Women Analogue Watch"
        ),
        quantity=6,
        price="$14",
        image_filename="AnalogueWatch.jpg",
        image_url=''
    )
    session.add(item27)
    session.commit()
    session.close()
    print "Populated database with some items"


if __name__ == '__main__':
    populateData()
