from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from src.GUI.AssetsPath import assets_path
from src.GUI.CompFactory import CompFactory
from src.GUI.ModifiedComponents import ImageButton


class Header(RelativeLayout):
    def __init__(self, within, theme, **kwargs):
        super().__init__(**kwargs)
        # parent class
        self.within = within

        # Attributes
        self.theme = theme
        self.myFactory = CompFactory(self.theme)

        # Components
        self.background = Rectangle()
        self.logo = Label(text="Current", font_name=assets_path["font_logo"], font_size=30,
                          color=self.myFactory.get_text_color(), pos_hint={"x": -.3, "center_y": .5})

        self.mode_button = ImageButton(source=self.myFactory.get_mode_source(), size_hint=(.35, .9),
                                       pos_hint={"right": 1, "center_y": .5}, keep_ratio=True, allow_stretch=False)

        self.mode_button.bind(on_press=self.change_mode)

        # builder methods
        self.add_components()

    def add_components(self):
        self.add_background()
        self.add_widget(self.logo)
        self.add_widget(self.mode_button)

    def add_background(self):
        with self.canvas.before:
            self.myFactory.get_panel_color()
            self.background = Rectangle(pos=self.pos, size=self.size)

    # for changing modes
    def change_mode(self, *args):
        if self.theme == "light":
            self.theme = "dark"

        elif self.theme == "dark":
            self.theme = "light"

        self.myFactory = CompFactory(self.theme)
        self.logo.color = self.myFactory.get_text_color()
        self.mode_button.source = self.myFactory.get_mode_source()

        self.change_background()
        self.change_panels()

    def change_background(self):
        self.canvas.before.remove(self.background)
        with self.canvas.before:
            self.myFactory.get_panel_color()
            self.background = Rectangle(pos=(0, 0), size=self.size)
            self.canvas.before.add(self.background)

    def change_panels(self):
        self.within.change_mode(self.theme)

    # size adjustment methods
    def on_size(self, *args):
        self.background.pos = 0, 0
        self.background.size = self.size