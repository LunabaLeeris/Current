import asyncio
from threading import Thread
from kivy.graphics import Rectangle
from kivy.properties import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from src.GUI.CompFactory import CompFactory
from src.GUI.LoadingScreen import LoadingScreen
from src.GUI.NewsPanel import NewsPanel
from src import VoxScraper as vS
from src import TimeScraper as tS
from src import BBCScraper as bbcS
from src import NewyorkTimesScraper as nytS
from src import CNNScraper as cnnS
from src import ABCScraper as abcS
from src import ManilaTimesScraper as mtS


class NewsSection(ScrollView):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.myFactory = CompFactory(theme)
        self.loading_screen = LoadingScreen(theme)

        self.news_section_contents = NewsSectionContents(self.theme, self, size_hint=(1, None),
                            padding=("20dp", "10dp", "20dp", "0dp"),
                            spacing=("10dp", "10dp"))

        self.news_section_contents.height = self.news_section_contents.minimum_height

        # components
        self.background = Rectangle()
        
        # builder methods
        self.draw_background()
        self.add_components()

    def add_components(self):
        self.add_widget(self.loading_screen)
        self.loading_screen.start_loading()
        
    def add_news_section(self):
        if self.loading_screen.scheduled:
            self.remove_widget(self.loading_screen)
            self.loading_screen.stop_loading()
            self.add_widget(self.news_section_contents)

    def draw_background(self):
        with self.canvas.before:
            self.myFactory.get_background_color()
            self.background = Rectangle(size=self.size, pos=self.pos)

    def add_new_article(self, theme, headline_text, image_path, article_link, author, publish_date, excerpt, logo):
        self.news_section_contents.add_new_article(theme, headline_text, image_path, article_link, author, publish_date, excerpt, logo)

    def re_draw_background(self):
        self.background.size = self.size
        self.background.pos = self.pos

    def adjust_screen(self):
        self.news_section_contents.height = self.news_section_contents.minimum_height
        self.news_section_contents.adjust_screen()

        self.re_draw_background()

    # ----------- Asynchronous Scraping Methods -----------
    def change_mode(self, theme):
        self.theme = theme
        self.myFactory = CompFactory(theme)
        self.change_background()
        self.loading_screen.change_mode(theme)
        self.news_section_contents.change_mode(theme)

    def change_background(self):
        self.canvas.before.remove(self.background)
        self.draw_background()
        self.canvas.before.add(self.background)


class NewsSectionContents(StackLayout):
    def __init__(self, theme, within, **kwargs):
        super().__init__(**kwargs)
        self.within = within # parent class. Follows the observer pattern principle
        self.theme = theme
        self.article_panels = []  # will hold all the articles
        
        # components
        self.scrapers = [cnnS, nytS, abcS, mtS, bbcS, vS, tS]
        self.articles = []
        self.background = Rectangle()
        self.done_scraping = False
        # for threading attributes
        self.thread_parser = Thread(target=self.start_scraping).start()

        self.checker = Clock.schedule_interval(self.check, 1)

    # ----------- Asynchronous Scraping Methods -----------

    def check(self, dt):
        if self.done_scraping:
            self.add_components()
            self.within.add_news_section()
            self.checker.cancel()

    def start_scraping(self, *args):
        asyncio.run(self.scrape_contents())

    async def scrape_contents(self):
        # will cause a little loading
        task = []

        for i in self.scrapers:
            task.append(asyncio.create_task(self.scrape_content(i)))

        await asyncio.gather(*task)

        self.done_scraping = True

    async def scrape_content(self, scraper):
        content = await scraper.scrape()
        self.articles += content

    def add_components(self):
        for article in self.articles:
            if len(article) == 0:
                continue

            self.add_new_article(self.theme, article[0], article[1],
                                 article[2], article[3], article[4],
                                 article[5], article[6])

    # ----------- adjust screen methods -----------

    def adjust_screen(self):
        for article in self.article_panels:
            article.adjust_screen()

    def add_new_article(self, theme, headline_text, image_path, article_link, author, publish_date, excerpt, logo):
        article = NewsPanel(theme, headline_text, image_path, article_link, author, publish_date, excerpt, logo)
        self.article_panels.append(article)
        self.add_widget(article)

    #  ----------- For changing the modes -----------

    def change_mode(self, theme):
        self.theme = theme

        for panel in self.article_panels:
            panel.change_mode(theme)



