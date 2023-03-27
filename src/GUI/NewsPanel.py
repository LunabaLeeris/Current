import math
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout

from AssetsPath import *
from src.GUI.CompFactory import CompFactory


class NewsPanel(GridLayout):
    cols = 1

    def __init__(self, theme, headline_text, image_path, article_link, author, publish_date, excerpt, logo, **kwargs):
        super().__init__(**kwargs)
        # class attributes
        self.myFactory = CompFactory(theme)
        self.theme = theme
        self.headline_text = headline_text
        self.image_path = image_path
        self.article_link = article_link
        self.author_name = author
        self.publish_date = publish_date
        self.excerpt_text = excerpt
        self.logo = logo

        # component attributes
        self.image = None
        self.headline = None
        self.excerpt = None
        self.footer = None
        self.background = Rectangle()

        # dimensions
        self.size_hint = (1, None)
        self.height_ratio = 0
        self.text_size_ratio = .9  # width limit of text_size
        self.headline_size_ratio = 0  # font size ratio of headline based on the height of the panel
        self.excerpt_size_ratio = 0  # font size ratio of excerpt based on the width of the panel

        # builder methods
        self.add_components()
        self.add_background()

    def add_background(self):
        with self.canvas.before:
            self.myFactory.get_panel_color()
            self.background = Rectangle(pos=self.pos, size=self.size)

    def add_components(self):
        self.add_image()
        self.add_headline()
        self.add_excerpt()
        self.add_footer()

    # ------------------ adding components --------------------

    def add_headline(self):
        self.headline_size_ratio = .3 / math.log(len(self.headline_text)**.8) # arbitrary number

        if self.headline_text != "none":
            self.headline = self.myFactory.create_headline(self.headline_text,
                                                           self.article_link, self.width * self.text_size_ratio,
                                                           self.height * self.headline_size_ratio)
            self.height_ratio += .25
            self.add_widget(self.headline)

    def add_image(self):
        if self.image_path != "none":
            self.image = AsyncImage(source=self.image_path, allow_stretch=True, keep_ratio=True, size_hint=(1, 2))
            self.height_ratio += .7

            self.add_widget(self.image)

    def add_excerpt(self):
        self.excerpt_size_ratio = .08 / (math.log(len(self.excerpt_text))**.5)  # arbitrary number

        if self.excerpt_text != "none":
            self.excerpt = self.myFactory.create_excerpt(self.excerpt_text,
                                                         self.article_link, self.width * self.text_size_ratio,
                                                         self.height * self.excerpt_size_ratio)
            self.height_ratio += .3
            self.excerpt.size_hint_y = .8
            self.add_widget(self.excerpt)

    def add_footer(self):
        self.height_ratio += .03
        self.footer = Footer(self.theme, self.logo, self.author_name, self.publish_date, size_hint=(.5, .2), pos_hint={"center_x": .5})
        self.add_widget(self.footer)

    # ----------- adjusting screen methods -----------------

    def adjust_screen(self):
        self.re_draw_background()
        self.adjust_components()

    def re_draw_background(self, *args):
        self.height = self.width * self.height_ratio  # changes the height of the panel
        self.background.size = self.size
        self.background.pos = self.pos

    def adjust_components(self):
        if self.headline is not None:  # adjusts the headline
            self.headline.text_size = (self.width * self.text_size_ratio, None)  # adjusts the line wrapping
            self.headline.font_size = self.width * self.headline_size_ratio

        if self.excerpt is not None:  # adjusts the excerpt
            self.excerpt.text_size = (self.width * self.text_size_ratio, None)  # adjusts the line wrapping
            self.excerpt.font_size = self.width * self.excerpt_size_ratio

    # ----------- changing modes -----------------

    def change_mode(self, theme):
        self.theme = theme
        self.myFactory = CompFactory(theme)

        self.change_background()

        if self.headline is not None:
            self.remove_widget(self.headline)
            self.headline = self.myFactory.create_headline(self.headline_text,
                                                           self.article_link, self.headline.text_size[0],
                                                           self.headline.font_size)
            self.footer.details.color = self.myFactory.get_headline_text_color()
            self.remove_widget(self.footer)

            if self.excerpt is not None:
                self.excerpt.color = self.myFactory.get_excerpt_text_color()
                self.remove_widget(self.excerpt)

            self.add_widget(self.headline)

            if self.excerpt is not None:
                self.add_widget(self.excerpt)

            self.add_widget(self.footer)

    def change_background(self):
        self.canvas.before.remove(self.background)
        with self.canvas.before:
            self.myFactory.get_panel_color()
            self.background = Rectangle(pos=self.pos, size=self.size)
            self.canvas.before.add(self.background)


class Footer(BoxLayout):
    orientation = 'horizontal'
    padding = (0, 0, 0, 5)

    def __init__(self, theme, logo, author_name, publish_date, **kwargs):
        super().__init__(**kwargs)
        self.logo = logo
        self.font_size_ratio = .4
        self.details = CompFactory(theme).create_author_date(author_name, publish_date, self.height*self.font_size_ratio)
        self.add_components()

    def add_components(self):
        self.add_widget(AsyncImage(source=self.logo, allow_stretch=True, keep_ratio=True, size_hint=(.4, 1)))
        self.details.size_hint = (.6, 1)
        self.add_widget(self.details)

    def on_size(self, *args):
        self.details.font_size = self.height*self.font_size_ratio
