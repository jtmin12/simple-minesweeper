import pygame, sys
from pygame.locals import QUIT
import random

#beginner minesweeper: 8x8, 10 mines
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (150, 150, 150)
DARKER_GREY = (114, 114, 114)
LIGHT_GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


class Board():

  def __init__(self):
    self.mines = []
    self.tiles = pygame.sprite.Group()

    self.lost = False

    combinations = []
    for i in range(8):
      for j in range(8):
        combinations.append((i, j))

    self.mines = random.sample(combinations, 10)

    for j in range(8):
      for i in range(8):
        surrounding_mines = []
        for x in [-1, 0, 1]:
          for y in [-1, 0, 1]:
            if ((x + i, y + j) in self.mines):
              surrounding_mines.append((x + i, y + j))
        tile_ = Tile(i * 50, j * 50, (i, j) in self.mines,
                     len(surrounding_mines), self)
        self.tiles.add(tile_)

  def uncover_mines(self, x, y):
    surrounding_tiles = []
    for i in [-1, 0, 1]:
      for j in [-1, 0, 1]:
        if (x + i >= 0 and y + j >= 0 and x + i < 8 and y + j < 8):
          for tile in self.tiles:
            if tile.x == (x + i) * 50 and tile.y == (y + j) * 50:
              surrounding_tiles.append(tile)

    for tile in surrounding_tiles:
      if not tile.uncovered and not tile.is_mine:
        tile.uncovered = True
        tile.image.fill(DARK_GREY)
        pygame.draw.rect(tile.image, DARKER_GREY, pygame.Rect(0, 0, 50, 50), 1)
        if (tile.number > 0):
          draw_text(str(tile.number), BLACK, tile.image, 47, 47, 50)
        else:
          self.uncover_mines(tile.x // 50, tile.y // 50)


class Tile(pygame.sprite.Sprite):

  def __init__(self, x, y, is_mine, number, board):
    super().__init__()
    self.x = x
    self.y = y
    self.is_mine = is_mine

    self.number = number
    self.board = board

    self.left_clicked = False
    self.right_clicked = False
    self.uncovered = False

    self.marked = False

    self.image = pygame.Surface((50, 50))
    self.image.fill(LIGHT_GREY)

    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)

    pygame.draw.polygon(self.image, WHITE,
                        ((0, 0), (50, 0), (45, 5), (5, 5), (5, 50), (0, 50)))
    pygame.draw.polygon(self.image, DARK_GREY, ((0, 50), (50, 50), (50, 0),
                                                (45, 5), (45, 45), (5, 45)))
    pygame.draw.rect(self.image, DARKER_GREY, pygame.Rect(0, 0, 50, 50), 1)

  def on_right_click(self):
    if (not self.uncovered and not self.marked):
      pygame.draw.polygon(self.image, BLACK,
                          ((15, 40), (39, 40), (32, 33), (29, 33), (29, 23),
                           (27, 23), (27, 33), (22, 33)))
      pygame.draw.polygon(self.image, RED,
                          ((29, 25), (29, 11), (27, 11), (14, 19)))
      self.marked = True
    elif (not self.uncovered and self.marked):
      self.image.fill(LIGHT_GREY)
      pygame.draw.polygon(self.image, WHITE,
                          ((0, 0), (50, 0), (45, 5), (5, 5), (5, 50), (0, 50)))
      pygame.draw.polygon(self.image, DARK_GREY, ((0, 50), (50, 50), (50, 0),
                                                  (45, 5), (45, 45), (5, 45)))
      pygame.draw.rect(self.image, DARKER_GREY, pygame.Rect(0, 0, 50, 50), 1)
      self.marked = False

  def on_left_click(self):
    if (not self.uncovered and not self.marked):
      self.image.fill(DARK_GREY)  #CHANGE
      pygame.draw.rect(self.image, DARKER_GREY, pygame.Rect(0, 0, 50, 50), 1)
      self.uncovered = True
      if (self.is_mine):
        pygame.draw.circle(self.image, RED, (50 // 2, 50 // 2), 10)
        self.board.lost = True
      elif (self.number == 0):
        board.uncover_mines(self.x // 50, self.y // 50)
      else:
        draw_text(str(self.number), BLACK, self.image, 47, 47, 50)

  def update(self):
    pos = pygame.mouse.get_pos()

    if self.rect.collidepoint(pos):
      if pygame.mouse.get_pressed()[0] and self.left_clicked == False:
        self.left_clicked = True
        self.on_left_click()

      if pygame.mouse.get_pressed()[2] and self.right_clicked == False:
        self.right_clicked = True
        self.on_right_click()

    if not pygame.mouse.get_pressed()[0]:
      self.left_clicked = False
    if not pygame.mouse.get_pressed()[2]:
      self.right_clicked = False


def draw_text(text, color, surface, w, h, size):
  font = pygame.font.SysFont(pygame.font.get_default_font(), size)
  msg = font.render(text, False, color)
  width, height = font.size(text)
  xoffset = (w - width) // 2
  yoffset = (h - height) // 2
  surface.blit(msg, (xoffset, yoffset))
  pygame.display.update()


def fade():
  faded_bg = pygame.Surface((400, 400))
  faded_bg.fill(BLACK)
  for alpha in range(0, 150):
    faded_bg.set_alpha(alpha)
    board.tiles.draw(DISPLAYSURF)
    DISPLAYSURF.blit(faded_bg, (0, 0))
    pygame.display.update()
    pygame.time.wait(1)


pygame.init()

DISPLAYSURF = pygame.display.set_mode((400, 400))

pygame.display.set_caption('Minesweeper')

board = Board()
DISPLAYSURF.fill(BLACK)

running = True

while running:
  for event in pygame.event.get():
    if event.type == QUIT:
      running = False

  board.tiles.update()
  board.tiles.draw(DISPLAYSURF)
  pygame.display.update()

  won = True
  for tile in board.tiles:
    if not tile.is_mine and not tile.uncovered:
      won = False
      break

  if board.lost:
    for tile in board.tiles:
      if tile.is_mine and not tile.uncovered:
        tile.on_left_click()
        pygame.time.wait(300)
        board.tiles.draw(DISPLAYSURF)
        pygame.display.update()
    fade()
    draw_text("YOU LOSE :(", RED, DISPLAYSURF, 400, 400, 80)
    running = False

  if won:
    fade()
    draw_text("YOU WIN!", GREEN, DISPLAYSURF, 400, 400, 80)
    running = False
