from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.sprite import Sprite
from cocos.scene import Scene

from pyglet.window import key

from math import cos, sin, radians, fabs


class Background(ScrollableLayer):
    def __init__(self):
        super(Background, self).__init__()

        background_image = Sprite('mosaic_texture.png')
        self.add(background_image)


class Player_Ship_Layer(ScrollableLayer):

    def __init__(self):
        super(Player_Ship_Layer, self).__init__()

        self.ship = Sprite('player_ship.png')
        self.add(self.ship)


        self.ship.x = 0
        self.ship.y = 0

        self.ship.x_velocity = 0
        self.ship.y_velocity = 0

        self.ship.acceleration_rate = 1/10


        self.ship.rotation = 0
        self.ship.rotational_velocity = 0

        self.ship.rotational_acceleration_rate = 1/20


        self.ship.max_speed = 20
        self.ship.max_rotational_speed = 5


    def handle_key_input(self, keys):

        # Accelerate rotation counter-clockwise.
        if keys[key.symbol_string(key.A)]:
            self.ship.rotational_velocity -= self.ship.rotational_acceleration_rate

        # Accelerate rotation clockwise.
        if keys[key.symbol_string(key.D)]:
            self.ship.rotational_velocity += self.ship.rotational_acceleration_rate

        # Accelerate forward.
        if keys[key.symbol_string(key.W)]:
            self.ship.x_velocity += cos(radians(self.ship.rotation)) * self.ship.acceleration_rate
            self.ship.y_velocity -= sin(radians(self.ship.rotation)) * self.ship.acceleration_rate

        # Accelerate backward.
        if keys[key.symbol_string(key.S)]:
            self.ship.x_velocity -= cos(radians(self.ship.rotation)) * self.ship.acceleration_rate
            self.ship.y_velocity += sin(radians(self.ship.rotation)) * self.ship.acceleration_rate

        # Set both translational and rotational velocities to 0.
        if keys[key.symbol_string(key.SPACE)]:
            self.ship.x_velocity, self.ship.y_velocity, self.ship.rotational_velocity = 0, 0, 0

        # Set position and rotation to 0.
        if keys[key.symbol_string(key.R)]:
            self.ship.x, self.ship.y, self.ship.rotation = 0, 0, 0


    def update_ship_spacial_properties(self):

        self.ship.x += self.ship.x_velocity
        self.ship.y += self.ship.y_velocity
        self.ship.rotation += self.ship.rotational_velocity

        # Prevent the speed of the ship from exceeding its maximum.
        if self.ship.x_velocity**2 + self.ship.y_velocity**2 > self.ship.max_speed**2:
            self.ship.x_velocity *= 0.99
            self.ship.y_velocity *= 0.99

        # Prevent the rotational speed of the ship from exceeding its maximum.
        if fabs(self.ship.rotational_velocity) > self.ship.max_rotational_speed:
            self.ship.rotational_velocity *= 0.99


class Game(Layer):

    is_event_handler = True

    def __init__(self):
        super(Game, self).__init__()

        # ScrollingManager is what gives the camera effect of being able to follow the ship around the level.
        self.scrolling_manager = ScrollingManager()
        self.add(self.scrolling_manager)

        self.background = Background()
        self.scrolling_manager.add(self.background)

        self.player_ship_layer = Player_Ship_Layer()
        # This is just to create a reference shortcut for later, repeated use.
        self.player_ship = self.player_ship_layer.ship

        self.scrolling_manager.add(self.player_ship_layer)


        self.keys = {
            key.symbol_string(key.A): False,
            key.symbol_string(key.D): False,
            key.symbol_string(key.W): False,
            key.symbol_string(key.S): False,
            key.symbol_string(key.SPACE): False,
            key.symbol_string(key.R): False
        }



        # See the definition of the Game class's update function for an explanation.
        self.dt_accumulator = 0
        self.update_period = 1/60
        self.schedule(self.update)


    def on_key_press(self, k, modifiers):
        self.keys[key.symbol_string(k)] = True

    def on_key_release(self, k, modifiers):
        self.keys[key.symbol_string(k)] = False


    def update(self, dt):

        '''
        To keep a fairly regular update rate, the time since the last update is accumulated. When the accumulator is
        greater than the update period, an update is invoked, and then the accumulator is reduced by the update period.
        There may be some residual time left in the accumulator after this, which may build up over repeated iterations.
        If the accumulator holds a value equal to or greater than twice the update period, multiple update steps are
        invoked on the same update until the accumulator is reduced to a value less than the update period.
        '''
        self.dt_accumulator += dt
        while self.dt_accumulator > self.update_period:

            self.player_ship_layer.handle_key_input(self.keys)
            self.player_ship_layer.update_ship_spacial_properties()

            self.scrolling_manager.set_focus(self.player_ship.x, self.player_ship.y)

            self.dt_accumulator -= self.update_period




class Game_Scene(Scene):
    def __init__(self):
        super(Game_Scene, self).__init__()

        self.add(Game())