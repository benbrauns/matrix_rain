#
import pygame
from src.constants import WIDTH, HEIGHT, TITLE

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.mouse.set_visible(False)
    hwnd = pygame.display.get_wm_info()['window']

    from src.game import Game
    from src.window_manager import WindowManager
    game = Game(screen)
    WindowManager.init(hwnd)
    try:
        game.run()
    except (KeyboardInterrupt, Exception) as err:
        WindowManager.quit()
        raise err

if __name__ == '__main__':
    main()





