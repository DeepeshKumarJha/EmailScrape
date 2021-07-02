import scrapy
import re
from scrapy.http import headers
from scrapy.selector import Selector
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options



"""
links which contain emails have either of these keywords in them
    - contact-us
    - contact
    - contactus
    - about
    - about-us
    - aboutus
"""

class MailSpider(scrapy.Spider):
    
    # link is the list variable send from run.py file which contains links list.
    
    name = 'mail'

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1'
    }

    email_check = '([a-z0-9][-a-z0-9_\+\.]*[a-z0-9])@([a-z0-9][-a-z0-9\.]*[a-z0-9]\.(arpa|root|aero|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)|([0-9]{1,3}\.{3}[0-9]{1,3}))'

    custom_settings = {
        'USER_AGENT': user_agent,
        'DUPEFILTER_DEBUG': True,
    }

    options = Options()
    options.add_argument('--headless')
    driver = Chrome(options=options)

    def start_requests(self):
        for url in self.link:
            yield scrapy.Request(
                url = url,
                headers=self.headers,
                callback=self.parse
                )


    def parse(self, response):
        
        #flag will determine which loop i will use to call those contact links by defalt True means scrapy.Request
        flag = True

        values = []

        if response.status == 200:

            values = self.get_links_extracted(Selector(text=response.body))

            if not values:
                flag = False
                self.driver.get(response.url)
                selector_object = Selector(text = self.driver.page_source)
                values = self.get_links_extracted(selector_object)

        else:
            flag = False
            self.driver.get(response.url)
            selector_object = Selector(text = self.driver.page_source)

            values = self.get_links_extracted(selector_object)

        if flag:
            for v in values:
                yield scrapy.Request(
                    url = response.urljoin(v),
                    callback = self.extract_emails_using_scrapy,
                    headers=self.headers
                )
        else:
            self.extract_emails_using_selenium(values, response)
        

    def get_links_extracted(self, temp_selector):

        temp_val = []
        lists = temp_selector.xpath('//a/@href').extract()
        contact_search = re.compile('.*contact.*')
        about_search = re.compile('.*about.*')
        temp_val += list(filter(contact_search.match, lists))
        temp_val += list(filter(about_search.match, lists))

        return temp_val

    def extract_emails_using_selenium(self,list_of_email_links, response):
        
        for li in list_of_email_links:

            self.driver.get(response.urljoin(li))
            
            emails_list = self.help_email_extracter(Selector(text = self.driver.page_source))

            self.logger.info(f'########################## here we go : \n\n{emails_list}\n\n')
            
    def extract_emails_using_scrapy(self,response):

            emails_list=self.help_email_extracter(Selector(text=response.body))

            self.logger.info(f'########################## here we go : \n\n{emails_list}\n\n')

    def help_email_extracter(self, last_selector):
        
        page_text = last_selector.xpath('//text()').extract()
        email_expression = re.compile(self.email_check)
        last_list = list(filter(email_expression.match, page_text))

        return last_list