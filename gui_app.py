import pygame
import pygame_gui

# App constants
APP_SIZE = APP_WEIGHT, APP_HEIGHT = 400, 600
BACKGROUND_COLOR = "#505050"


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Time Tracker")
        self.time_delta = 0.0
        self._display = pygame.display.set_mode(
            APP_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self._clock = pygame.time.Clock()
        self.gui_manager = pygame_gui.UIManager(APP_SIZE)
        self.hello_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 40), (100, 50)),
            text="Hi!",
            manager=self.gui_manager,
        )
        self._running = True

    def on_init(self):
        pass

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.gui_manager.process_events(event)

    def on_loop(self):
        self.gui_manager.update(self.time_delta)

    def on_render(self):
        self._display.fill(BACKGROUND_COLOR)
        self.gui_manager.draw_ui(self._display)

        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            self.time_delta = self._clock.tick(60) / 1000.0
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
