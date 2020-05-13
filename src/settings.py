import json
from copy import deepcopy

from pyglet.canvas import get_display

from cocos.menu import Menu, CENTER, MenuItem, MultipleMenuItem, ImageMenuItem
from cocos.director import director
from cocos.scene import Scene



default_settings = {
    'window': {
        'width': 1920,
        'height': 1080
    }
}

def read_settings():
    with open('../cfg/settings.json', 'r') as settings_json:
        return json.load(settings_json)

def write_settings(settings_dictionary):
    with open('../cfg/settings.json', 'w+') as settings_json:
        json.dump(settings_dictionary, settings_json, indent='\t')



class Settings_Menu(Menu):
    def __init__(self):
        super(Settings_Menu, self).__init__()

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

            #(MenuItem('Audio', self.audio_settings_callback)),
            (MenuItem('Graphics', self.graphics_settings_callback)),
            (MenuItem('Back', self.previous_scene))

        ]

        self.create_menu(menu_items)

    def audio_settings_callback(self):
        print('Audio Settings Callback invoked!')

    def graphics_settings_callback(self):
        director.push(Settings_Scene_Graphics())

    def previous_scene(self):
        director.pop()  # return to previous scene


class Settings_Menu_Graphics(Menu):
    def __init__(self):
        super(Settings_Menu_Graphics, self).__init__()

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

        self.window_sizes = [
            (960, 540),
            (1120, 630),
            (1280, 720),
            (1440, 810),
            (1600, 900),
            (1760, 990),
            (1920, 1080)
        ]


        self.menu_items = [


            (MultipleMenuItem(
                'Window Size: ',
                self.resize_window,
                [str(size) for size in self.window_sizes],
                self.window_sizes.index(tuple([value for value in read_settings()['window'].values()]))
            )),
            (MenuItem('Back', self.previous_scene))

        ]

        self.create_menu(self.menu_items)


    def resize_window(self, new_window_sizes_index):
        screen_width = get_display().get_default_screen().width
        screen_height = get_display().get_default_screen().height

        new_window_width = self.window_sizes[new_window_sizes_index][0]
        new_window_height = self.window_sizes[new_window_sizes_index][1]

        # Center the window using its new size
        new_window_x_position = screen_width//2 - new_window_width//2
        new_window_y_position = screen_height//2 - new_window_height//2
        director.window.set_location(new_window_x_position, new_window_y_position)
        director.window.set_size(new_window_width, new_window_height)

        new_settings_dictionary = deepcopy(default_settings)
        new_settings_dictionary['window'] = {'width': new_window_width, 'height': new_window_height}
        write_settings(new_settings_dictionary)


    def previous_scene(self):
        director.pop() # return to previous scene


class Settings_Scene(Scene):
    def __init__(self):
        super(Settings_Scene, self).__init__()

        self.add(Settings_Menu())



class Settings_Scene_Graphics(Scene):
    def __init__(self):
        super(Settings_Scene_Graphics, self).__init__()

        self.add(Settings_Menu_Graphics())

