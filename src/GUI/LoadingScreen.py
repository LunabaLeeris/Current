import os
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.uix.relativelayout import RelativeLayout
from src.GUI.AssetsPath import assets_path
from src.GUI.CompFactory import CompFactory
from src.GUI.ModifiedComponents import AnimatedLabel


class LoadingScreen(RelativeLayout):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)
        self.theme = theme
        self.myFactory = CompFactory(theme)
        self.background = Rectangle()

        # for loading thread
        self.scheduled = False
        self.loading_animation_thread = None

        # for robot head animation
        self.frame = 0
        self.robot_image = Image(source=os.path.join("Assets", "LoadingScreen", self.theme, f"{self.frame}.png"),
                                 size_hint=(.5, .4),
                                 keep_ratio=True, pos_hint={"center_x": .5, "center_y": .5})
        # for scraping text
        self.text = None
        self.text_ratio = .15

        self.add_components()

    def add_components(self):
        self.add_background()
        self.add_widget(self.robot_image)
        self.start_loading()

    def add_background(self):
        with self.canvas.before:
            CompFactory(self.theme).get_panel_color()
            self.background = Rectangle(size=self.size, pos=self.pos)

    def loading(self, dt):  # main loading animation function
        if self.frame == 6:
            self.frame = 0

        self.robot_image.source = os.path.join("Assets", "LoadingScreen", self.theme, f"{self.frame}.png")
        self.frame += 1

    def start_loading(self):  # starts the loading animation
        if not self.scheduled:
            self.loading_animation_thread = Clock.schedule_interval(self.loading, 1 / 10)
            self.text = (AnimatedLabel(text="SCRAPING THE WEB",
                                       pos_hint={"center_x": .5, "center_y": .65},
                                       font_name=assets_path["font_bold"],
                                       font_size=self.width * self.text_ratio,
                                       color=self.myFactory.get_headline_text_color()))

            self.add_widget(self.text)
            self.scheduled = True
        else:
            return  # throws an error if the loading screen was already scheduled and is scheduled again

    def stop_loading(self):  # stops the loading animation
        if self.scheduled:
            self.loading_animation_thread.cancel()
            self.scheduled = False
        else:
            return  # throws an error if loading screen is tried to stop schedule without scheduling it first

    # changing methods

    def change_mode(self, theme):
        self.theme = theme
        self.myFactory = CompFactory(theme)
        self.change_background()
        self.text.color = self.myFactory.get_headline_text_color()

    def change_background(self):
        self.canvas.before.remove(self.background)
        with self.canvas.before:
            CompFactory(self.theme).get_panel_color()
            self.background = Rectangle(size=self.size, pos=self.pos)
            self.canvas.before.add(self.background)

    def on_size(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

        if self.text is not None:
            self.text.font_size = self.width * self.text_ratio
