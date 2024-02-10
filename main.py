import json
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from pyrogram import filters
from pyrogram import filters, types
from pyrogram.errors.exceptions import ChannelInvalid
import datetime
import asyncpg
import pyrogram
from pyrogram import enums
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pyrogram import Client, filters
from pyrogram.types import Message
import psycopg2  

api_id = os.environ.get('api_id')
api_hash = os.environ.get('api_hash')
bot_token = os.environ.get('bot_token')


def delete_user(conn_hacaton, cursor_hacaton, user_id):
    try:
        query_delete = "DELETE FROM user_data_hacaton1 WHERE id = %s"
        cursor_hacaton.execute(query_delete, (user_id,))
        conn_hacaton.commit()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error deleting user: {e}\n")
        conn_hacaton.rollback()
        return False

def change_status_money(conn_hacaton, cursor_hacaton, user_id, status_money):
    try:
        query_update = "UPDATE user_data_hacaton1 SET status_money = %s WHERE id = %s"
        cursor_hacaton.execute(query_update, (status_money, user_id))
        conn_hacaton.commit()
        return True
    except Exception as e:
        print(f"Error changing status_money: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error changing status_money: {e}\n")
        conn_hacaton.rollback()
        return False

def change_status_delete(conn_hacaton, cursor_hacaton, user_id, status_delete):
    try:
        query_update = "UPDATE user_data_hacaton1 SET status_delete = %s WHERE id = %s"
        cursor_hacaton.execute(query_update, (status_delete, user_id))
        conn_hacaton.commit()
        return True
    except Exception as e:
        print(f"Error changing status_delete: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error changing status_delete: {e}\n")
        conn_hacaton.rollback()
        return False
def delete_user(conn_hacaton, cursor_hacaton, user_id):
    try:
        query_delete = "DELETE FROM user_data_hacaton1 WHERE id = %s"
        cursor_hacaton.execute(query_delete, (user_id,))
        conn_hacaton.commit()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error deleting user: {e}\n")
        conn_hacaton.rollback()
        return False


def change_status_add(conn_hacaton, cursor_hacaton, user_id, status_add):
    try:
        query_update = "UPDATE  user_data_hacaton1 SET status_add = %s WHERE id = %s"
        cursor_hacaton.execute(query_update, (status_add, user_id))
        conn_hacaton.commit()
        return True
    except Exception as e:
        print(f"Error changing status_add: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error changing status_add: {e}\n")
        conn_hacaton.rollback()
        return False

def get_info(conn_hacaton, cursor_hacaton, user_id, choise):
    try:
        query_select = f"SELECT {choise} FROM  user_data_hacaton1 WHERE id = %s"
        cursor_hacaton.execute(query_select, (user_id,))
        result = cursor_hacaton.fetchone()

        if result is not None:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error getting info: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error getting info: {e}\n")
        return None

 
def add_new_user(conn_hacaton, cursor_hacaton, user_id, money):
    try:
        query_insert = "INSERT INTO  user_data_hacaton1 (id, money, status_money, status_delete, status_add) VALUES (%s, %s, %s, %s, %s)"
        cursor_hacaton.execute(query_insert, (user_id, money, False, False, False))
        conn_hacaton.commit()
        return True
    except Exception as e:
        print(f"Error adding new user: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error adding new user: {e}\n")
        conn_hacaton.rollback()
        return False

def check_user_data(conn_hacaton, cursor_hacaton, user_id):
    try:
        query_name = "SELECT * FROM  user_data_hacaton1 WHERE id = %s"
        cursor_hacaton.execute(query_name, (user_id,))
        result_name = cursor_hacaton.fetchone()
        if result_name == None:  
         return False
        else:
         return True
    except Exception as e:
        print(f"Error checking user data: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error checking user data: {e}\n")
        return False
def delete_money(conn_hacaton, cursor_hacaton, user_id, amount):
    try:
        current_money = get_info(conn_hacaton, cursor_hacaton, user_id, "money")

        if current_money is not None and current_money >= amount and amount>=0:
            new_money = current_money - amount

            query_update = "UPDATE  user_data_hacaton1 SET money = %s WHERE id = %s"
            cursor_hacaton.execute(query_update, (new_money, user_id))
            conn_hacaton.commit()

            return True
        else:
            print("Insufficient funds.")
            return False
    except Exception as e:
        print(f"Error deleting money: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error deleting money: {e}\n")
        return False
def add_money(conn_hacaton, cursor_hacaton, user_id, amount):
    try:
        current_money = get_info(conn_hacaton, cursor_hacaton, user_id, "money")

        if current_money is not None and amount>=0:
            new_money = current_money + amount

            query_update = "UPDATE  user_data_hacaton1 SET money = %s WHERE id = %s"
            cursor_hacaton.execute(query_update, (new_money, user_id))
            conn_hacaton.commit()

            return True
        else:
            print("User not found.")
            return False  
    except Exception as e:
        print(f"Error adding money: {e}")
        with open("logs.txt", "a") as logs_file:
            logs_file.write(f"Error adding money: {e}\n")
        return False

