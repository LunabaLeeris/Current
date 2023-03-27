from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivymd.uix.behaviors import HoverBehavior


class ResponsiveLabel(Label, HoverBehavior):
    def __init__(self, transition_color, **kwargs):
        super().__init__(**kwargs)
        self.transition_color = transition_color
        self.default_color = self.color

        self.on_enter_animation = Animation(color=self.transition_color, d=0.3)
        self.on_leave_animation = Animation(color=self.default_color, d=0.3)

    def on_enter(self):
        self.on_enter_animation.start(self)

    def on_leave(self):
        self.on_leave_animation.start(self)

class AnimatedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anim = Animation(opacity=.5, d=1) + Animation(opacity=1, d=1)
        self.anim.repeat = True
        self.anim.start(self)


class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
