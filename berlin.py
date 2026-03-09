import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8644991977:AAH2A2lE2Azg4N-62n9sXSkyI4rdgHVMSos"
bot = telebot.TeleBot(TOKEN)

# данные
total = {}
history = {}

PERCENT = 10


# меню
def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("💰 Показать сумму", callback_data="show_sum"),
        InlineKeyboardButton("🔄 Сбросить", callback_data="reset")
    )
    return markup


# старт
@bot.message_handler(commands=['start','menu'])
def start(message):
    chat_id = message.chat.id

    total.setdefault(chat_id, 0)
    history.setdefault(chat_id, [])

    bot.send_message(
        chat_id,
        "🤖 *BERLIN_bot*\n\n"
        "Отправляй числа прямо в чат:\n\n"
        "➕ `+5000` — прибавить (минус 10%)\n"
        "➖ `-2000` — вычесть\n\n"
        "📊 Бот работает в группах без тега.",
        parse_mode="Markdown",
        reply_markup=menu_markup()
    )


# кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id

    total.setdefault(chat_id, 0)
    history.setdefault(chat_id, [])

    if call.data == "show_sum":

        hist = "\n".join(history[chat_id][-5:]) if history[chat_id] else "История пуста"

        bot.send_message(
            chat_id,
            f"💰 *Общая сумма:* {round(total[chat_id],2)}\n\n"
            f"📜 *Последние операции:*\n{hist}",
            parse_mode="Markdown"
        )

    elif call.data == "reset":

        total[chat_id] = 0
        history[chat_id] = []

        bot.send_message(
            chat_id,
            "🔄 *Сумма обнулена!*",
            parse_mode="Markdown"
        )


# обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    chat_id = message.chat.id
    text = message.text.strip()

    total.setdefault(chat_id, 0)
    history.setdefault(chat_id, [])

    try:

        # ПЛЮС
        if text.startswith("+"):

            num = float(text.replace("+",""))

            result = num * (1 - PERCENT/100)

            total[chat_id] += result

            history[chat_id].append(f"➕ {num} → {round(result,2)}")

            bot.reply_to(
                message,
                f"➕ {num}\n"
                f"💸 -{PERCENT}% = {round(result,2)}\n"
                f"💰 Сумма: {round(total[chat_id],2)}"
            )


        # МИНУС
        elif text.startswith("-"):

            num = float(text)

            total[chat_id] += num

            history[chat_id].append(f"➖ {abs(num)}")

            bot.reply_to(
                message,
                f"➖ {abs(num)}\n"
                f"💰 Сумма: {round(total[chat_id],2)}"
            )

    except:
        pass


print("BERLIN_bot запущен...")
bot.polling(none_stop=True)