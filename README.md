# **Conceptions Telegram Bot**

The Conceptions Telegram Bot is a bot designed to provide users with access to a library of books and social media links. Users can choose categories of books they want to read and then select specific books for downloading. Additionally, the bot provides links to Conceptions' social media profiles.


## **Features**



1. **Start Command**: The `/start` command initiates a conversation with the bot and displays a one-time keyboard with options to navigate to the library or social media links.
2. **Library Command**: The `Library` command displays a list of available book categories using data retrieved from the Conceptions API. Users can select a category to view the books within that category.
3. **Book Selection**: After selecting a category, users can choose a specific book to download. The bot retrieves book information from the API and displays the book's title, category, file size, and an option to download the book.
4. **Download Limit**: The bot tracks the number of books a user has downloaded and limits the number of downloads to five. If a user reaches the download limit, they receive a notification indicating that they have reached the maximum allowed downloads.
5. **Social Media Links**: The `Social Media Links` command provides users with quick access to Conceptions' social media profiles, including Facebook, YouTube, Instagram, LinkedIn, and TikTok.


## **Setup**

To run the Conceptions Telegram Bot, you need to perform the following steps:



1. Set up a Redis server and obtain the host, port, and password.
2. Create an account on the[ Telegram Bot Platform](https://core.telegram.org/bots) and obtain an API token.
3. Obtain an API token for the Conceptions API by contacting the administrators of the Conceptions platform.
4. Set up a server to host the bot code. You can use platforms like[ Heroku](https://www.heroku.com/) or[ Google Cloud Platform](https://cloud.google.com/) for deployment.
5. Set the environment variables required for the bot:
    * `TELEGRAM_API`: Telegram API token obtained from the Bot Platform.
    * `ROUTE_API`: Conceptions API token.
    * `REDIS_HOST`: Redis server host.
    * `REDIS_PORT`: Redis server port.
    * `REDIS_PASSWORD`: Redis server password.
6. Install the necessary Python packages by running `pip install -r requirements.txt`.
7. Start the bot by running `python &lt;filename.py>`.


## **Usage**

Once the bot is up and running, users can interact with it through Telegram. Here's a step-by-step guide on how to use the bot:



1. Start a conversation with the bot by searching for its username or by clicking on a provided link.
2. Upon starting, the bot will greet the user and display a one-time keyboard with options to navigate to the library or social media links.
3. To access the library, select the `Library` option from the keyboard. The bot will retrieve a list of available book categories.
4. Choose a category of interest by selecting it from the displayed options. The bot will retrieve books belonging to the selected category.
5. Select a specific book from the list to view details about the book, such as the title, category, file size, and an option to download the book.
6. If the user attempts to download more than five books within the same category, they will receive a notification indicating that they have reached the maximum allowed downloads.
7. To access Conceptions' social media links, select the `Social Media Links` option from the one-time keyboard. The bot will display buttons for various social media platforms.
8. Click on any of the provided buttons to open the respective social media link.

## **About**

The Conceptions Telegram Bot was developed by Sai Khant Zay Lynn Yaung as a project to provide users with easy access to a library of books and Conceptions' social media profiles. It is not an official product of Conceptions but utilizes the Conceptions API for book data.

For more information, contact Sai Khant Zay Lynn Yaung at khant_zay@icloud.com .

Thank you for using the Conceptions Telegram Bot! We hope you enjoy your reading experience and find the social media links helpful.
