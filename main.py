from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

Window.set_icon("icon.ico")

LabelBase.register(name="NotoSans", fn_regular="NotoSans-Bold.ttf")

common_patterns = ["1234", "qwerty", "11111", "123", "abc123", "0000", "password",
    "7777", "999", "qwertyuiop", "444", "333", "8888", "6666",
    "789", "4567", "3456"]
months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
nos = ["one","two","three","four","five","six","seven","eight","nine","ten"]
KV = '''
<PasswordScreen>:
    orientation: "vertical"
    padding: dp(20)
    spacing: dp(20)
    size_hint_y: None
    height: self.minimum_height

    MDLabel:
        id: game_title
        text: "\\nLino's Password Game"
        halign: "center"
        font_style: "H4"
        theme_text_color: "Custom"
        text_color: 0, 1, 0, 1
        font_name: "NotoSans"
        size_hint_y: None
        height: self.texture_size[1]

    CustomTextInput:
        id: password_field
        hint_text: "Start typing your password"
        size_hint_x: 0.9
        pos_hint: {"center_x": 0.5}
        size_hint_y: None
        height: dp(50)
        multiline: False

    MDLabel:
        id: char_count
        text: "Characters: 0"
        halign: "left"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        font_name: "NotoSans"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        id: label_message
        text: ""
        markup: True
        halign: "left"
        theme_text_color: "Custom"
        font_name: "NotoSans"
        size_hint_y: None
        height: self.texture_size[1]


<WinScreen>:
    FloatLayout:
        MDLabel:
            id: win_title
            text: "YOU WON!"
            halign: "center"
            font_style: "H3"
            theme_text_color: "Custom"
            text_color: 0, 1, 0, 1
            font_name: "NotoSans"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            opacity: 0

        MDLabel:
            id: win_sub
            text: "Thanks for Playing Lino's Password Game"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 1, 1, 1
            font_name: "NotoSans"
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            opacity: 0
'''

class CustomTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.foreground_color = (1, 1, 1, 1)
        self.cursor_color = (0.8, 1, 0, 1)
        self.background_color = (0, 0, 0, 0)
        self.hint_text_color = (0.7, 0.7, 0.7, 1)
        self.font_name = "NotoSans"
        self.write_tab = False


class PasswordScreen(BoxLayout):
    pass


class WinScreen(Screen):
    pass


class PasswordApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Lime"
        self.theme_cls.theme_style = "Dark"
        Builder.load_string(KV)

        self.sm = ScreenManager()
        self.scroll = MDScrollView()
        self.screen = PasswordScreen()
        self.scroll.add_widget(self.screen)

        game_screen = Screen(name="game")
        game_screen.add_widget(self.scroll)
        self.win_screen = WinScreen(name="win")

        self.sm.add_widget(game_screen)
        self.sm.add_widget(self.win_screen)

        return self.sm

    def on_start(self):
        self.typing_event = None
        self.error_sound = SoundLoader.load("error.mp3")
        self.complete_sound = SoundLoader.load("complete.mp3")
        self.screen.ids.password_field.bind(text=self.schedule_validation)
        self.last_rules_text = ""

    def schedule_validation(self, instance, value):
        self.screen.ids.char_count.text = f"Characters: {len(value)}"
        if self.typing_event:
            self.typing_event.cancel()
        self.typing_event = Clock.schedule_once(lambda dt: self.check_password(value), 0.4)

    def check_password(self, paswd):
        label = self.screen.ids.label_message
        if not paswd:
            label.text = ""
            self.last_rules_text = ""
            return

        def has_total_25(p):
            return sum(int(c) for c in p if c.isdigit()) == 25

        rules = []

        rules.append(("Password must contain a lowercase letter",
                  lambda p: any(c.islower() for c in p)))

        if rules[-1][1](paswd):
            rules.append(("Password must contain an uppercase letter",
                      lambda p: any(c.isupper() for c in p)))

        if len(rules) == 2 and rules[-1][1](paswd):
            rules.append(("Password must contain at least 7 characters",
                      lambda p: len(p) >= 7))

        if len(rules) == 3 and rules[-1][1](paswd):
            rules.append(("Password must contain a number",
                      lambda p: any(c.isdigit() for c in p)))

        if len(rules) == 4 and rules[-1][1](paswd):
            rules.append(("Password must contain the name of a month",
                      lambda p: any(m in p.lower() for m in months)))

        if len(rules) == 5 and rules[-1][1](paswd):
            rules.append(("Password must contain a number name between 1-10",
                      lambda p: any(n in p.lower() for n in nos)))

        if len(rules) == 6 and rules[-1][1](paswd):
            rules.append(("Password must contain '#'",
                      lambda p: "#" in p))

        if len(rules) == 7 and rules[-1][1](paswd):
            rules.append(("Password must contain '@'",
                         lambda p: "@" in p))

        if len(rules) == 8 and rules[-1][1](paswd):
            rules.append(("Password must contain '&'",
                          lambda p: "&" in p))

        if len(rules) == 9 and rules[-1][1](paswd):
            rules.append(("The digits in the password must add up to 25",
                          lambda p: has_total_25(p)))

        if len(rules) == 10 and rules[-1][1](paswd):
            rules.append(("Password must contain '!'",
                          lambda p: "!" in p))

        if len(rules) == 11 and rules[-1][1](paswd):
            rules.append(("Password must contain '*'",
                          lambda p: "*" in p))

        if len(rules) == 12 and rules[-1][1](paswd):
            rules.append(("Password must contain '%'",
                          lambda p: "%" in p))

        if len(rules) == 13 and rules[-1][1](paswd):
            rules.append(("Password must contain '?'",
                          lambda p: "?" in p))

        if len(rules) == 14 and rules[-1][1](paswd):
            rules.append(("Password must not contain a common pattern",
                          lambda p: not any(x in p.lower() for x in common_patterns)))
    
        if len(rules) == 15 and rules[-1][1](paswd):
            rules.append(("Password must not contain spaces",
                          lambda p: " " not in p))

        if len(rules) == 16 and rules[-1][1](paswd):
            rules.append(("Password must contain a Roman numeral (I, V, X, L, C, D or M)",
                          lambda p: any(c in "IVXLCDM" for c in p.upper())))

        if len(rules) == 17 and rules[-1][1](paswd):
            rules.append(("Password must contain a color name",
                          lambda p: any(color in p.lower() for color in [
                              "red", "blue", "green", "yellow", "orange",
                              "purple", "pink", "black", "white", "brown",
                              "gray", "grey"
                          ])))

        if len(rules) == 18 and rules[-1][1](paswd):
            rules.append(("Password must contain both an even and an odd digit",
                          lambda p: any(c in "02468" for c in p) and
                                    any(c in "13579" for c in p)))

        if len(rules) == 19 and rules[-1][1](paswd):
            rules.append(("Password length must be a multiple of 3",
                          lambda p: len(p) % 3 == 0))
        red_rules = []
        green_rules = []
        all_green = True

        for i, (msg, check) in enumerate(rules, start=1):
            if check(paswd):
                green_rules.append(f"[color=00FF00]Rule {i}: {msg}[/color]")
            else:
                red_rules.append(f"[color=FF0000]Rule {i}: {msg}[/color]")
                all_green = False

        new_text = "\n\n".join(red_rules + green_rules)

        if new_text != self.last_rules_text:
            if not all_green:
                if self.error_sound:
                    self.error_sound.play()
            else:
                if self.complete_sound:
                    self.complete_sound.play()
                if len(rules) == 20:
                    Clock.schedule_once(self.show_win_screen, 1)

        label.opacity = 0
        label.y = -50
        label.text = new_text

        Animation(
            opacity=1,
            y=0,
            duration=0.4,
            t="out_back"
        ).start(label)

        self.last_rules_text = new_text

    def show_win_screen(self, dt=None):
        self.sm.current = "win"
        win_title = self.win_screen.ids.win_title
        win_sub = self.win_screen.ids.win_sub
        Animation(opacity=1, duration=1).start(win_title)
        Animation(opacity=1, duration=1.2).start(win_sub)


if __name__ == "__main__":
    PasswordApp().run()
