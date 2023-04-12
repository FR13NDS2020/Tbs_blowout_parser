# Team-Blacksheep Scraper
### Overview
The script in this project scrapes the website https://www.team-blacksheep.com for products listed under the 'Blowout' category, and sends updates to a Telegram chat when new products are added, or when the price of an existing product changes.

### Requirements
* Python 3.6 or higher
* 'httpx' module
* 'selectolax' module
* 'requests' module
* A Telegram Bot API token
* A Telegram chat ID to which the updates will be sent
### Installation
1. Clone the repository to your local machine
2. Install the required modules using the following command:

'''pip install -r requirements.txt
'''
3. Edit the apiToken and chatID variables at the beginning of the tbs_scraper.py file with your Telegram Bot API token and chat ID.
4. Run the script using the following command:

'''python tbs_scraper.py'''
### Usage
The script will scrape the Team-Blacksheep website for products listed under the 'Blowout' category, and send updates to the specified Telegram chat when new products are added, or when the price of an existing product changes. The updates will include the name of the product, its price, a link to the product page, and an image of the product.

The script will create a file named products.json in the same directory as the script, which will store the details of the products that have been scraped. If the script is run multiple times, it will check this file to see if any new products have been added, or if the price of an existing product has changed.

If new products have been added, or if the price of an existing product has changed, the script will send a Telegram message to the specified chat with the details of the new or updated product. If no new products have been added, the script will exit without sending any messages.

### Contributing
If you'd like to contribute to this project, feel free to open an issue or a pull request.

### License
This project is licensed under the MIT License.