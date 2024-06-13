from aiogram import Dispatcher, Bot, executor, types
from config import API_KEY
import database

bot = Bot(token= API_KEY)
dp = Dispatcher(bot)

database.init_db()

async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command='/start', description='Команда для того, чтобы запустить бота'),
        types.BotCommand(command='/add', description='Команда для того, чтобы добавить запись'),
        types.BotCommand(command='/list', description='Команда для того, чтобы узнать, свои записи'),
        types.BotCommand(command='/delete', description='Команда для того, чтобы удалить свои записи'),
    ]

    await bot.set_my_commands(commands)


@dp.message_handler(commands= 'start')
async def start(message: types.Message):
    await message.reply('Привет я бот в котором ты можешь оставить заметки')


@dp.message_handler(commands= 'add')
async def add(message: types.Message):
    task = message.get_args()
    if task:
        user_id = message.from_user.id
        username = message.from_user.username
        database.add_task(user_id, username, task)
        await message.reply(f"Задача {task} добавлена")
    else:
        await message.reply('Пожалуйста, укажите задачу через команду /add')

@dp.message_handler(commands= 'list')
async def list(message: types.Message):
    tasks = database.get_task()
    if tasks:
        tasks_list = "\n".join([f"{task[0]}.{task[3]} (Добавлена пользователем) @{task[2]}" for task in tasks])
        await message.reply(f"Ваши задачи: \n{tasks_list}")
    else:
        await message.reply('У вас нет задач')

# async def update_task_ids():
#     tasks = database.get_task()
#     for i, task in enumerate(tasks):
#         database.update_task_id(task[0], i + 1)
#
#
# @dp.message_handler(commands= 'delete')
# async def delete(message: types.Message):
#     task_id = message.get_args()
#     if task_id.isdigit():
#         database.delete_task(int(task_id))
#         await message.reply(f"Задача {task_id} удалена")
#         await update_task_ids()
#     else:
#         await message.reply('Укажите корректный id задачи')
#

# Функция для обновления айди задач после удаления
@dp.callback_query_handler(text='delete_all')
async def delete_all_tasks(callback: types.CallbackQuery):
    database.delete_all_tasks()
    await callback.message.reply('Все задачи удалены!')  # Обновляем айди задачи в базе данных


@dp.message_handler(commands=['delete'])
async def delete(message: types.Message):
    task_id = message.get_args()
    if task_id.isdigit():
        database.delete_tasks(int(task_id))
        tasks = database.get_task()
        for i, task in enumerate(tasks):
            database.update_task_id(task[0], i + 1)
        await message.reply(f"Задача {task_id} удалена")
    else:
        await message.reply('Укажите корректный id задачи ')
    print(task_id)

async def on_startup(Dispatcher):
    await set_commands(dp.bot)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)