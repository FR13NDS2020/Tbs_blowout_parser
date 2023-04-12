import re
import httpx
import json
from selectolax.parser import HTMLParser
import requests

apiToken = 'BOT.API.TOKEN'
chatID = 'YOUR CHATID'


def send_to_telegram(message, img_url):
    print("sending message")
    apiURL = f'https://api.telegram.org/bot{apiToken}/'

    # First, download the image from the URL
    response = requests.get(img_url)
    img_file = response.content

    # Then, send the message along with the image
    files = {'photo': ('image.jpg', img_file)}
    data = {'chat_id': chatID, 'caption': message}
    r = requests.post(apiURL + 'sendPhoto', files=files, data=data)

    print(r.text)


def scrape_tbs():
    print("start scraping")
    base_url = "https://www.team-blacksheep.com"
    endpoint = "/shop/q:blowout"
    url = base_url + endpoint

    try:
        with httpx.Client() as client:
            response = client.get(url, timeout=30)
            # rest of the scraping code
    except httpx.ConnectTimeout as exc:
        print(f"Failed to connect to {url}: {exc}")

    parser = HTMLParser(response.text)
    listings = parser.css_first('div#product_listing')
    items = listings.css('li')

    products = []
    for item in items:
        product = {}
        product['name'] = item.css_first('b').text()
        product['img'] = base_url + item.css_first('img.product').attributes['src']
        product['price'] = item.css_first('em').text()
        product['link'] = base_url + item.css_first('a').attributes['href']
        products.append(product)
    # print(products[:-2])
    print("end scraping")
    return products


def if_new(products):
    # Load existing products from the JSON file
    try:
        with open('products.json', 'r') as infile:
            existing_products = json.load(infile)
    except FileNotFoundError:
        # If the file does not exist yet, there are no existing products
        existing_products = []

    # Get the URLs of the existing products
    existing_urls = {product['link'] for product in existing_products}
    existing_products_dict = {product['link']: product for product in existing_products}

    new_products = []
    for product in products:
        if not product['price']:
            continue  # Skip products with invalid price

        # Check if the product is already in the existing products
        if product['link'] in existing_urls:
            existing_product = existing_products_dict[product['link']]
            if existing_product['price'] != product['price']:
                # Send a custom message for price change
                refactored_price = re.sub(r"(in|out of) stock", "", product['price'].lower()).strip()
                previus_price = re.sub(r"(in|out of) stock", "", existing_product['price'].lower()).strip()

                float_price = re.sub(r"[^\d.]", "", product['price']).strip()
                float_previus_price = re.sub(r"[^\d.]", "", existing_product['price']).strip()

                if float(float_price) > float(float_previus_price):
                    price_emoji = "📈"  # Use a chart increasing emoji
                elif float(float_price) < float(float_previus_price):
                    price_emoji = "📉"  # Use a chart decreasing emoji
                else:
                    price_emoji = "🔽"

                text = f"{product['name']}\nPrice {price_emoji} {previus_price} to {refactored_price}. \n{product['link']}"
                send_to_telegram(text, img_url=product['img'])

                # Update price in the existing product
                existing_product['price'] = product['price']
        else:
            # Add new product to existing_products list and new_products list
            existing_products.append(product)
            existing_urls.add(product['link'])
            new_products.append(product)

    # Remove duplicate products from existing_products list
    existing_products = list(existing_products_dict.values())

    # Write the updated existing_products list to the file
    with open('products.json', 'w') as f:
        json.dump(existing_products, f, indent=1)

    # Exit the program with an error message if the products list is empty
    if not new_products:
        exit("No new products to process")

    # Check for products in the existing products that are no longer on the website
    for product in existing_products:
        if product['link'] not in [p['link'] for p in products]:
            # Remove the product from the list
            print(f"Remove old products{product}")
            existing_products.remove(product)
    # Add the new products to the existing products
    existing_products.extend(new_products)

    # Save the updated products to the JSON file
    with open('products.json', 'w') as outfile:
        json.dump(existing_products, outfile, indent=1)

    # Send a Telegram message for each new product
    for product in new_products:
        if "in stock" in product['price'].lower():
            stock = " ✅"
        elif "out of stock" in product['price'].lower():
            stock = " ❌"
        else:
            stock = ""
        refactored_text = re.sub(r"(in|out of) stock", "", product['price'].lower()).strip()
        text = f"🆕 {product['name']}\n\n{refactored_text}{stock}\n{product['link']}"
        send_to_telegram(text, img_url=product['img'])


if __name__ == '__main__':
    products = scrape_tbs()
    if_new(products)
