import arcade
import time

SCREEN_TITLE = 'Игра с собачкой'
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 450
PLAYER_MOVEMENT_SPEED = 5
RIGHT_FACING = 0
LEFT_FACING = 1
SPRITE_SCALING_PLAYER = 2.0

GRAVITY=1500
DEFAULT_DAMPING=1.0
PLAYER_DAMPING=0.4
PLAYER_FRICTION=1.0
WALL_FRICTION=0.7
DYNAMIC_ITEM_FRICTION=0.6
PLAYER_MASS=2.5
PLAYER_MAX_HORIZONTAL_SPEED=450
PLAYER_MAX_VERTICAL_SPEED=1600
PLAYER_MOVE_FORCE_ON_GROUND=8000
PLAYER_MOVE_FORCE_IN_AIR=900
PLAYER_JUMP_IMPULSE=1300

DEAD_ZONE=0.1
DISTANCE_TO_CHANGE_TEXTURE=20

TILE_SCALING = 0.4

class Bat(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.idle = True
        self.scale = SPRITE_SCALING_PLAYER
        main_path = 'resources/bat/'
        self.run_texture_pair = self.load_texture_pair(f'{main_path}/Bat1.png')
        self.run_textures = []
        for i in range(1, 3):
            texture = self.load_texture_pair(f'{main_path}/Bat{i}.png')
            self.run_textures.append(texture)
        self.texture = self.run_texture_pair[0]


        self.character_face_direction = LEFT_FACING
        self.cur_texture = 0
        self.x_odometer = 0
        self.center_x = 680
        self.center_y = 45
        self.move_direction = 1


    @staticmethod
    def load_texture_pair(filename):
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True),
        ]

    def on_update(self, delta_time: float = 1 / 60):
     self.center_x += 1 * self.move_direction
     if self.move_direction == 1 and self.center_x > 1100:
            self.move_direction = -1
            self.character_face_direction = RIGHT_FACING

     elif self.move_direction == -1 and self.center_x < 680:
            self.move_direction = 1
            self.character_face_direction = LEFT_FACING
     self.center_x += 1 * self.move_direction


    def update_animation(self, delta_time: float = 1 / 60):
            self.cur_texture += 0.125
            if self.cur_texture >= len(self.run_textures):
                self.cur_texture = 0
            current_index = int(self.cur_texture) % len(self.run_textures)
            self.texture = self.run_textures[current_index][self.character_face_direction]


class Dog(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.idle = True
        self.scale = SPRITE_SCALING_PLAYER
        self.stop = False
        self.gameover = False
        main_path = 'resources/1 Dog/'
        self.idle_texture_pair = self.load_texture_pair(f'{main_path}/Idle/Idle1.png')
        self.run_texture_pair = self.load_texture_pair(f'{main_path}/Walk/Walk1.png')
        self.run_textures = []
        for i in range(1, 6):
            texture = self.load_texture_pair(f'{main_path}/Walk/Walk{i}.png')
            self.run_textures.append(texture)
        self.texture = self.idle_texture_pair[0]
        self.idle_texture = []
        for i in range(1, 4):
            texture = self.load_texture_pair(f'{main_path}/Idle/Idle{i}.png')
            self.idle_texture.append(texture)
        self.texture = self.idle_texture[0][0]

        self.gameover_texture_pair = self.load_texture_pair(f'{main_path}/Death/Death1.png')
        self.gameover_texture = []
        for i in range(1, 4):
            texture = self.load_texture_pair(f'{main_path}/Death/Death{i}.png')
            self.gameover_texture.append(texture)
        self.texture = self.gameover_texture[0][0]


        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0
        self.x_odometer = 0


    @staticmethod
    def load_texture_pair(filename):
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True),
        ]


    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
      if self.stop == False:
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        is_on_ground = physics_engine.is_on_ground(self)

        self.x_odometer += dx

        if not is_on_ground:
            if dy > DEAD_ZONE or dy < -DEAD_ZONE:
                self.texture = self.run_texture_pair[self.character_face_direction]
                return

        if abs(dx) > DEAD_ZONE or abs(dy) > DEAD_ZONE:
            self.idle = False
        else:
            self.idle = True

        if self.idle:
            self.cur_texture += 0.125
            if self.cur_texture >= len(self.idle_texture):
                self.cur_texture = 0
            self.texture = self.idle_texture[int(self.cur_texture) % len(self.idle_texture)][
                self.character_face_direction]
        else:
            if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
                self.x_odometer = 0
                self.cur_texture += 1
                if self.cur_texture >= len(self.run_textures):
                    self.cur_texture = 0
                self.texture = self.run_textures[int(self.cur_texture) % len(self.run_textures)][
                    self.character_face_direction]
      else:
              self.cur_texture += 0.125
              if self.cur_texture >= len(self.gameover_texture) - 1:
                  self.gameover = True
              else:
                  self.cur_texture += 0.125
                  self.texture = self.gameover_texture[int(self.cur_texture) % len(self.gameover_texture)][self.character_face_direction]


