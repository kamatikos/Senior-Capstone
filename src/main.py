from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from pyglet.app import exit
from src.settings import Settings



class Main_Menu(Menu):
    def __init__(self):
        super(Main_Menu, self).__init__('Main Menu')

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        menu_items = [

            (MenuItem('Item A', self.item_A_callback)),
            (MenuItem('Settings', self.settings)),
            (MenuItem('Exit', self.on_quit)),
        ]

        self.create_menu(menu_items)

    def item_A_callback(self):
        print('Item A Callback invoked!')

    def settings(self):
        director.push(Scene(Settings()))

    def on_quit(self):
        exit()


director.init()

director.run(Scene(Main_Menu()))
