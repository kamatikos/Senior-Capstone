from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.tiles import load
from cocos.director import director
from cocos.actions import Move, MoveBy, IntervalAction
from cocos import mapcolliders
from cocos.euclid import Vector2, Point2
import random

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


class Entity_Layer(ScrollableLayer):

    def __init__(self, collision_handler):
        super(Entity_Layer, self).__init__()

        self.collision_handler = collision_handler

        self.player = Sprite('elf.png')
        self.player.position = (100, 100)
        self.player.speed = 150
        self.player.collide_map = self.collision_handler
        self.player.do(Player_Mover(self.player.speed))
        self.add(self.player)

        self.enemies = []


        self.schedule_interval(interval=1/120, callback=lambda dt :
            self.move_enemies(dt)
        )
        self.schedule_interval(interval=1, callback=lambda dt :
            self.spawn_bat_enemy(Point2(*self.player.position)+Point2(random.gauss(0, 300), random.gauss(0, 300)))
        )

    def move_enemies(self, dt):
        for enemy in self.enemies:
            velocity = enemy.speed * Vector2(enemy.quarry.x - enemy.x, enemy.quarry.y - enemy.y).normalized()
            last = enemy.get_rect()
            new = last.copy()
            new.x += velocity.x * dt
            new.y += velocity.y * dt
            enemy.velocity = enemy.collide_map(last, new, velocity.x, velocity.y)
            enemy.position = new.center

    def spawn_bat_enemy(self, location):
        enemy = Sprite('enemy_bat.png')
        enemy.position = location
        enemy.speed = 100
        enemy.collide_map = self.collision_handler
        enemy.quarry = self.player
        enemy.health = 1
        self.enemies.append(enemy)
        self.add(enemy)

class Player_Mover(Move):
    # step() is called every frame.
    # dt is the number of seconds elapsed since the last call.
    def init(self, speed):
        self.speed = speed

    def step(self, dt):
        if dt > 0.1:
            return

        # Determine velocity based on keyboard inputs.
        x_direction = KEYBOARD[key.D] - KEYBOARD[key.A]
        y_direction = KEYBOARD[key.W] - KEYBOARD[key.S]

        velocity = self.speed * Vector2(x_direction, y_direction).normalized()

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
        self.scrolling_manager.scale = 1.8
        self.add(self.scrolling_manager)

        #add the backgrounds to the map
        self.background = Background()
        self.scrolling_manager.add(self.background.layer1)
        self.scrolling_manager.add(self.background.layer2)
        self.scrolling_manager.add(self.background.layer3)
        self.scrolling_manager.add(self.background.layer4)


        # Attach a KeyStateHandler to the keyboard object.
        global KEYBOARD
        KEYBOARD = key.KeyStateHandler()
        director.window.push_handlers(KEYBOARD)

        mapcollider = mapcolliders.TmxObjectMapCollider()
        mapcollider.on_bump_handler = mapcollider.on_bump_bounce
        collision_handler = mapcolliders.make_collision_handler(mapcollider, self.background.colliders)

        self.entity_layer = Entity_Layer(collision_handler)

        self.scrolling_manager.add(self.entity_layer)


class Game_Scene(Scene):
    def __init__(self):
        super(Game_Scene, self).__init__()

        self.add(Game())