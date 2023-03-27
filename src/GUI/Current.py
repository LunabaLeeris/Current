from kivy import Config
Config.set('graphics', 'width', 500)
Config.set('graphics', 'height', 800)

from src.GUI.Header import Header
from kivy.properties import Clock
from src.GUI.NewsSection import NewsSection
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout


class PrimaryScreen(RelativeLayout):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.news_section = NewsSection(self.theme, pos_hint={"center_x": .5, "top": .9}, size_hint=(1, .9))
        self.header = Header(self, self.theme, size_hint=(1, .09), pos_hint={"center_x": .5, "top": 1})
        self.add_components()

        # Threads
        Clock.schedule_interval(self.adjust_screen, 1/5)  # adjusts the screen

    def add_components(self):
        self.add_widget(self.news_section)
        self.add_widget(self.header)

    def adjust_screen(self, dt):
        if self.news_section is not None:
            self.news_section.adjust_screen()

    # responsible for changing the mode
    def change_mode(self, theme):
        self.theme = theme
        self.news_section.change_mode(theme)


class Current(App):
    def build(self):
        return PrimaryScreen("light")


if __name__ == "__main__":
    Current().run()
