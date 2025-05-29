import arcade
import random
import time


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_RADIUS = 30
TARGET_COUNT = 1
GAME_DURATION = 30
TARGET_LIFETIME = 1.0
SCORE_TO_WIN = 20

class Target(arcade.SpriteCircle):
    def init(self, radius, color):
        super().init(radius, color)
        self.change_x = random.uniform(-3, 3)  #
        self.change_y = random.uniform(-3, 3)
        self.spawn_time = time.time()

    def update(self):
        super().update()

        if time.time() - self.spawn_time > TARGET_LIFETIME:
            self.remove_from_sprite_lists()

class ClickerShooter(arcade.Window):
    def init(self):
        super().init(SCREEN_WIDTH, SCREEN_HEIGHT, "Кликер-шутер")
        self.target_list = None
        self.score = 0
        self.game_start_time = None
        self.game_active = False
        self.setup()

    def setup(self):
        self.target_list = arcade.SpriteList()
        self.score = 0
        self.game_active = False

    def on_draw(self):
        arcade.start_render()
        self.target_list.draw()


        if self.game_active:
            time_left = max(0, GAME_DURATION - (time.time() - self.game_start_time))
            arcade.draw_text(f"Очки: {self.score}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 20)
            arcade.draw_text(f"Время: {int(time_left)}", 10, SCREEN_HEIGHT - 60, arcade.color.WHITE, 20)
        else:
            arcade.draw_text("Нажми ПРОБЕЛ, чтобы начать!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, 30, anchor_x="center")

    def on_update(self, delta_time):
        if not self.game_active:
            return


        if time.time() - self.game_start_time >= GAME_DURATION:
            self.game_active = False
            if self.score >= SCORE_TO_WIN:
                arcade.draw_text("Победа!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                 arcade.color.GOLD, 50, anchor_x="center")
            else:
                arcade.draw_text("Время вышло!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                 arcade.color.RED, 50, anchor_x="center")


        if len(self.target_list) == 0:
            target = Target(TARGET_RADIUS, arcade.color.RED)
            target.center_x = random.randint(TARGET_RADIUS, SCREEN_WIDTH - TARGET_RADIUS)
            target.center_y = random.randint(TARGET_RADIUS, SCREEN_HEIGHT - TARGET_RADIUS)
            self.target_list.append(target)

        self.target_list.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.game_active:
            return


        hit_targets = arcade.get_sprites_at_point((x, y), self.target_list)
        for target in hit_targets:
            target.remove_from_sprite_lists()
            self.score += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and not self.game_active:
            self.game_active = True
            self.game_start_time = time.time()
            self.score = 0

def main():
    game = ClickerShooter()
    game.setup()
    arcade.run()

if __name__ == "main":
    main()