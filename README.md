# Buff Scraper

Gets all item codes from buff and saves it to a database.
It saves:
- The item code
- The name
- It's type
- The url to a picture of that item
- The link to it's steam community market page

## Configuration

There are 2 supported methods of getting the codes.
1. Going over each page on [the selling page](https://buff.163.com/api/market/goods) and [the buying page](https://buff.163.com/api/market/goods/buying) and getting the information of each item listed on there.
2. Trying each code in a specified interval and see what gives result.

The method can be selected inside *config.py*

### *USE_URL_METHOD* = True

This will select the **first** method.

**Be careful! This method can and will temporarily ban you on buff if used more than once**

**Use at your own risk**

However, this method is extremely faster than the second one.

### *USE_URL_METHOD* = False

This will select the **second** method.

It supports threading to speed up the process. I recommend using 10 threads.

## Database

All the data will be saved inside a database.
Officially, only mysql databases are supported. 
A small adjustment inside *database.py* is needed to work with sqlite.

You should already prepare a table with the following columns:
- code (int) primary key
- name (varchar(100))
- type (varchar(100))
- icon_url (varchar(256))
- steam_market_url (varchar(256))