from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.pelicula

peli = db.peli

def insert_user(update):
    peli.insert({"usuario_id":update.message.chat.id,
                 "edad":update.message.text})


def update_user(update):
    peli.update({"usuario_id": update.message.chat.id}, {"$push": {"pelicula":update.message.text}})


def user_exists(update):
    try:
        bol = False
        if peli.find({"usuario_id": update.message.chat.id}).count() > 0:
            bol = True
        return bol
    except Exception as e:
        return bol


