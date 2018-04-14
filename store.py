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
		noticia = db.noticias_dev.find({'n_analisis':{'$eq':3} }).sort('n_analisis',1).limit(1)[0]
		return noticia
	except Exception as e:
		return None

def getTitular(noticia):
	titular = noticia['titular']
	return titular

def getCuerpo(noticia):
	palabras = noticia['cuerpo'].replace('\n', ' ').split(' ')
	i = 0
	frase = ''
	frases = []
	for palabra in palabras: 
		frase = frase + palabra + ' '
		i = i + 1
		if i == 100 : 
			frases.append(frase)
			i = 0
			frase = ''
	frases.append(frase)
	return frases

def marcarNoticia(noticia): 
	cnoticias.update({'item_id' : noticia['item_id']}, {'$set' : {'invalida': True }})

def clasificaPais(update, noticia): 
	nombre_pais = update.message.text
	n_analisis = int(noticia['n_analisis']) + 1
	cnoticias.update({'item_id' : noticia['item_id']}, {'$push': {'posibles_paises': nombre_pais} })
	cnoticias.update({'item_id' : noticia['item_id']}, {'$set' : {'n_analisis': n_analisis} }  )
