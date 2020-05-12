from cocos.layer import ScrollingManager, ScrollableLayer, Layer
from cocos.sprite import Sprite
from cocos.scene import Scene
from cocos.tiles import load
from cocos.director import director
from cocos.actions import Move, FadeOut, FadeIn, sequence, CallFuncS
from cocos import mapcolliders
from cocos.euclid import Vector2, Point2
from math import atan2, degrees
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
        self.player.velocity = Vector2(0, 0)
        self.player.collide_map = self.collision_handler
        self.player.shot_cooldown = {'remaining': 0, 'time': 1}
        self.player.do(Player_Mover(self.player.speed))
        self.add(self.player)

        self.enemies = []
        self.arrows = []


        self.schedule_interval(interval=1/120, callback=lambda dt :
            self.game_loop(dt)
        )
        self.schedule_interval(interval=2, callback=lambda dt :
            self.spawn_bat_enemy(Point2(*self.player.position)+Point2(random.gauss(0, 300), random.gauss(0, 300)))
        )

    def game_loop(self, dt):
        self.move_enemies(dt)
        self.shoot_arrow()
        self.move_arrows(dt)
        self.arrow_cooldown(dt)
        self.arrow_lives(dt)
        self.detect_enemy_kills()

    def arrow_cooldown(self, dt):
        if self.player.shot_cooldown['remaining'] < 0:
            self.player.shot_cooldown['remaining'] = 0
        else:
            self.player.shot_cooldown['remaining'] -= dt


    def move_enemies(self, dt):
        for enemy in self.enemies:
            velocity = enemy.speed * Vector2(enemy.quarry.x - enemy.x, enemy.quarry.y - enemy.y).normalized()
            last = enemy.get_rect()
            new = last.copy()
            new.x += velocity.x * dt
            new.y += velocity.y * dt
            enemy.velocity = enemy.collide_map(last, new, velocity.x, velocity.y)
            enemy.position = new.center

    def move_arrows(self, dt):
        for arrow in self.arrows:
            last = arrow.get_rect()
            new = last.copy()
            new.x += arrow.velocity.x * dt
            new.y += arrow.velocity.y * dt
            arrow.velocity = Vector2(*arrow.collide_map(last, new, *arrow.velocity))
            if last == new:
                arrow.life_remaining = 0
            arrow.position = new.center

    def create_arrow(self, direction_vector):
        arrow = Sprite('arrow.png')
        arrow.position = Point2(*self.player.position)
        arrow.velocity = 400 * direction_vector + Vector2(*self.player.velocity)
        arrow.rotation = degrees(atan2(arrow.velocity.x, arrow.velocity.y))
        arrow.collide_map = self.collision_handler
        arrow.life_remaining = 10
        self.arrows.append(arrow)
        self.add(arrow)

    def shoot_arrow(self):
        if self.player.shot_cooldown['remaining'] <= 0:
            shot_fired = False
            if KEYBOARD[key.UP]:
                self.create_arrow(Vector2(0, 1))
                shot_fired = True
            elif KEYBOARD[key.DOWN]:
                self.create_arrow(Vector2(0, -1))
                shot_fired = True
            elif KEYBOARD[key.RIGHT]:
                self.create_arrow(Vector2(1, 0))
                shot_fired = True
            elif KEYBOARD[key.LEFT]:
                self.create_arrow(Vector2(-1, 0))
                shot_fired = True

            if shot_fired:
                shot_fired = False
                self.player.shot_cooldown['remaining'] = self.player.shot_cooldown['time']

    def arrow_lives(self, dt):
        for arrow in self.arrows:
            if arrow.life_remaining > 0:
                arrow.life_remaining -= dt
            else:
                self.arrows.remove(arrow)
                arrow.do(sequence(FadeOut(20), CallFuncS(lambda this_arrow: self.remove(this_arrow))))

    def spawn_bat_enemy(self, location):
        enemy = Sprite('enemy_bat.png')
        location.x = min(max(location.x, 35), 930)
        location.y = min(max(location.y, 60), 530)
        enemy.position = location
        enemy.speed = 200
        enemy.collide_map = self.collision_handler
        enemy.quarry = self.player
        enemy.health = 1
        enemy.opacity = 0
        self.add(enemy)
        enemy.do(
            sequence(
                FadeIn(min(enemy.quarry.speed/Vector2(enemy.quarry.x - enemy.x, enemy.quarry.y - enemy.y).magnitude(), 3)),
                CallFuncS(lambda this_enemy: self.enemies.append(this_enemy))
            )
        )

    def detect_enemy_kills(self):
        for arrow in self.arrows:
            for enemy in self.enemies:
                if (Vector2(*arrow.position) - Vector2(*enemy.position)).magnitude() < 20:
                    arrow.color = (255, 0, 0)
                    enemy.color = (255, 0, 0)
                    self.arrows.remove(arrow)
                    self.enemies.remove(enemy)
                    arrow.do(
                        sequence(
                            FadeOut(0.5),
                            CallFuncS(lambda this_arrow: self.remove(this_arrow))
                        )
                    )
                    enemy.do(
                        sequence(
                            FadeOut(0.5),
                            CallFuncS(lambda this_enemy: self.remove(this_enemy))
                        )
                    )


class Player_Mover(Move):
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
        self.target.velocity = Vector2(*self.target.collide_map(last, new, velocity.x, velocity.y))
        self.target.position = new.center


class Game(Layer):

    is_event_handler = True

    def __init__(self):
        super(Game, self).__init__()

        # ScrollingManager is what gives the camera effect of being able to follow the ship around the level.
        self.scrolling_manager = ScrollingManager()
        self.scrolling_manager.scale = 2.5
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
        mapcollider.on_bump_handler = mapcollider.on_bump_stick
        collision_handler = mapcolliders.make_collision_handler(mapcollider, self.background.colliders)

        self.entity_layer = Entity_Layer(collision_handler)

        self.scrolling_manager.add(self.entity_layer)
        self.schedule_interval(interval=1/240, callback=lambda dt:
            self.scrolling_manager.set_focus(*self.entity_layer.player.position)
        )


class Game_Scene(Scene):
    def __init__(self):
        super(Game_Scene, self).__init__()

        self.add(Game())