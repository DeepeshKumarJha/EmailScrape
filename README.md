# EmailScraper

EmailScraper is a Program which is created to scrape emails from different website,
EmailScraper support both dynamic and static pages.




## How to use:

you can use `requirment.txt` to install all the dependences,

To execute the program :
  
    python run.py -s <list_of_sites>


## Library Used:
- scrapy
- re
- selenium

## Limitations:

- Current version don't work with the social media sites.
- It don't work with the sites which has contact form.
- If the header and footer is generated through javascript, than it might don't work properly.