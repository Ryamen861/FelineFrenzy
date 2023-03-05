import pygame.mouse


class Button:

    def __init__(self, x, y, image, screen, func_name):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.func_name = func_name

        self.is_clicked = False

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_click(self):
        # get the position of the mouse to know when the button is clicked
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1 and self.is_clicked is False:
            self.is_clicked = True
            self.func_name()

        if pygame.mouse.get_pressed()[0] == 0:
            # if it is not clicked, then reset it back to false
            self.is_clicked = False


