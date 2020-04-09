# These 3 lines maintain the pixelated nature of textures
from pyglet.gl import *
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from pyglet.app import exit
from src.settings import Settings_Scene
from src.settings import read_settings, default_settings
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



# This makes it so that when loading a resource (eg: creating a sprite object), the res folder will be treated as root
pyglet.resource.path = ['../res']
pyglet.resource.reindex()

settings = read_settings()

director.init(
    caption="Capstone Game",
    width=default_settings['window']['width'],
    height=default_settings['window']['height'],
    autoscale=True,
    resizable=False,
    fullscreen=False, # settings['fullscreen'],
    visible=False # initialized as invisible to hide the window resizing done below
)
director.window.set_size(settings['window']['width'], settings['window']['height'])
director.window.set_visible(visible=True)
director.run(Main_Scene())
