from conn_conf import client

db = client.proyecto_sinf
cpaises = db.paises
cnoticias = db.noticias

def insert_pais(update):
	cpaises.insert({"usuario_id":update.message.chat.id,
                 "edad":update.message.text})


def update_user(update):
    cpaises.update({"usuario_id": update.message.chat.id}, {"$push": {"cplicula":update.message.text}})


def pais_exists(update):
    try:
        bol = False
        if cpaises.find({"nombrePais": update.message.text}).count() > 0:
            bol = True
        return bol
    except Exception as e:
        return bol

		
def getNoticia(): 
	try: 
		noticia = cnoticias.find({'n_analisis':{'$lt':5} }).sort('n_analisis',1).limit(1)[0]
		return noticia
	except Exception as e:
	return None
	
def getTitular(noticia):
	return noticia['titular']
	
def getCuerpo(noticia):
	return noticia['cuerpo']
	
def marcarNoticia(noticia): 
	cnoticias.update(
		{
			'item_id' : noticia['item_id'] 
		}, 
		{
			'$set' : {'invalida':true}
		}
	)
	
def clasificaPais(update, noticia): 
	nombre_pais = update.message.text
	cnoticias.update(
		{
			'item_id' : noticia['item_id'] 
		}, 
		{
			'$push': {'posibles_paises': nombre_pais}	
		}
	)