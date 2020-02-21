from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director


class Settings(Menu):
    def __init__(self):
        super(Settings, self).__init__('Settings')

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        menu_items = [

            (MenuItem('Audio', self.audio_settings_callback)),
            (MenuItem('Graphics', self.graphics_settings_callback)),
            (MenuItem('Back', self.previous_scene)),

        ]

        self.create_menu(menu_items)

    def audio_settings_callback(self):
        print('Audio Settings Callback invoked!')

    def graphics_settings_callback(self):
        print('Graphics Settings Callback invoked!')

    def previous_scene(self):
        director.pop()  # return to previous scene
