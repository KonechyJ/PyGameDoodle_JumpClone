#!/usr/bin/env python3
"""Class that has functions and classes to create the title screen for the snake game"""
from enum import Enum
import pygame
import pygame.freetype
from pygame.sprite import Sprite


BLUE = (51, 51, 255)
WHITE = (255, 255, 255)


def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """Returns surface with text written on"""
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    """creates a clickable interface for the title"""
    #pylint: disable=too-many-arguments
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False
        default_image = create_surface_with_text(text=text, font_size=font_size,
                                                 text_rgb=text_rgb, bg_rgb=bg_rgb)

        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2,
                                                     text_rgb=text_rgb, bg_rgb=bg_rgb)
        if action == GameState.TEXT:
            self.images = [default_image, default_image]
            self.rects = [default_image.get_rect(center=center_position),
                          default_image.get_rect(center=center_position)]
        else:
            self.images = [default_image, highlighted_image]
            self.rects = [default_image.get_rect(center=center_position),
                          highlighted_image.get_rect(center=center_position)]
        super().__init__()
        self.action = action
    @property
    def image(self):
        """returns the image of self"""
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        """returns a rect of mouse going over it"""
        return self.rects[1] if self.mouse_over else self.rects[0]
    #could not change the update to fix the lasting issues for update it was to important for my code
    #pylint: disable=arguments-differ
    #pylint: disable=inconsistent-return-statements
    def update(self, mouse_pos, mouse_up):
        """updates mouse position"""
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                #pylint: disable=inconsistent-return-statements
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class GameState(Enum):
    """action class for what happens when you click"""
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    RULES = 2
    TEXT = 3
    GAME_OVER = 4

def title_screen(screen):
    """creates the interface for the title screen"""
    game_title = UIElement(
        center_position=(200, 100),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Doodle JumpClone",
        action=GameState.TEXT,
    )

    start_btn = UIElement(
        center_position=(200, 300),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )


    buttons = [start_btn, game_title]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            #needs this for the wording to highlight while hoviering
            #pylint: disable=no-member
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


    while True:
        mouse_up = False
        for event in pygame.event.get():
            #needs this for the wording to highlight while hoviering
            #pylint: disable=no-member
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)


        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()
