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

---

**IMPORTANT WARNING**

This method can and will temporarily block you from buff if used too often.
I've been able to get every code using this method, and I only got banned on my second run however this does not mean the same will apply to you.

After being blocked you need to contact support and will be unblocked after a couple of days. 
Getting blocked a second time using this method will mean a __permanent block__. 

Use the second method if you want to be safe.

**USE AT YOUR OWN RISK**

---

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


---
Thanks to [daradan](https://github.com/daradan/buff_163_scraper) for the first method 