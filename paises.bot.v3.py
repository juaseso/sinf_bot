import logging
from time import sleep
from store import getNoticia, getTitular, getCuerpo, marcarNoticia, clasificaPais, paisExists
from telegramkey import Token
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler, Handler


noticia = {}
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
CLASIFICAR_INI, CLASIFICAR_TITULO_SUFICIENTE, CLASIFICAR_CUERPO_SUFICIENTE, CLASIFICAR_PAIS = range(4)

def inicio(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="Hola {}, ¿Quieres clasificar una noticia?".format(update.message.chat.first_name))
	return CLASIFICAR_INI

def clasificar_ini(bot, update):
	global noticia 
	noticia = getNoticia()
	return decisor(1, bot, update)

def clasificar_titulo_suficiente(bot, update): 
	return decisor(2, bot, update)

def clasificar_cuerpo_suficiente(bot, update): 
	return decisor(4, bot, update)

def clasificar_pais(bot, update):
	if paisExists(update): 
		clasificaPais(update, noticia)
		bot.sendMessage(chat_id=update.message.chat.id, text='Noticia clasificada correctamente, gracias por participar.')
		return decisor(3,bot,update)
	else: 
		bot.sendMessage(chat_id=update.message.chat.id, text='El país introducido no existe, prueba de nuevo sin usar acentos o caracteres no alfabéticos')
		return CLASIFICAR_PAIS

def decisor(d, bot, update): 

	# Decision 1: Pregunta si quiere clasificar una noticia
	if d == 1: 
		if update.message.text.lower() == 'si' or update.message.text.lower() == 'sí':
			bot.sendMessage(chat_id=update.message.chat.id, text="Titular: "+getTitular(noticia))
			bot.sendMessage(chat_id=update.message.chat.id, text="¿Es posible decir a qué país pertenece con esta información?")
			return CLASIFICAR_TITULO_SUFICIENTE
		else:
			bot.sendMessage(chat_id=update.message.chat.id, text="Gracias, hasta luego!")
			return ConversationHandler.END

			
	# Decision 2: Pregunta si con el titular es suficiente para dar una respuesta
	elif d == 2:
		if update.message.text.lower() == 'si' or update.message.text.lower() == 'sí':
			bot.sendMessage(chat_id=update.message.chat.id, text="1-Introduce el nombre del país, por favor")
			return CLASIFICAR_PAIS
		else:
			cuerpo = text=getCuerpo(noticia)
			for linea in cuerpo: 
				bot.sendMessage(chat_id=update.message.chat.id, text = linea)
				sleep(0.5)
			bot.sendMessage(chat_id=update.message.chat.id, text="¿Es posible decir a qué país pertenece con esta información?")
			return CLASIFICAR_CUERPO_SUFICIENTE
			
			
	# Decision 3: Pregunta si desea seguir clasificando noticias
	elif d == 3: 
		bot.sendMessage(chat_id=update.message.chat.id, text='¿Quieres seguir clasificando noticias?')
		return CLASIFICAR_INI
		
		
	# Decision 4: Pregunta si el cuerpo es suficiente para dar una respuesta
	elif d == 4: 
		if update.message.text.lower() == 'si' or update.message.text.lower() == 'sí':
			bot.sendMessage(chat_id=update.message.chat.id, text="Introduce el nombre del país, por favor")
			return CLASIFICAR_PAIS
		else: 
			bot.sendMessage(chat_id=update.message.chat.id, text="Noticia marcada como no clasificable para su revisión.")
			marcarNoticia(noticia)
			bot.sendMessage(chat_id=update.message.chat.id, text='¿Quieres seguir clasificando noticias?')
			return CLASIFICAR_INI

def cancel(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="Conversación reiniciada")
	return ConversationHandler.END

def main():
    update = Updater(str(Token))
    conversacion = ConversationHandler(entry_points=[CommandHandler("inicio", inicio)],
										states={
											CLASIFICAR_INI: [MessageHandler(Filters.text, clasificar_ini)],
											CLASIFICAR_TITULO_SUFICIENTE: [MessageHandler(Filters.text, clasificar_titulo_suficiente)],
											CLASIFICAR_CUERPO_SUFICIENTE: [MessageHandler(Filters.text, clasificar_cuerpo_suficiente)],
											CLASIFICAR_PAIS: [MessageHandler(Filters.text, clasificar_pais)],
											   },
                                       fallbacks=[CommandHandler('cancelar', cancel)])
	
    update.dispatcher.add_handler(conversacion)
    update.start_polling()
    update.idle()

if __name__ == '__main__':
    main()
