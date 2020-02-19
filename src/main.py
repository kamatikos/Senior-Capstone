from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from pyglet.app import exit



class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Title')

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        menuItems = [

            (MenuItem('Item A', self.itemACallback)),
            (MenuItem('Item B', self.itemBCallback)),
            (MenuItem('Exit', self.onQuit)),

        ]

        self.create_menu(menuItems)

    def itemACallback(self):
        print('Item A Callback invoked!')

    def itemBCallback(self):
        print('Item B Callback invoked!')

    def onQuit(self):
        exit()

director.init()

director.run(Scene(MainMenu()))