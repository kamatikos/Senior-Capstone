from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.tiles import load
from cocos.director import director
from cocos.actions import Move
from cocos import mapcolliders
from cocos.euclid import Vector2

from pyglet.window import key


class Background:
    def __init__(self):
        super(Background, self).__init__()

        #load map from tmx file
        bg = load("map.tmx")
        self.layer1 = bg["background"]
        self.layer2 = bg["ground"]
        self.layer3 = bg["walls"]
        self.layer4 = bg["obstacle"]
        self.colliders = bg["colliders"]


class Player_Layer(ScrollableLayer):

    def __init__(self,collision_handler):
        super(Player_Layer, self).__init__()

        self.character = Sprite('elf.png')
        self.add(self.character)

        self.character.x = 100
        self.character.y = 100

        self.character.velocity = (0,0)
        self.character.collide_map = collision_handler
        self.character.do(Mover())

class Mover(Move):
    # step() is called every frame.
    # dt is the number of seconds elapsed since the last call.
    def step(self, dt):
        if dt > 0.1:
            return




        # Determine velocity based on keyboard inputs.
        velocity_magnitude = 150

        x_direction = keyboard[key.RIGHT] - keyboard[key.LEFT]
        y_direction = keyboard[key.UP] - keyboard[key.DOWN]
        velocity = velocity_magnitude * Vector2(x_direction, y_direction).normalized()

        dx = velocity.x * dt
        dy = velocity.y * dt

        last = self.target.get_rect()

        new = last.copy()
        new.x += dx
        new.y += dy

        # Set the object's velocity.
        self.target.velocity = self.target.collide_map(last, new, velocity.x, velocity.y)

        self.target.position = new.center


class Game(Layer):

    is_event_handler = True

    def __init__(self):
        super(Game, self).__init__()

        # ScrollingManager is what gives the camera effect of being able to follow the ship around the level.
        self.scrolling_manager = ScrollingManager()
        self.add(self.scrolling_manager)

        #add scrolling manager to  the map
        self.background = Background()
        self.scrolling_manager.add(self.background.layer1)
        self.scrolling_manager.add(self.background.layer2)
        self.scrolling_manager.add(self.background.layer3)
        self.scrolling_manager.add(self.background.layer4)


        global keyboard

        # Attach a KeyStateHandler to the keyboard object.
        keyboard = key.KeyStateHandler()
        director.window.push_handlers(keyboard)

        mapcollider = mapcolliders.TmxObjectMapCollider()
        mapcollider.on_bump_handler = mapcollider.on_bump_bounce
        collision_handler = mapcolliders.make_collision_handler(mapcollider, self.background.colliders)

        self.player_ship_layer = Player_Layer(collision_handler)
        # This is just to create a reference shortcut for later, repeated use.
       # self.player_ship = self.player_ship_layer.ship

        self.scrolling_manager.add(self.player_ship_layer)




class Game_Scene(Scene):
    def __init__(self):
        super(Game_Scene, self).__init__()

        self.add(Game())