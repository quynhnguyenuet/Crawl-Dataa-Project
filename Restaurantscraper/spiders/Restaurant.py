import scrapy
import urllib.parse
from Restaurantscraper.items import RestaurantItem
from scrapy.http import Request
class RestaurantSpider(scrapy.Spider):
    name = "Restaurant"
    allowed_domains = ["www.yelp.com"]
    start_urls = ["https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA&start=0"]
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
    def parse(self, response):
        # Using CSS to select the href attribute directly
        links = response.css('a.yelp-emotion-idvn5q::attr(href)').getall()
        for link in links:
            # Ensure the link is not the homepage
            if "/biz/" in link:  # Assuming that valid business links contain '/biz/'
                full_url = response.urljoin(link)  # Ensure the link is a full URL
                # Follow each link that was extracted and call the parse_details callback
                yield response.follow(full_url, callback=self.parse_details)
                
        # next_page_url = response.css('a.pagination-link-component__09f24__iAi8c::attr(href)').get()

        # current_page_number = response.css('div.pagination-link-current__09f24__nwDm3::text').get()
        # if current_page_number:
        #     current_page_number = int(current_page_number)

    
        # if next_page_url and current_page_number < 25:
        #     next_page_url = response.urljoin(next_page_url)
        #     yield scrapy.Request(next_page_url, callback=self.parse)
                # Handle pagination
        current_offset = response.url.split("start=")[-1]
        if current_offset:
            current_offset = int(current_offset)
            next_offset = current_offset + 10
            if next_offset <= 230:  # Ensure scraping stops after page 24 (10 results per page, 24 pages)
                next_page_url = f"https://www.yelp.com/search?find_desc=Restaurants&find_loc=San+Francisco%2C+CA&start={next_offset}"
                yield response.follow(next_page_url, callback=self.parse)


    def parse_details(self, response):
        name = response.css('h1::text').get()  
        add_len = len(response.xpath("//address/p"))
        if add_len == 3:
            address_1 = response.xpath("//a/span[@class=' raw__09f24__T4Ezm']/text()").get()
            address_2 = response.xpath("(//address/p/span/text())[1]").get()
            address_3 = response.xpath("(//address/p/span/text())[2]").get()
        elif add_len == 2:
            address_1 = response.xpath("//a/span[@class=' raw__09f24__T4Ezm']/text()").get()
            address_2 = ''
            address_3 = response.xpath("(//address/p/span/text())[1]").get()
        else:
            address_1 = ''
            address_2 = ''
            address_3 = response.xpath("//a/span[@class=' raw__09f24__T4Ezm']/text()").get()
            
        try:
            street_address = address_1 + " " + address_2
        except:
            street_address = ''
        try:
            city = address_3.split(", ")[0]
        except:
            city = ''
        try:
            zip_code = address_3.split(", ")[1].split()[1]
        except:
            zip_code = ''
        try:
            state = address_3.split(", ")[1].split()[0]
        except:
            state = ''
          
        phone_number = response.xpath("/html/body/yelp-react-root/div[1]/div[6]/div/div[1]/div[2]/aside/section[1]/div/div[2]/div/div[2]/p[2]/text()").get()
        # number_of_reviews = response.css('a.css-19v1rkv::text').get().strip('() reviews')
        # Try to get the review count
        reviews_text = response.xpath("//a[contains(text(), 'reviews')]/text()").get()
        # review_text = response.css('a.css-19v1rkv::text').get()
       
        # # Check if the review_text is not None
        if reviews_text:
            number_of_reviews = reviews_text.strip('() reviews')
        else:
            number_of_reviews = '0'
        number_of_reviews = int(number_of_reviews.replace(',', ''))
        #rating = float(response.css('span.css-1fdy0l5::text').get())
        # Try to get the rating text
        rating_text =  response.css('span.yelp-emotion-1sphrcy::text').get()
        # Check if the rating_text is not None and is a valid number
        if rating_text:
            try:
                rating = float(rating_text)
            except ValueError:
                rating = None  # Handle cases where the conversion could fail
        else:
            rating = None
        price_range = response.css('span.price__09f24__F1T0p::text').getall()
        for price_text in price_range:
            if price_text:
                price = float(price_text.replace('$', '').strip())
        link = response.xpath('//*[@id="main-content"]/section[1]/div[2]/div[2]/p/a/@href').get()
        # url_param = link.split("url=")[1].split("&")[0]
        # menu_url = urllib.parse.unquote(url_param)
        url_param = None
        menu_url = None

# Check if the link is not None and contains the required URL parameter
        if link and "url=" in link:
            try:
                # Attempt to extract the URL parameter
                url_param = link.split("url=")[1].split("&")[0]
                # Decode the URL-encoded string
                menu_url = urllib.parse.unquote(url_param)
            except IndexError:
                # Handle cases where split does not work as expected
                print("Error parsing the URL parameter from link.")
        Restaurant = RestaurantItem()
        Restaurant['Name'] = name
        Restaurant['Street_Address'] = street_address
        Restaurant['Zip_Code'] = zip_code
        Restaurant['City'] = city
        Restaurant['State'] = state
        Restaurant['Price_Range'] = price_range
        Restaurant['Phone'] = phone_number
        Restaurant['Rating'] = rating
        Restaurant['Number_of_Reviews'] = number_of_reviews
        Restaurant['Menu_Link'] = menu_url
        yield Restaurant