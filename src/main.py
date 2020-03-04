from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from pyglet.app import exit
from src.settings import Settings_Scene
from src.game import Game



class Main_Menu(Menu):
    def __init__(self):
        super(Main_Menu, self).__init__('Main Menu')

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        menu_items = [

            (MenuItem('Play', self.play)),
            (MenuItem('Settings', self.settings)),
            (MenuItem('Exit', self.on_quit))
        ]

        self.create_menu(menu_items)

    def play(self):
        director.push(Scene(Game()))

    def settings(self):
        director.push(Scene(Settings_Scene()))

    def on_quit(self):
        exit()


class Main_Scene(Scene):
    def __init__(self):
        super(Main_Scene, self).__init__()

        self.add(Main_Menu())




director.init(width=800, height=600, autoscale=False, resizable=False)

director.run(Main_Scene())
