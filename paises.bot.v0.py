import logging
import store
from telegramkey import Token
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

PAIS, FIN = range(2)


def inicio(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="hola {} ¿Me puedes decir un nombre de pais?".format(update.message.chat.first_name))
	print('funcion inicio')
	return PAIS


def pais(bot, update):
	if store.pais_exists(update):
		bot.sendMessage(chat_id=update.message.chat.id, text="Es un país!")
		bot.sendMessage(chat_id=update.message.chat.id, text="¿Quieres volver a introducir un pais?")
		return FIN
	else: 
		bot.sendMessage(chat_id=update.message.chat.id, text="No es un país : ( ")
		bot.sendMessage(chat_id=update.message.chat.id, text="¿Quieres volver a intentarlo?")
		return FIN
	

def fin(bot, update):
	if update.message.text == 'si':
		bot.sendMessage(chat_id=update.message.chat.id, text="Inserta un nombre de pais")
		return PAIS
	else: 
		bot.sendMessage(chat_id=update.message.chat.id, text="hasta otra")
		return ConversationHandler.END


def cancel(bot, update):
	bot.sendMessage(chat_id=update.message.chat.id, text="lastima puedes entrar mas tarde")
	return ConversationHandler.END


def main():
    update = Updater(str(Token))
    conversacion = ConversationHandler(entry_points=[CommandHandler("inicio", inicio)],
                                       states={PAIS: [MessageHandler(Filters.text, pais)],
                                               FIN: [MessageHandler(Filters.text, fin)]},
                                       fallbacks=[CommandHandler('cancelar', cancel)])
    update.dispatcher.add_handler(conversacion)
    update.start_polling()
    update.idle()


if __name__ == '__main__':
    main()
