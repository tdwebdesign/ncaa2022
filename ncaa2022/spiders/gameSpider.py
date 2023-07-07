import scrapy


class GamespiderSpider(scrapy.Spider):
    name = "gameSpider"
    allowed_domains = ["www.espn.com"]
    start_urls = ["https://www.espn.com/college-football/scoreboard/_/week/1/year/2022/seasontype/2/group/80"]

    def parse(self, response):
        # Extract game IDs from the scoreboard page
        game_ids = response.css('section::attr(id)').getall()

        # For each game ID, create a request to the recap and boxscore pages
        for game_id in game_ids:
            recap_url = f'https://www.espn.com/college-football/recap/_/gameId/{game_id}'
            boxscore_url = f'https://www.espn.com/college-football/boxscore/_/gameId/{game_id}'
            
            yield scrapy.Request(recap_url, self.parse_recap)
            yield scrapy.Request(boxscore_url, self.parse_boxscore)

    def parse_recap(self, response):
        # Extract game ID from the URL
        game_id = response.url.split('/')[-1]

        # Extract game recap title
        game_recap_title = response.css('.Story__Headline::text').get()

        # Extract game recap body
        game_recap_body = response.css('.Story__Body p::text').getall()
        game_recap_body = [recap.strip() for recap in game_recap]

        # Extract game recap date
        game_recap_date = response.css('.Byline__Meta--publishDate::text').get()

        # Create a dictionary for the game
        game = {
            'game_id': game_id,
            'game_recap_date': game_recap_date,
            'game_recap_title': game_recap_title,
            'game_recap_body': game_recap_body,
        }

        # Yield the game
        yield game