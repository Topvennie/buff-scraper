############################
#  Database Configuration  #
############################

# Refer to the README to see the required columns in your database table

DATABASE_USER = 'XXX'
DATABASE_PASSWORD = 'XXX'
DATABASE_HOST = 'XXX'
DATABASE = 'XXX'
DATABASE_NAME = 'XXX'

# Select which method to use
# True  | Goes over each page of the sales and/or buying tab (depends on your following configuration)
# False | Tries each code between a start and end value

USE_URL_METHOD = True

###########################
#  USE_URL_METHOD = True  #
#  Configuration          #
###########################

URL_PURCHASE = 'https://buff.163.com/api/market/goods/buying'
URL_SALE = 'https://buff.163.com/api/market/goods'
# Which pages to go over
# Only add the ones you want to include
URLS = [URL_SALE, URL_PURCHASE]

# Replace device-id, session and csrf_token with your own values
# You can get them by
#   Logging into buff
#   Right click -> inspect element
#   Go to the 9th tab 'Application'
#   Select on the left side 'Cookies'
#   Enter the values

COOKIES = {
    'Device-Id': 'XXX',
    'Locale-Supported': 'en',
    'game': 'csgo',
    'AQ_HD': '1',
    'YD_SC_SID': 'XXX',
    'NETS_utid': 'XXX',
    'NTES_YD_SESS': 'XXX',
    'S_INFO': 'XXX',
    'P_INFO': 'XXX',
    'remember_me': 'XXX',
    'session': 'XXX',
    'csrf_token': 'XXX',
}

# Which page to start at
START_PAGE = 0

############################
#  USE_URL_METHOD = False  #
#  Configuration           #
############################

# The code to start with
START_CODE = 0
# The maximum code value ( but not including [START_CODE, END_CODE[ )
END_CODE = 1000000

# Whether to use threads
# Using 10 threads speeds up the process by about 2 to 4 times
# If you're unsure of what this means leave them to their default values
ENABLE_THREADS = True
# The amount of threads to use
AMOUNT_OF_THREADS = 10

####################################
#  No need to change these values  #
####################################

URL_API = 'https://buff.163.com/api/market/goods/sell_order'

HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://buff.163.com/market/csgo',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/107.0.0.0 Safari/537.36 '
                  'OPR/93.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Opera";v="93", "Not/A)Brand";v="8", "Chromium";v="107"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

PARAMS = {
    'game': 'csgo',
    'page_num': '1',
}

REPLACE_DICT = {
    '★': '%E2%98%85',
    ' ': '%20',
    '|': '%7C',
    '™': '%E2%84%A2',
    '(': '%28',
    ')': '%29'
}

