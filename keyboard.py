from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_hi = KeyboardButton('Привет! 👋')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)

greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))

inline_kb_klass = InlineKeyboardMarkup()
btn_5a = InlineKeyboardButton('5А', callback_data='5а')
btn_5b = InlineKeyboardButton('5Б', callback_data='5б')
btn_5c = InlineKeyboardButton('5В', callback_data='5в')
btn_5d = InlineKeyboardButton('5Г', callback_data='5г')
btn_6a = InlineKeyboardButton('6А', callback_data='6а')
btn_6b = InlineKeyboardButton('6Б', callback_data='6б')
btn_6c = InlineKeyboardButton('6В', callback_data='6в')
btn_6d = InlineKeyboardButton('6Г', callback_data='6г')
btn_7a = InlineKeyboardButton('7А', callback_data='7а')
btn_7b = InlineKeyboardButton('7Б', callback_data='7б')
btn_7c = InlineKeyboardButton('7В', callback_data='7в')
btn_7d = InlineKeyboardButton('7Г', callback_data='7г')
btn_8a = InlineKeyboardButton('8А', callback_data='8а')
btn_8b = InlineKeyboardButton('8Б', callback_data='8б')
btn_8c = InlineKeyboardButton('8В', callback_data='8в')
btn_9a = InlineKeyboardButton('9А', callback_data='9а')
btn_9b = InlineKeyboardButton('9Б', callback_data='9б')
btn_9c = InlineKeyboardButton('9В', callback_data='9в')
btn_10a = InlineKeyboardButton('10А', callback_data='10а')
btn_11a = InlineKeyboardButton('11А', callback_data='11а')
btn_11b = InlineKeyboardButton('11Б', callback_data='11б')

inline_kb_klass.row(btn_5a, btn_5b, btn_5c, btn_5d)
inline_kb_klass.row(btn_6a, btn_6b, btn_6c, btn_6d)
inline_kb_klass.row(btn_7a, btn_7b, btn_7c, btn_7d)
inline_kb_klass.row(btn_8a, btn_8b, btn_8c)
inline_kb_klass.row(btn_9a, btn_9b, btn_9c)
inline_kb_klass.row(btn_10a)
inline_kb_klass.row(btn_11a, btn_11b)