class Second_Dog(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.cur_texture = 0
        self.call = False
        self.scale = SPRITE_SCALING_PLAYER
        self.stop = False
        main_path = 'resources/2 Dog/'
        self.idle_texture_pair = self.load_texture_pair(f'{main_path}/Dog1.png')
        self.idle_texture = []
        for i in range(1, 4):
            texture = self.load_texture_pair(f'{main_path}/Dog{i}.png')
            self.idle_texture.append(texture)
        self.texture = self.idle_texture[0][0]

        self.call_texture_pair = self.load_texture_pair(f'{main_path}/angry/Angry1.png')
        self.call_texture = []
        for i in range(1, 4):
            texture = self.load_texture_pair(f'{main_path}/angry/Angry{i}.png')
            self.call_texture.append(texture)
        self.texture = self.call_texture[0][0]

        self.cur_texture = 0
        self.x_odometer = 0

    @staticmethod
    def load_texture_pair(filename):
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, flipped_horizontally=True),
        ]


    def pymunk_moved(self, physics_engine, dx, dy, d_angle):
            if not self.call:
                self.cur_texture += 0.250
                if self.cur_texture >= len(self.call_texture):
                    self.cur_texture = 0
                self.texture = self.call_texture[int(self.cur_texture) % len(self.call_texture)][0]

            elif self.call:
                self.cur_texture += 0.125
                if self.cur_texture >= len(self.idle_texture):
                    self.cur_texture = 0
                self.texture = self.idle_texture[int(self.cur_texture) % len(self.idle_texture)][1]


