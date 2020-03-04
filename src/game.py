from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.tiles import MapLayer
from cocos.sprite import Sprite
from cocos.scene import Scene

from pyglet.image import load
from pyglet.window import key



class Background(ScrollableLayer):
    def __init__(self):
        super(Background, self).__init__()

        self.add(Sprite(load('../res/mosaic_texture.png')))


class Player_Ship(ScrollableLayer):

    def __init__(self):
        super(Player_Ship, self).__init__()

        self.sprite = Sprite(load('../res/player_ship.png'))

        self.sprite.position = (0, 0)

        self.velocity = (0, 0)
        self.acceleration_rate = 0.25

        self.angular_velocity = 0
        self.angular_acceleration_rate = 0.25

        self.add(self.sprite)

    def set_position(self, position):
        self.position = position

    def set_velocity(self, velocity):
        self.velocity = velocity

    def modify_velocity(self, velocity_delta):
        velocity_x, velocity_y = self.velocity
        velocity_delta_x, velocity_delta_y = velocity_delta
        self.velocity = (velocity_x + velocity_delta_x, velocity_y + velocity_delta_y)

    def update_position(self):
        position_x, position_y = self.sprite.position
        position_delta_x, position_delta_y = self.velocity
        self.set_position((position_x + position_delta_x, position_y + position_delta_y))





class Game(Scene):

    #keyboard = key.KeyStateHandler()

    def __init__(self):
        super(Game, self).__init__()


        self.scrolling_manager = ScrollingManager()


        self.background = Background()
        #self.player_ship = Player_Ship()


        self.add(self.background)
        #self.add(self.player_ship)
        '''
        self.keys = {
            key.symbol_string(key.A): False,
            key.symbol_string(key.D): False,
            key.symbol_string(key.W): False,
            key.symbol_string(key.S): False,
            key.symbol_string(key.Q): False,
            key.symbol_string(key.E): False,
            key.symbol_string(key.SPACE): False
        }
        '''
        self.schedule(self.update)

        self.dt_accumulator = 0
        self.update_period = 1.0 / 60
        self.schedule(self.update)

        self.zx, self.zy = 0, 0
    '''
    def on_key_press(self, k, modifiers):
        self.keys[key.symbol_string(k)] = True

    def on_key_release(self, k, modifiers):
        self.keys[key.symbol_string(k)] = False
    '''

    def update(self, dt):

        self.dt_accumulator += dt


        while self.dt_accumulator > self.update_period:

            self.scrolling_manager.set_focus(self.zx, self.zy)
            self.zx += 1
            self.zy += 1

            print(self.zx, self.zy)

            '''
            velocity_delta_x, velocity_delta_y = 0, 0

            if self.keys[key.symbol_string(key.A)]:
                velocity_delta_x += -self.player_ship.acceleration_rate
            if self.keys[key.symbol_string(key.D)]:
                velocity_delta_x += self.player_ship.acceleration_rate
            if self.keys[key.symbol_string(key.W)]:
                velocity_delta_y += self.player_ship.acceleration_rate
            if self.keys[key.symbol_string(key.S)]:
                velocity_delta_y += -self.player_ship.acceleration_rate
            if self.keys[key.symbol_string(key.SPACE)]:
                velocity_delta_x, velocity_delta_y = 0, 0
                self.player_ship.set_velocity((0, 0))

            self.player_ship.modify_velocity((velocity_delta_x, velocity_delta_y))
            self.player_ship.update_position()

            self.set_focus(*self.player_ship.position)

            print(self.player_ship.position)
            '''
            self.dt_accumulator -= self.update_period
