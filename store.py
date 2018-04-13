from conn_conf import client

db = client.proyecto_sinf
cpaises = db.paises
cnoticias = db.noticias

def paisExists(update):
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
		
		
def getNoticiaFalsa(): 
	try: 
		noticia = cnoticias.find({'n_analisis':{'$eq':3} }).sort('n_analisis',1).limit(1)[0]
		return noticia
	except Exception as e:
		return None

def getTitular(noticia):
	titular = noticia['titular']
	return titular

def getCuerpo(noticia):
	return noticia['cuerpo']

def marcarNoticia(noticia): 
	cnoticias.update({'item_id' : noticia['item_id']}, {'$set' : {'invalida': True }})

def clasificaPais(update, noticia): 
	nombre_pais = update.message.text
	cnoticias.update({'item_id' : noticia['item_id']}, {'$push': {'posibles_paises': nombre_pais}})