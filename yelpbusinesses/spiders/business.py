import scrapy
from scrapy.http import Response

find_desc = input("Please, enter category name (for example: 'General Contractors'): ")
find_loc = input("Please, enter location (for example: 'New York'): ")


class BusinessSpider(scrapy.Spider):
    name = "business"
    start_urls = [f"https://www.yelp.com/search?find_desc={find_desc}&find_loc={find_loc}"]

    def parse(self, response: Response, **kwargs):
        for business in response.css(".css-1agk4wl a::attr(href)"):
            yield response.follow(business, callback=self.parse_business)

            # next_page = (
            #     response.css(".pagination-links__09f24__bmFj8"
            #                  " > div")[-1]
            #     .css("a::attr(href)")
            #     .get()
            # )
            # if next_page is not None:
            #     yield scrapy.Request(next_page, callback=self.parse)

    def parse_business(self, response: Response):
        yield {
            "Business name": response.css("h1.css-1se8maq::text").get(),
            "Business rating":
                float(response.css(".five-stars__09f24__mBKym::attr(aria-label)")
                      .get().split(" ")[0]),
            "Number of reviews":
                int(response.css(".css-1m051bw::text")
                    .get().split(" ")[0]),
            "Business yelp url": response.request.url,
            "Business website": response.css("div.css-1vhakgw"
                                             " > div.arrange__09f24__LDfbs"
                                             " > div.arrange-unit__09f24__rqHTg"
                                             " > .css-1p9ibgf"
                                             " > a.css-1um3nx::attr(href)")
            .get().split("&cachebuster")[0].split("%3A%2F%2F")[-1],
            "List of reviews": self.get_reviews(response)
        }

    def get_reviews(self, response: Response):
        reviewer_name = response.css("span.fs-block"
                                     " > a.css-1m051bw::text").getall()[:5]
        reviewer_location = response.css(
            ".responsive-hidden-small__09f24__qQFtj"
            " > div.border-color--default__09f24__NPAKY"
            " > span.css-qgunke::text").getall()[1:6]
        review_date = response.css(
            ".margin-t1__09f24__w96jn"
            " > .arrange__09f24__LDfbs"
            " > div.arrange-unit__09f24__rqHTg"
            " > span.css-chan6m::text").getall()[:5]
        current_reviewer = {}
        reviewers_list = []
        for reviewer in range(5):
            current_reviewer["Reviewer name"] = reviewer_name[reviewer]
            current_reviewer["Reviewer location"] = reviewer_location[reviewer]
            current_reviewer["Review date"] = review_date[reviewer]
            reviewers_list.append(current_reviewer)
            current_reviewer = {}

        return reviewers_list
