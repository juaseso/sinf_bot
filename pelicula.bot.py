import logging
import store
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

PELICULA, END = range(2)


def inicio(bot, update):
    if not store.user_exists(update):
        bot.sendMessage(chat_id=update.message.chat.id,
                    text="hola {} ¿Me puedes decir tu edad?".format(update.message.chat.first_name))
        return PELICULA
    else:
        bot.sendMessage(chat_id=update.message.chat.id, text="¿qué pelis te gustan?")
        return END


def pelicula(bot, update):
    store.insert_user(update)
    bot.sendMessage(chat_id=update.message.chat.id, text="¿qué pelis te gustan?")
    return END


def end(bot, update):
    store.update_user(update)
    bot.sendMessage(chat_id=update.message.chat.id, text="hasta otra")
    return ConversationHandler.END


def cancel(bot, update):
    bot.sendMessage(chat_id=update.message.chat.id, text="lastima puedes entrar mas tarde")
    return ConversationHandler.END


def main():
    update = Updater(Token)
    conversacion = ConversationHandler(entry_points=[CommandHandler("inicio", inicio)],
                                       states={PELICULA: [MessageHandler(Filters.text, pelicula)],
                                               END: [MessageHandler(Filters.text, end)]},
                                       fallbacks=[CommandHandler('cancelar', cancel)])
    update.dispatcher.add_handler(conversacion)
    update.start_polling()
    update.idle()


if __name__ == '__main__':
    main()
