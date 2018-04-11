from conn_conf import client

db = client.proyecto_sinf
cpaises = db.paises

def insert_pais(update):
	cpaises.insert({"usuario_id":update.message.chat.id,
                 "edad":update.message.text})


def update_user(update):
    cpaises.update({"usuario_id": update.message.chat.id}, {"$push": {"cpaisescula":update.message.text}})


def pais_exists(update):
    try:
        bol = False
        if cpaises.find({"nombrePais": update.message.text}).count() > 0:
            bol = True
        return bol
    except Exception as e:
        return bol