app = Client(
    "leader_economic_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

conn_hacaton = psycopg2.connect(database="fyd", user="postgres", password="your_password", host="localhost", port="5432")
cursor_hacaton = conn_hacaton.cursor() 

# Функція, яка буде викликатися при старті бота
@app.on_message(filters.command("start"))
def start_command(client, message):
      user_id = message.from_user.id
      
      if check_user_data(conn_hacaton, cursor_hacaton, user_id):
        keyboard = [
           [
              InlineKeyboardButton("Закинути грошей", callback_data="deposit"),
              InlineKeyboardButton("Зняти грошей", callback_data="withdraw"),
      
           ],
           ]
  
        reply_markup = InlineKeyboardMarkup(keyboard)
  
      # Створити повідомлення з кількістю грошей та кнопками
        amount = get_info(conn_hacaton, cursor_hacaton, user_id, "money")
        message_text = f"Вітаю! Ваш рахунок:{amount} грн\nВиберіть опцію:"
        message.reply_text(message_text, reply_markup=reply_markup)
      else:
           add_new_user(conn_hacaton, cursor_hacaton, user_id, 0)
           
           message_text = f"Вітаю! Для початку введіть початкову суму, яка зараз у вас на рахунку в гривнях:"
           change_status_money(conn_hacaton, cursor_hacaton, user_id, True)
       
           message.reply_text(message_text)
          
  
  
  # Запускаємо бота
  # Запускаємо бота
@app.on_callback_query()
async def button_click(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "deposit":
        # Логіка для кнопки "Закинути грошей"
        message_text = "Будь ласка, введіть суму, яку ви хочете закинути:"
        await client.send_message(chat_id=user_id, text=message_text)
        change_status_add(conn_hacaton, cursor_hacaton, user_id, True)

    elif data == "withdraw":
        # Логіка для кнопки "Зняти грошей"
        message_text = "Будь ласка, введіть суму, яку ви хочете зняти:"
        await client.send_message(chat_id=user_id, text=message_text)
        change_status_delete(conn_hacaton, cursor_hacaton, user_id, True)
@app.on_message(filters.command("delete", prefixes="/") & filters.private)
async def delete_command(client, message: Message):
    try:
        # Перевірити, чи користувач, який викликав команду, має право видаляти інших користувачів
        
            # Отримати айді користувача для видалення з аргументів команди
            command_parts = message.text.split(" ", 1)
            if len(command_parts) == 2:
                user_id_to_delete = command_parts[1]

                # Викликати функцію видалення користувача
                if delete_user(conn_hacaton, cursor_hacaton, user_id_to_delete):
                    await message.reply(f"Користувача з ID {user_id_to_delete} успішно видалено.")
                else:
                    await message.reply(f"Помилка видалення користувача.")
            else:
                await message.reply("Неправильне використання команди /delete. Введіть ID користувача для видалення.")
       
    except Exception as e:
        await message.reply(f"Помилка: {e}")
@app.on_message(filters.private)
async def process_private_message(client, message):
    user_id = message.from_user.id

    if get_info(conn_hacaton, cursor_hacaton, user_id, "status_money"):
        

        try:
            current_balance = get_info(conn_hacaton, cursor_hacaton, user_id, "money")
            amount_text = message.text

            if amount_text is not None and amount_text.strip() != "":
                amount = float(amount_text)

                if amount >= 0:
                    add_money(conn_hacaton, cursor_hacaton, user_id, amount)
                    message_text = "Чудово! Гроші Тепер напишіть /start, щоб вибрати опцію"
                    await client.send_message(chat_id=user_id, text=message_text)
                    change_status_money(conn_hacaton, cursor_hacaton, user_id, False)
                elif amount < 0:
                    await client.send_message(chat_id=user_id, text="Сума має бути не менше 0.")
                else:
                    await client.send_message(chat_id=user_id, text="Недостатньо коштів на рахунку.")
            else:
                await client.send_message(chat_id=user_id, text="Будь ласка, введіть коректне число.")
        except ValueError:
            await client.send_message(chat_id=user_id, text="Будь ласка, введіть коректне число.")
    
    elif get_info(conn_hacaton, cursor_hacaton, user_id, "status_add"):
     try:
        current_balance = get_info(conn_hacaton, cursor_hacaton, user_id, "money")
        amount_text = message.text

        if amount_text is not None and amount_text.strip() != "":
            amount = float(amount_text)

            if amount >= 0:
                add_money(conn_hacaton, cursor_hacaton, user_id, amount)
                message_text = "Чудово! Гроші успішно додано! Тепер напишіть /start, щоб вибрати опцію"
                await client.send_message(chat_id=user_id, text=message_text)
                change_status_add(conn_hacaton, cursor_hacaton, user_id, False)
            else:
                await client.send_message(chat_id=user_id, text="Сума має бути не менше 0.")
        else:
            await client.send_message(chat_id=user_id, text="Будь ласка, введіть коректне число.")
     except ValueError:
        await client.send_message(chat_id=user_id, text="Будь ласка, введіть коректне число.")

    elif get_info(conn_hacaton, cursor_hacaton, user_id, "status_delete"):
       
     try:
        current_balance = get_info(conn_hacaton, cursor_hacaton, user_id, "money")
        amount_text = message.text

        if amount_text is not None and amount_text.strip() != "":
            amount = float(amount_text)

            if amount >= 0 and current_balance >= amount:
                delete_money(conn_hacaton, cursor_hacaton, user_id, amount)
                message_text = "Чудово! Гроші успішно знято! Тепер напишіть /start, щоб вибрати опцію"
                await client.send_message(chat_id=user_id, text=message_text)
                change_status_delete(conn_hacaton, cursor_hacaton, user_id, False)
            elif amount < 0:
                await client.send_message(chat_id=user_id, text="Сума має бути не менше 0.")
            else:
                await client.send_message(chat_id=user_id, text="Недостатньо коштів на рахунку.")
        else:
            await client.send_message(chat_id=user_id, text="Будь ласка, введіть коректне число.")
     except ValueError:
        await client.send_message(chat_id=user_id, text="Будь ласка, введіть коректне число.")

        

app.run()