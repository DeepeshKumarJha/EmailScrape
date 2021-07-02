

BOT_NAME = 'escrape'

SPIDER_MODULES = ['escrape.spiders']
NEWSPIDER_MODULE = 'escrape.spiders'

ROBOTSTXT_OBEY = False

# ------- Settings for selenium ----------------- #
# Don't Want This because i am using selenium directly
# from shutil import which

# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('/Users/deepeshjha/Desktop/Code/WebScraping/chromedriver')
# SELENIUM_DRIVER_ARGUMENTS=['--headless']

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_selenium.SeleniumMiddleware': 800
# }

# ----------------------------------------------- #