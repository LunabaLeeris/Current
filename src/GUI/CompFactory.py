# factory that will return components based on different contraints
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from src.GUI.AssetsPath import *
import webbrowser
from src.GUI.ModifiedComponents import ResponsiveLabel


class CompFactory:
    def __init__(self, theme):  # mode can only be the following ("light", "dark")
        self.theme = theme
        self.driver = None

    # ------------------- creation properties -------------------

    def create_button(self, text, pos_hint, size_hint):
        pass

    def create_headline(self, text, link, text_size, font_size):  # returns a label for the headline
        if self.theme == "light":
            label = ResponsiveLabel(text=f'[b][ref=clicked]{text}[/ref][/b]', halign='center', valign="bottom",
                                    color=self.get_headline_text_color(), transition_color=self.get_transition_color(),
                                    text_size=(text_size, None), font_size=font_size, font_name=assets_path["font_bold"], markup=True)

        elif self.theme == "dark":  # e4e6eb
            label = ResponsiveLabel(text=f'[b][ref=clicked]{text}[/ref][/b]', halign='center', valign="bottom",
                                    color=self.get_headline_text_color(), transition_color=self.get_transition_color(),
                                    text_size=(text_size, None), font_size=font_size, font_name=assets_path["font_bold"], markup=True)
        else:
            return  # no such thing as that kind of theme

        label.bind(on_ref_press=lambda value, instance: self.click_link(value, instance, link))
        return label

    def create_excerpt(self, text, link, text_size, font_size):  # returns a label for the excerpt
        if self.theme == "light":
            label = Label(text=f'[ref=clicked]{text}[/ref]', halign='center', text_size=(text_size, None),
                          valign="top", color=self.get_excerpt_text_color(), font_size=font_size,
                          font_name=assets_path["font_normal"], opacity=.9, markup=True)

        elif self.theme == "dark":
            label = Label(text=f'[ref=clicked]{text}[/ref]', halign='center', text_size=(text_size, None),
                          valign="top", color=self.get_excerpt_text_color(), font_size=font_size,
                          font_name=assets_path["font_normal"], opacity=.9, markup=True)

        else:
            return  # no such thing as that kind of theme

        label.bind(on_ref_press=lambda value, instance: self.click_link(value, instance, link))
        return label

    def create_author_date(self, author, date, size):  # returns a label for the excerpt
        if self.theme == "light":
            return Label(text=author+": "+date, font_name=assets_path['font_normal'],
                         font_size=size, color=self.get_headline_text_color())
        elif self.theme == "dark":
            return Label(text=author+": "+date, font_name=assets_path['font_normal'], font_size=size,
                         color=self.get_headline_text_color())
        else:
            return  # no such thing as that kind of theme

    def create_slider(self, *args):
        pass

    # ------------------- getting properties -------------------

    def get_panel_color(self):
        if self.theme == "light":
            return Color(255 / 255, 255 / 255, 255 / 255, 1)  # hex = "#65676B"
        elif self.theme == "dark":
            return Color(36/255, 37/255, 38/255, 1)  # hex = #242526
        else:
            return

    def get_background_color(self):
        if self.theme == "light":
            return Color(101 / 255, 103 / 255, 107 / 255, 1)  # hex = "#65676B"
        elif self.theme == "dark":
            return Color(24/255, 25/255, 26/255, 1)  # hex = #18191A
        else:
            return

    def get_text_color(self):
        if self.theme == "light":
            return 0, 0, 0, 1
        elif self.theme == "dark":
            return 228/255, 230/255, 235/255
        else:
            pass

    def get_mode_source(self):
        return os.path.join('Assets', 'Button', self.theme+".png")

    def get_headline_text_color(self):
        if self.theme == "light":
            return 0, 0, 0, 1

        elif self.theme == "dark":
            return 228/255, 230/255, 235/255

    def get_excerpt_text_color(self):
        if self.theme == "light":
            return "#000000"

        elif self.theme == "dark":
            return "#e4e6eb"

    def get_transition_color(self):
        if self.theme == "light":
            return 39/255, 130/255, 32/255, 1

        elif self.theme == "dark":
            return 145 / 255, 203 / 255, 141 / 255, 1

    # helper methods
    def click_link(self, value, instance, link):  # responsible for opening a link when clicked
        webbrowser.open(link)


