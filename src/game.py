#
import pygame
import random
from src.trail import Trail
from src import utils
from src.window_manager import WindowManager
from src.rendered_text import RenderedText
from src.constants import FPS, GREEN, MAX_TRAILS

# Done? TODO Blit letters to the Trail surface
# Done? TODO Remove off screen trails only when new trails are made
# TODO Space same size letters apart to prevent overlapping

TRAIL_TIMER = pygame.USEREVENT + 0
MOUSE_TIMER = pygame.USEREVENT + 1

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.letter_group = SizeSortedDrawGroup(screen)
        self.trail_group = pygame.sprite.Group()
        self.screen.fill("black")
        self.clock = pygame.time.Clock()
        self.makeTrails(10)
        self.bounds = pygame.Rect((0, 0), pygame.display.get_window_size())
        self.blured = False
        self.debug_mode = False
        self._init_timers()

    def makeTrails(self, amount):
        for i in range(amount):
            trail = Trail(GREEN,self.trail_group, self.letter_group)
            self.trail_group.add(trail)

    def _init_timers(self):
        pygame.time.set_timer(TRAIL_TIMER, random.randint(100, 500))
        pygame.time.set_timer(MOUSE_TIMER, 1000)

    def hide_cursor(self):
        if pygame.mouse.get_visible():
            pygame.mouse.set_visible(False)

    def clear_screen(self):
        self.screen.fill('black')

    def quit(self):
        WindowManager.quit()
        pygame.quit()
        raise SystemExit

    def update_bounds(self):
        self.bounds = pygame.Rect((0, 0), pygame.display.get_window_size())

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == TRAIL_TIMER:
                pygame.time.set_timer(TRAIL_TIMER, random.randint(100, 500))
                self._add_new_trails()
            if event.type == pygame.MOUSEMOTION and not pygame.mouse.get_visible():
                pygame.mouse.set_visible(True)
            if event.type == MOUSE_TIMER and pygame.mouse.get_visible():
                pygame.time.set_timer(MOUSE_TIMER, 1000)
                self.hide_cursor()
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
                elif event.key == pygame.K_b:
                    self.blured = not self.blured
                elif event.key == pygame.K_d:
                    self.debug_mode = not self.debug_mode

    def _add_new_trails(self):
        if len(self.trail_group) < MAX_TRAILS:
            amount = min(10, MAX_TRAILS - len(self.trail_group))
            self.makeTrails(amount)


    def _handle_trails(self, dt):
        self.trail_group.update()
        self.letter_group.update(dt)
        self.letter_group.customDraw()
        

    def blur(self):
        new_surf = pygame.transform.smoothscale(self.screen, (self.bounds.width // 2, self.bounds.height // 2))
        new_surf = pygame.transform.smoothscale(new_surf, (self.bounds.width, self.bounds.height))
        self.screen.blit(new_surf, (0, 0))

    def display_fps(self):
        text = f"FPS: {self.clock.get_fps():.0f} " \
               f"Trails: {len(self.trail_group)} " \
               f"Letters: {sum([len(trail.letters) for trail in self.trail_group])}"
        size = 18
        rendered_text = RenderedText.font_objects[size].render(text, True, 'white')
        rendered_text_shadow = RenderedText.font_objects[size].render(text, True, 'purple')
        self.screen.blit(rendered_text_shadow, (-1, -1))
        self.screen.blit(rendered_text, (0, 0))

    def run(self):
        while True:
            dt = self.clock.tick_busy_loop(FPS)
            self._handle_events()
            self.clear_screen()
            self._handle_trails(dt)
            if self.blured:
                self.blur()
            if not self.debug_mode:
                self.display_fps()
            pygame.display.flip()



class SizeSortedDrawGroup(pygame.sprite.Group):
    def __init__(self,surface):
        super().__init__()
        self.display_surface = surface

    def customDraw(self):
        if pygame.time.get_ticks() % 2:
            for letter in sorted(self.sprites(),key = lambda letter: letter.size):
                self.display_surface.blit(letter.image, letter.rect.topleft)
        else:
            for letter in self.sprites():
                self.display_surface.blit(letter.image, letter.rect.topleft)