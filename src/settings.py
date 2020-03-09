from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene


class Settings_Menu(Menu):
    def __init__(self):
        super(Settings_Menu, self).__init__('Settings')

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        menu_items = [

            (MenuItem('Audio', self.audio_settings_callback)),
            (MenuItem('Graphics', self.graphics_settings_callback)),
            (MenuItem('Back', self.previous_scene))

        ]

        self.create_menu(menu_items)

    def audio_settings_callback(self):
        print('Audio Settings Callback invoked!')

    def graphics_settings_callback(self):
        print('Graphics Settings Callback invoked!')

    def previous_scene(self):
        director.pop()  # return to previous scene


class Settings_Scene(Scene):
    def __init__(self):
        super(Settings_Scene, self).__init__()

        self.add(Settings_Menu())