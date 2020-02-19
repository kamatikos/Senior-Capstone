from cocos.menu import Menu, CENTER, MenuItem
from pyglet.app import exit



class Settings(Menu):
    def __init__(self):
        super(Settings, self).__init__('Settings')

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        menu_items = [

            (MenuItem('Audio', self.audio_settings_callback)),
            (MenuItem('Graphics', self.graphics_settings_callback)),
            (MenuItem('Exit', self.on_quit)),

        ]

        self.create_menu(menu_items)

    def audio_settings_callback(self):
        print('Audio Settings Callback invoked!')

    def graphics_settings_callback(self):
        print('Graphics Settings Callback invoked!')

    def on_quit(self):
        exit()