import pyglet

from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from pyglet.app import exit
from src.settings import Settings_Scene
from src.game import Game_Scene



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
        director.push(Game_Scene())

    def settings(self):
        director.push(Settings_Scene())

    def on_quit(self):
        exit()


class Main_Scene(Scene):
    def __init__(self):
        super(Main_Scene, self).__init__()

        self.add(Main_Menu())


'''
This makes it so that when loading a resource (eg: creating a sprite object), the res folder will be treated as root
'''
pyglet.resource.path = ['../res']
pyglet.resource.reindex()

director.init(width=1600, height=900, autoscale=True, resizable=False)

director.run(Main_Scene())
