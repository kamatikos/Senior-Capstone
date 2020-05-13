# These 3 lines maintain the pixelated nature of textures
from pyglet.gl import *
glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer.base_layers import Layer
from pyglet.app import exit
from src.settings import Settings_Scene
from src.settings import read_settings, default_settings
from src.game import Game_Scene


class Background(Layer):
    def __init__(self):
        super(Background, self).__init__()

        background = Sprite('title.png')
        self.position = (settings['window']['width']/2,settings['window']['height']/2)
        self.add(background)


class Main_Menu(Menu):
    def __init__(self):
        super(Main_Menu, self).__init__()

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        self.font_item = {
            'font_name': 'Bauhaus 93',
            'font_size': 32,
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (192, 192, 192, 255),
            'dpi': 96,
        }
        self.font_item_selected = {
            'font_name': 'Bauhaus 93',
            'font_size': 42,
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'color': (255, 255, 255, 255),
            'dpi': 96,
        }

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

        self.add(Main_Menu(),z=1)
        self.add(Background(),z=0)



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