class Game(arcade.Window):
   def __init__(self):
       super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate=1/30)
       self.bg_layer = arcade.load_texture('resources/1 Dog/back3.jpg')
       self.physics_engine = arcade.PymunkPhysicsEngine
       self.left_pressed = False
       self.right_pressed = False
       self.up_pressed: bool = False
       self.down_pressed:bool = False
       self.stop = False
       self.sound_played = False
       self.music = arcade.Sound('resources/sounds/lost-soul_30sec-177569.mp3')
       self.music.play(0.5, 0, True, 1)

   def setup(self):
       self.player = Dog()
       self.enemy = Bat()
       self.friend = Second_Dog()
       self.player.center_x = 50
       self.player.center_y = 100
       self.friend.center_x = 1900
       self.friend.center_y = 100
       self.platform_list = arcade.SpriteList()

       for i in range(10):
           platform = arcade.SpriteSolidColor(200, 20, (16, 40, 43))
           platform.center_x = i * 200 + 100
           platform.bottom = 0
           self.platform_list.append(platform)

       damping = DEFAULT_DAMPING
       gravity = (0, -GRAVITY)
       self.physics_engine = arcade.PymunkPhysicsEngine(damping=damping, gravity=gravity)
       self.physics_engine.add_sprite(self.player, friction=PLAYER_FRICTION, mass=PLAYER_MASS,
                                      moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="player",
                                      max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                      max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
       self.physics_engine.add_sprite(self.friend, friction=PLAYER_FRICTION, mass=10,
                                      moment=arcade.PymunkPhysicsEngine.MOMENT_INF, collision_type="player",
                                      max_horizontal_velocity=PLAYER_MAX_HORIZONTAL_SPEED,
                                      max_vertical_velocity=PLAYER_MAX_VERTICAL_SPEED)
       self.physics_engine.add_sprite_list(self.platform_list, friction=WALL_FRICTION, collision_type="wall",
                                           body_type=arcade.PymunkPhysicsEngine.STATIC)

       self.bridge_list = arcade.SpriteList()

       coordinate_list = [ [695, 105], [720, 105], [745, 105], [770, 105], [1050,125], [1075,125], [1100,125]]
       for coordinate in coordinate_list:
           bridge = arcade.Sprite("resources/1 Dog/wooden-platform.png", TILE_SCALING)
           bridge.position = coordinate
           self.bridge_list.append(bridge)

       for bridge in self.bridge_list:
           self.physics_engine.add_sprite(bridge, friction=WALL_FRICTION, collision_type="wall",
                                          body_type=arcade.PymunkPhysicsEngine.STATIC)

       self.barrell_list = arcade.SpriteList()
       coordinate_list = [[200, 34], [500, 34], [563, 34], [626, 34], [1150,38]]
       for coordinate in coordinate_list:
           barrell = arcade.Sprite('resources/1 Dog/barrell.png', 0.7)
           barrell.position = coordinate
           self.barrell_list.append(barrell)

       coordinate_list = [[-6, 50], [-6, 90], [-6, 160],[-6, 270], [2005, 50], [2005, 90],  [2005, 160],[2005, 270],]
       for coordinate in coordinate_list:
           barrell = arcade.Sprite('resources/1 Dog/barrell.png', 0.7)
           barrell.position = coordinate
           barrell.alpha = 0
           self.barrell_list.append(barrell)


       for barrell in self.barrell_list:
           self.physics_engine.add_sprite(barrell, friction=WALL_FRICTION, collision_type="wall",
                                          body_type=arcade.PymunkPhysicsEngine.STATIC)

       self.bone_list = arcade.SpriteList()
       coordinate_list = [[200, 115], [563, 90], [800, 200], [900, 200], [1000, 200]]
       for coordinate in coordinate_list:
           bone = arcade.Sprite('resources/1 Dog/bone2.png', 0.07)
           bone.position = coordinate
           self.bone_list.append(bone)


   def on_update(self, delta_time):
       self.physics_engine.step()
       self.player.update_animation()
       is_on_ground = self.physics_engine.is_on_ground(self.player)
       if self.left_pressed and not self.right_pressed:
        if is_on_ground:
           force = (-PLAYER_MOVE_FORCE_ON_GROUND, 0)
        else:
           force = (-PLAYER_MOVE_FORCE_IN_AIR, 0)
        self.physics_engine.apply_force(self.player, force)
        self.physics_engine.set_friction(self.player, 0)
       elif self.right_pressed and not self.left_pressed:
        if is_on_ground:
           force = (PLAYER_MOVE_FORCE_ON_GROUND, 0)
        else:
            force = (PLAYER_MOVE_FORCE_IN_AIR, 0)
        self.physics_engine.apply_force(self.player, force)
        self.physics_engine.set_friction(self.player, 0)
       else:
           self.physics_engine.set_friction(self.player, 1.0)


       self.view_left = self.player.center_x - SCREEN_WIDTH / 2
       self.view_bottom = 0
       self.view_left = max(self.view_left, 0)
       self.view_left = min(self.view_left, 1000)
       self.view_bottom = max(self.view_bottom, 0)
       arcade.set_viewport(self.view_left,
                           SCREEN_WIDTH + self.view_left,
                           self.view_bottom,
                           SCREEN_HEIGHT + self.view_bottom)

       if arcade.check_for_collision_with_list(self.player, self.bone_list):
           hit_list = arcade.check_for_collision_with_list(self.player, self.bone_list)
           for bone in hit_list:
               bone.remove_from_sprite_lists()
       if arcade.check_for_collision(self.player, self.enemy):
          self.player.stop = True
       if self.player.gameover:
           self.sound = arcade.Sound('resources/sounds/minecraft-dog-pain-3.mp3')
           self.sound.play()
           time.sleep(1)
           self.setup()
       if 1600 <= self.player.center_x <= 1900 :
           self.friend.call = True
       if 1400 <= self.player.center_x <= 1900 and not self.sound_played:
           self.sound_played = True
           self.sound = arcade.Sound('resources/sounds/minecraft-dog-bark.mp3')
           self.sound.play()



   def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
       print(f'{x=}')
       print(f'{y=}')


   def on_draw(self):
               self.clear()
               arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer)
               arcade.draw_lrwh_rectangle_textured(1000, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg_layer)
               self.player.draw()
               self.friend.draw()
               self.enemy.draw()
               self.platform_list.draw()
               self.bridge_list.draw()
               self.barrell_list.draw()
               self.bone_list.draw()
               self.player.update_animation()
               self.enemy.on_update()
               self.enemy.update_animation()


   def on_key_press(self, key, modifiers):
               if key == arcade.key.LEFT or key == arcade.key.A:
                   self.left_pressed = True
                   self.player.idle = False
               elif key == arcade.key.RIGHT or key == arcade.key.D:
                   self.right_pressed = True
                   self.player.idle = False
               elif key == arcade.key.UP or key == arcade.key.W:
                   self.up_pressed = True
                   self.player.idle = False
                   if self.physics_engine.is_on_ground(self.player):
                       impulse = (0, PLAYER_JUMP_IMPULSE)
                       self.physics_engine.apply_impulse(self.player, impulse)
               elif key == arcade.key.DOWN or key == arcade.key.S:
                   self.down_pressed = True
                   self.player.idle = False


   def on_key_release(self, key, modifiers):
               if key == arcade.key.LEFT or key == arcade.key.A:
                   self.left_pressed = False
                   self.player.idle = True
               elif key == arcade.key.RIGHT or key == arcade.key.D:
                   self.right_pressed = False
                   self.player.idle = True



if __name__ == '__main__':
   game = Game()
   game.setup()
   arcade.run()