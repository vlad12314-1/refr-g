from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import requests


response = requests.get("https://openlibrary.org/search.json?q=harry+potter")
data = response.json()
print(f"Первая книга: {data['docs'][0]['title']}")

logger = logging.getLogger(__name__)


TOKEN = ""


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        ['Search Book'],
        ['Search Author'],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)


def search_book(update: Update, context: CallbackContext) -> None:
    """Prompts user for the book title."""
    update.message.reply_text('Enter the book title to search for:')
    # context.user_data['search_type'] = 'book' Сохранить тип поиска


def search_author(update: Update, context: CallbackContext) -> None:
    """Prompts user for the author name."""
    update.message.reply_text('Enter the author name to search for:')
    context.user_data['search_type'] = 'author'  # Сохранить тип поиска


def search_open_library(query: str, search_type: str) -> str:
    """Searches Open Library for books or authors."""
    try:
        base_url = "https://openlibrary.org/search.json"
        search_param = "author" if search_type == "author" else "title"  # Use 'title' for books

        params = {search_param: query, "limit": 3}  # Limiting to 3 results for brevity
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if data['numFound'] == 0:
            return "No results found."

        results = data['docs']
        message = "Here are some results:\n\n"

        for i, result in enumerate(results):
           title = result.get('title', 'Unknown Title')
           author_names = result.get('author_name', ['Unknown Author'])
           author_string = ", ".join(author_names)
           first_publish_year = result.get('first_publish_year', 'Unknown Year')

           message += f"{i+1}. {title} by {author_string} (First published: {first_publish_year})\n"
        return message

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return "Sorry, there was an error during the search."
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again later."


def handle_message(update: Update, context: CallbackContext) -> None:
    """Handles the user's search query."""
    query = update.message.text
    search_type = context.user_data.get('search_type', 'book') # По умолчанию 'book', если не найдено

    results = search_open_library(query, search_type)
    update.message.reply_text(results)


def main() -> None:
    """Start the bot."""

    # Добавляет обработчики сообщений
    dispatcher.add_handler(MessageHandler(Filters.regex('^Search Author$'), search_author))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))  # Handles messages


    # Start the Bot
    updater.start_polling()

    # “Запускайте бота до тех пор, пока не нажмете Ctrl-C или процесс не получит сигналы SIGINT,
    # SIGTERM или SIGABRT.
    # Этот способ следует использовать в большинстве случаев,
    # поскольку start_polling() является неблокирующим и корректно остановит бота.”
    updater.idle()


if __name__ == '__main__':
    main()