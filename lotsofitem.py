import codecs
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import helpers
from database_setup import Base, User, CatalogItem

#engine = create_engine('sqlite:///catalogitem.db')
engine = create_engine('postgresql+psycopg2://catalog:logacat@localhost/itemcatalog')
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
password = 'password'

f = list(codecs.open('names.txt', encoding='utf-8-sig', mode='rb'))
# Menu for UrbanBurger
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$7.50", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()


catalogItem1 = CatalogItem(name="French Fries", description="with garlic and parmesan",
                     price="$2.99", category="Appetizer", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chicken Burger", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                     price="$5.50", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Chocolate Cake", description="fresh baked and served with ice cream",
                     price="$3.99", category="Dessert", user=user1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Sirloin Burger", description="Made with grade A beef",
                     price="$7.99", category="Entree", user=user1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Root Beer", description="16oz of refreshing goodness",
                     price="$1.99", category="Beverage", user=user1)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(name="Iced Tea", description="with Lemon",
                     price="$.99", category="Beverage", user=user1)

session.add(catalogItem6)
session.commit()

catalogItem7 = CatalogItem(name="Grilled Cheese Sandwich", description="On texas toast with American Cheese",
                     price="$3.49", category="Entree", user=user1)

session.add(catalogItem7)
session.commit()

catalogItem8 = CatalogItem(name="Veggie Burger", description="Made with freshest of ingredients and home grown spices",
                     price="$5.99", category="Entree", user=user1)

session.add(catalogItem8)
session.commit()


# Menu for Super Stir Fry
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user2 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user2)
session.commit()


catalogItem1 = CatalogItem(name="Chicken Stir Fry", description="With your choice of noodles vegetables and sauces",
                     price="$7.99", category="Entree", user=user2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(
    name="Peking Duck", description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", price="$25", category="Entree", user=user2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Spicy Tuna Roll", description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
                     price="15", category="Entree", user=user2)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Nepali Momo ", description="Steamed dumplings made with vegetables, spices and meat. ",
                     price="12", category="Entree", user=user2)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     price="14", category="Entree", user=user2)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(name="Ramen", description="a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
                     price="12", category="Entree", user=user2)

session.add(catalogItem6)
session.commit()


# Menu for Panda Garden
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()


catalogItem1 = CatalogItem(name="Pho", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
                     price="$8.99", category="Entree", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chinese Dumplings", description="a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
                     price="$6.99", category="Appetizer", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Gyoza", description="The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner",
                     price="$9.95", category="Entree", user=user1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Stinky Tofu", description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
                     price="$6.99", category="Entree", user=user1)

session.add(catalogItem4)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$9.50", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()


# Menu for Thyme for that
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()


catalogItem1 = CatalogItem(name="Tres Leches Cake", description="Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.",
                     price="$2.99", category="Dessert", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Mushroom risotto", description="Portabello mushrooms in a creamy risotto",
                     price="$5.99", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Honey Boba Shaved Snow", description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi",
                     price="$4.50", category="Dessert", user=user1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Cauliflower Manchurian", description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
                     price="$6.95", category="Appetizer", user=user1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Aloo Gobi Burrito", description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom",
                     price="$7.95", category="Entree", user=user1)

session.add(catalogItem5)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$6.80", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()


# Menu for Tony's Bistro
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()


catalogItem1 = CatalogItem(name="Shellfish Tower", description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
                     price="$13.95", category="Entree", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chicken and Rice", description="Chicken... and rice",
                     price="$4.95", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Mom's Spaghetti", description="Spaghetti with some incredible tomato sauce made by mom",
                     price="$6.95", category="Entree", user=user1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
                     description="Milk, cream, salt, ..., Liquid nitrogen magic", price="$3.95", category="Dessert", user=user1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Tonkatsu Ramen", description="Noodles in a delicious pork-based broth with a soft-boiled egg",
                     price="$7.95", category="Entree", user=user1)

session.add(catalogItem5)
session.commit()


# Menu for Andala's
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()


catalogItem1 = CatalogItem(name="Lamb Curry", description="Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.",
                     price="$9.95", category="Entree", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chicken Marsala", description="Chicken cooked in Marsala wine sauce with mushrooms",
                     price="$7.95", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Potstickers", description="Delicious chicken and veggies encapsulated in fried dough.",
                     price="$6.50", category="Appetizer", user=user1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Nigiri Sampler", description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
                     price="$6.75", category="Appetizer", user=user1)

session.add(catalogItem4)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$7.00", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()


# Menu for Auntie Ann's
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()

catalogItem9 = CatalogItem(name="Chicken Fried Steak", description="Fresh battered sirloin steak fried and smothered with cream gravy",
                     price="$8.99", category="Entree", user=user1)

session.add(catalogItem9)
session.commit()


catalogItem1 = CatalogItem(name="Boysenberry Sorbet", description="An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness",
                     price="$2.99", category="Dessert", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Broiled salmon", description="Salmon fillet marinated with fresh herbs and broiled hot & fast",
                     price="$10.95", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Morels on toast (seasonal)", description="Wild morel mushrooms fried in butter, served on herbed toast slices",
                     price="$7.50", category="Appetizer", user=user1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Tandoori Chicken", description="Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.",
                     price="$8.95", category="Entree", user=user1)

session.add(catalogItem4)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$9.50", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

catalogItem10 = CatalogItem(name="Spinach Ice Cream", description="vanilla ice cream made with organic spinach leaves",
                      price="$1.99", category="Dessert", user=user1)

session.add(catalogItem10)
session.commit()


# Menu for Cocina Y Amor
name = random.choice(f).replace('\r\n', '').replace(' ', '_')
hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])

session.add(user1)
session.commit()


catalogItem1 = CatalogItem(name="Super Burrito Al Pastor", description="Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla",
                     price="$5.95", category="Entree", user=user1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Cachapa", description="Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ",
                     price="$7.99", category="Entree", user=user1)

session.add(catalogItem2)
session.commit()

hashbrown = helpers.make_pw_hash(name, password)
user1 = User(name=name, salt=hashbrown.split('|')[1], hashedpw=hashbrown.split('|')[0])
session.add(user1)
session.commit()

catalogItem1 = CatalogItem(name="Chantrelle Toast", description="Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms",
                     price="$5.95", category="Appetizer", user=user1)

session.add(catalogItem1)
session.commit

catalogItem1 = CatalogItem(name="Guanciale Chawanmushi", description="Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)",
                     price="$6.95", category="Dessert", user=user1)

session.add(catalogItem1)
session.commit()


catalogItem1 = CatalogItem(name="Lemon Curd Ice Cream Sandwich", description="Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews",
                     price="$4.25", category="Dessert", user=user1)

session.add(catalogItem1)
session.commit()


print "added menu items!"
