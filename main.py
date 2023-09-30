from aiogram.utils import executor
from create_bot import dp
import handlers
import database


    


async def on_startup(_):
    print("Бот вышел на связь")
    database.sql_start()

#admin.register_handlers_admin(dp)
handlers.register_handlers(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)