#
import pygame
import random
from src.trail import Trail
from src import utils
from src.window_manager import WindowManager
from src.rendered_text import RenderedText
from src.constants import FPS, GREEN, MAX_TRAILS

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.fill("black")
        self.clock = pygame.time.Clock()
        self.trails = utils.make(Trail, 10, args=[GREEN])
        self.trail_timer = 0
        self.reset_timer()
        self.bounds = pygame.Rect((0, 0), pygame.display.get_window_size())
        self.debug_mode = False

    def hide_cursor(self):
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)

    def clear_screen(self):
        self.screen.fill('black')

    def reset_timer(self):
        self.trail_timer = random.randint(100, 500)

    def quit(self):
        WindowManager.quit()
        pygame.quit()
        raise SystemExit

    def update_bounds(self):
        self.bounds = pygame.Rect((0, 0), pygame.display.get_window_size())
        [trail.update_bounds(self.bounds) for trail in self.trails]

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.MOUSEMOTION and not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.quit()
                elif event.key == pygame.K_w:
                    # Experimental
                    self.screen = WindowManager.toggle_wallpaper()
                    self.update_bounds()
                elif event.key == pygame.K_f:
                    self.screen = WindowManager.toggle_fullscreen()
                    self.update_bounds()
                elif event.key == pygame.K_d:
                    self.debug_mode = not self.debug_mode

    def remove_offscreen(self):
        self.trails[:] = [trail for trail in self.trails if any(letter.rect.y < self.bounds.height for letter in trail.letters)]

    def sort_biggest_last(self):
        self.trails.sort(reverse=False, key=lambda t: t.letters[0].size)

    def _handle_trail_timer(self, dt):
        if self.trail_timer <= 0 and len(self.trails) < MAX_TRAILS:
            self.reset_timer()
            amount = min(random.randint(5, 10), MAX_TRAILS - len(self.trails))
            self.trails += utils.make(Trail, amount, args=[GREEN])
        self.trail_timer -= dt

    def _handle_trails(self, dt):
        [(trail.update(dt), trail.draw(self.screen)) for trail in self.trails]

    def blur(self):
        new_surf = pygame.transform.smoothscale(self.screen, (self.bounds.width // 2, self.bounds.height // 2))
        new_surf = pygame.transform.smoothscale(new_surf, (self.bounds.width, self.bounds.height))
        self.screen.blit(new_surf, (0, 0))

    def display_fps(self):
        text = f"FPS: {self.clock.get_fps():.0f} " \
               f"Trails: {len(self.trails)} " \
               f"Letters: {sum([len(trail.letters) for trail in self.trails])}"
        rendered_text = RenderedText.font_objects[18].render(text, True, 'white')
        rendered_text_shadow = RenderedText.font_objects[18].render(text, True, 'purple')
        self.screen.blit(rendered_text_shadow, (-1, -1))
        self.screen.blit(rendered_text, (0, 0))

    def run(self):
        while True:
            dt = self.clock.tick_busy_loop(FPS)
            self._handle_events()
            self._handle_trail_timer(dt)

            self.clear_screen()
            self._handle_trails(dt)
            #self.blur()
            if pygame.time.get_ticks() % 2:
                self.remove_offscreen()
                self.sort_biggest_last()
                self.hide_cursor()
            if self.debug_mode:
                self.display_fps()
            pygame.display.flip()



