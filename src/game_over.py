from cocos.menu import Menu, CENTER, MenuItem
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
from cocos.layer.base_layers import Layer
from cocos.text import RichLabel
from cocos.euclid import Point2

class Background(Layer):
    def __init__(self):
        super(Background, self).__init__()

        background = Sprite('title.png')
        x, y = director.get_window_size()
        self.position = (x//2, y//2)
        self.add(background)


class Game_Over_Menu(Menu):
    def __init__(self, font):
        super(Game_Over_Menu, self).__init__()

        self.menu_valign = CENTER
        self.menu_halign = CENTER

        self.font_item = font.copy()
        self.font_item['font_size'] = 32
        self.font_item['color'] = (192, 192, 192, 255)

        self.font_item_selected = font.copy()
        self.font_item_selected['font_size'] = 42
        self.font_item_selected['color'] = (255, 255, 255, 255)

        menu_items = [

            (MenuItem('Main Menu', self.main_menu)),
            (MenuItem('Exit', self.on_quit))
        ]

        self.create_menu(menu_items)

    def main_menu(self):
        director.pop()

    def on_quit(self):
        exit()


class Stats_Layer(Layer):
    def __init__(self, font, stats):
        super(Stats_Layer, self).__init__()

        self.font_item = font.copy()
        self.font_item['font_size'] = 32
        self.font_item['color'] = (255, 255, 255, 255)

        self.time_text = RichLabel(
            text='{:02d}:{:02d}'.format(stats['time'] // 60, stats['time'] % 60),
            position=Point2(director.get_window_size()[0]*(1/3), director.get_window_size()[1]*(2/3)),
            **self.font_item
        )

        self.kills_text = RichLabel(
            text='➶ {}'.format(stats['kills']),
            position=Point2(director.get_window_size()[0]*(2/3), director.get_window_size()[1]*(2/3)),
            **self.font_item
        )

        self.add(self.time_text)
        self.add(self.kills_text)




class Game_Over_Scene(Scene):
    def __init__(self, stats):
        super(Game_Over_Scene, self).__init__()

        font = {
            'font_name': 'Bauhaus 93',
            'bold': False,
            'italic': False,
            'anchor_y': 'center',
            'anchor_x': 'center',
            'dpi': 96,
        }

        self.add(Background())
        self.add(Game_Over_Menu(font))
        self.add(Stats_Layer(font, stats))


