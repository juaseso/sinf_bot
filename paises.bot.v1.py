import logging
import store
from telegramkey import Token
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler, Handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

D1, TITULAR, FIN = range(3)


def inicio(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="hola {} ¿Quieres clasificar una noticia?".format(update.message.chat.first_name))
	return D1

def decision1(bot, update):
	if update.message.text.lower() == 'si' or update.message.text.lower() == 'sí':
		return TITULAR
	else: 
		return FIN


def titular (bot, update): 
	bot.sendMessage(chat_id=update.message.chat.id, text="Esto es un Titular, fin")
	return ConversationHandler.END

def fin(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="Gracias, hasta luego!")
	return ConversationHandler.END



def cancel(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="lastima puedes entrar mas tarde")
	return ConversationHandler.END


def main():
    update = Updater(str(Token))
    conversacion = ConversationHandler(entry_points=[CommandHandler("inicio", inicio)],
										states={
											D1: [MessageHandler(Filters.text, decision1)],
											TITULAR: [Handler(titular)],
											FIN: [MessageHandler(Filters.text, fin)],
											   },
                                       fallbacks=[CommandHandler('cancelar', cancel)])
	
    update.dispatcher.add_handler(conversacion)
    update.start_polling()
    update.idle()


if __name__ == '__main__':
    main()
