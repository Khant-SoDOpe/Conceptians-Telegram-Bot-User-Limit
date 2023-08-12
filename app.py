import json
import requests
import redis
from telebot import types, TeleBot
from keep_alive import keep_alive
import os

keep_alive()

bot = TeleBot(os.environ["TELEGRAM_API"])

# Connect to Redis
redis_client = redis.Redis(host=os.environ['REDIS_HOST'],
                           port=os.environ['REDIS_PORT'],
                           password=os.environ['REDIS_PASSWORD'])


def get_premium_users():
  premium_users_data = redis_client.get("premium_users")
  if premium_users_data:
    return json.loads(premium_users_data)
  else:
    return []


premium_users = get_premium_users()

chat_id = {}
log_key = 0


def add(id, category):
  # Load the existing data from Redis
  users_data = redis_client.get("users_data")
  if users_data:
    users_data = json.loads(users_data)
  else:
    users_data = []

  # Check if the user already exists in the data
  existing_user = next((player for player in users_data if player["id"] == id),
                       None)

  if existing_user is not None:
    # Replace the existing user's category
    existing_user["category"] = category
  else:
    # Create a dictionary for the new player with chance_count set to 0
    new_user = {"id": id, "category": category, "chance_count": 0}
    # Append the new user data to the existing data
    users_data.append(new_user)

  # Save the updated user data to Redis
  redis_client.setex("users_data", 86400, json.dumps(users_data))


@bot.message_handler(commands=['start'])
def send_welcome(message):
  # Create a one-time keyboard
  keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  library = types.KeyboardButton('Library')
  social = types.KeyboardButton('Social Media Links')
  keyboard.add(library, social)

  # Send the message with the one-time keyboard
  global log_key
  log_key = 3
  bot.send_message(message.chat.id,
                   'Welcome From Conceptians!',
                   reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Library')
def Library(message):
  url = f"https://admin.conceptians.org/api/bot/category"
  headers = {"Authorization": os.environ["ROUTE_API"]}
  response = requests.get(url, headers=headers)
  data = response.json()
  #Create a keyboard with buttons for each category
  keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
  for category in data:
    button = types.KeyboardButton(category['category'])
    keyboard.add(button)
  global log_key
  log_key = 1
  bot.send_message(message.chat.id,
                   'Choose Categories that you want to read',
                   reply_markup=keyboard)


@bot.message_handler(func=lambda message: True if log_key == 1 else False)
def books(message):
  add(message.chat.id, message.text)
  keyboard = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
  button = types.KeyboardButton("Library")
  keyboard.add(button)
  url = f"https://admin.conceptians.org/api/bot/category/{message.text}"
  headers = {"Authorization": os.environ["ROUTE_API"]}
  response = requests.get(url, headers=headers)
  json_data = response.json()
  for data in json_data:
    button = types.KeyboardButton(data['title'])
    keyboard.add(button)
  global log_key
  log_key = 2
  bot.send_message(message.chat.id,
                   'Choose Books that you want to download',
                   reply_markup=keyboard)


@bot.message_handler(func=lambda message: True if log_key == 2 else False)
def download_books(message):
  # Load the existing data from Redis
  users_data = redis_client.get("users_data")
  if users_data:
    users_data = json.loads(users_data)
  else:
    users_data = []

  for user in users_data:
    if user["id"] == message.chat.id:
      if message.chat.id in premium_users:
        # Process without checking chance_count for specific user ID
        url = f"https://admin.conceptians.org/api/bot/category/{user['category']}"
        headers = {"Authorization": os.environ["ROUTE_API"]}
        response = requests.get(url, headers=headers)
        json_data = response.json()
        for book in json_data:
          if book['title'] == message.text:
            title = f"<b>{book['title']}</b>"
            cat = f"<i>Category: {book['category']}</i>"
            filesize = f"<i>File size: {book['filesize']}mb</i>"
            download = book['link']
            button = types.InlineKeyboardButton(text='Download', url=download)
            # Create a keyboard with the button
            keyboard = types.InlineKeyboardMarkup([[button]])
            try:
              photo_url = book['image']
              bot.send_photo(chat_id=message.chat.id, photo=photo_url)
            except:
              print('no photo')
            bot.send_message(message.chat.id,
                             f"{title}\n{cat}\n{filesize}",
                             parse_mode='HTML',
                             reply_markup=keyboard)

            return  # Exit the function after finding the book

      else:
        # Check chance_count for other user IDs
        if user["chance_count"] > 5:
          bot.send_message(
            message.chat.id,
            "You have reached the maximum number of allowed downloads.")
          return

        url = f"https://admin.conceptians.org/api/bot/category/{user['category']}"
        headers = {"Authorization": os.environ["ROUTE_API"]}
        response = requests.get(url, headers=headers)
        json_data = response.json()
        for book in json_data:
          if book['title'] == message.text:
            title = f"<b>{book['title']}</b>"
            cat = f"<i>Category: {book['category']}</i>"
            filesize = f"<i>File size: {book['filesize']}mb</i>"
            download = book['link']
            button = types.InlineKeyboardButton(text='Download', url=download)
            # Create a keyboard with the button
            keyboard = types.InlineKeyboardMarkup([[button]])
            try:
              photo_url = book['image']
              bot.send_photo(chat_id=message.chat.id, photo=photo_url)
            except:
              print('no photo')
            bot.send_message(message.chat.id,
                             f"{title}\n{cat}\n{filesize}",
                             parse_mode='HTML',
                             reply_markup=keyboard)

            # Update the chance count for the user
            user["chance_count"] += 1

            # Save the updated user data back to Redis
            redis_client.set("users_data", json.dumps(users_data))

            return  # Exit the function after finding the book

  # If no book is found for the user ID, you can handle it here
  bot.send_message(message.chat.id, "No book found for the user ID.")


@bot.message_handler(func=lambda message: message.text == 'Social Media Links')
def Social_Media_Links(message):
  keyboard = types.InlineKeyboardMarkup()
  button1 = types.InlineKeyboardButton(
    text='Facebook',
    url='https://www.facebook.com/profile.php?id=100082812927163')
  button2 = types.InlineKeyboardButton(
    text='Youtube', url='https://www.youtube.com/@conceptians8961/featured')
  button3 = types.InlineKeyboardButton(
    text='Instagram', url='https://www.instagram.com/conceptians_org')
  button4 = types.InlineKeyboardButton(
    text='Linkedin', url='https://www.linkedin.com/company/conceptians/')
  button5 = types.InlineKeyboardButton(
    text='Tiktok', url='https://www.tiktok.com/@conceptians')
  keyboard.add(button1, button2)
  keyboard.add(button3, button4)
  keyboard.add(button5)

  # Send a message with the inline keyboard
  bot.send_message(message.chat.id,
                   "Click the button to open the link:",
                   reply_markup=keyboard)


bot.polling()
