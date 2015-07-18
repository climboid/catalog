from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///cataloglist.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create a dummy user
User1 = User(name="Oscar Villarreal", email="oscarvillarreal14@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category Items for APP dummy data
## Different categories contain different items. For instance soccer and its
## game components ball and shoes.
#

# Soccer category dummy APP Data
soccer = Category(name="Soccer")

session.add(soccer)
session.commit()

soccer_item1 = CategoryItem(
    name="Shoes",
    description="""Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. """,
    category=soccer)

session.add(soccer_item1)
session.commit()

soccer_item2 = CategoryItem(
    name="Ball",
    description="""A football, or association football ball is the ball used in the sport of association football. """,
    category=soccer)

session.add(soccer_item2)
session.commit()

#
# Basketball category dummy APP Data
#
basketball = Category(name="Basketball")

session.add(basketball)
session.commit()

basketball_item1 = CategoryItem(
    name="Shoes",
    description="""Athletic shoe is a generic name for the footwear primarily designed for sports or other forms of physical exercise, but in recent years has come to be used for casual everyday activities.""",
    category=basketball)

session.add(basketball_item1)
session.commit()

basketball_item2 = CategoryItem(
    name="Basketball",
    description="""A basketball is a spherical inflated ball used in a game of basketball. """,
    category=basketball)

session.add(basketball_item2)
session.commit()

#
# Baseball category dummy APP Data
#
baseball = Category(name="Baseball")

session.add(baseball)
session.commit()

baseball_item1 = CategoryItem(
    name="Bat",
    description="""A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher. """,
    category=baseball)

session.add(baseball_item1)
session.commit()

baseball_item2 = CategoryItem(
    name="Cap",
    description="""A baseball cap is a type of soft cap with a rounded crown and a stiff peak projecting in front. """,
    category=baseball)

session.add(baseball_item2)
session.commit()

#
# Frisbee category dummy APP Data
#
frisbee = Category(name="Frisbee")

session.add(frisbee)
session.commit()

frisbee_item1 = CategoryItem(
    name="Flying Disk",
    description=""""Frisbee" redirects here. For the sport, see Ultimate (sport). """,
    category=frisbee)

session.add(frisbee_item1)
session.commit()

frisbee_item2 = CategoryItem(
    name="Shorts",
    description="""Shorts are a garment worn by both men and women over their pelvic area, circling the waist and splitting to cover the upper part of the legs, sometimes extending down to knee but not covering the entire length of the leg.""",
    category=frisbee)

session.add(frisbee_item2)
session.commit()

#
# Snowboarding category dummy APP Data
#
snowboarding = Category(name="Snowboarding")

session.add(snowboarding)
session.commit()

snowboarding_item1 = CategoryItem(
    name="Snowboard",
    description=""""Snowboards are boards that are usually the width of one's foot longways, with the ability to glide on snow.[1]""",
    category=snowboarding)

session.add(snowboarding_item1)
session.commit()

snowboarding_item2 = CategoryItem(
    name="Ski suit",
    description="""A ski suit is a suit made to be worn over the rest of the clothes when skiing or snowboarding.[1] """,
    category=snowboarding)

session.add(snowboarding_item2)
session.commit()

#
# Rockclimbing category dummy APP Data
#
rockclimbing = Category(name="Rockclimbing")

session.add(rockclimbing)
session.commit()

rockclimbing_item1 = CategoryItem(
    name="Carabinier",
    description=""""A carabinier (also sometimes spelled carabineer or carbineer) (carabinero in Spanish, carabiniere in Italian) is in principle a soldier armed with a carbine. """,
    category=rockclimbing)

session.add(rockclimbing_item1)
session.commit()

rockclimbing_item2 = CategoryItem(
    name="Harness",
    description="""A harness is a looped restraint or support. Specifically, it may refer to one of the following harness """,
    category=rockclimbing)

session.add(rockclimbing_item2)
session.commit()



print "added category items!"
