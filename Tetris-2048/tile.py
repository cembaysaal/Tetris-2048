import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
import numpy as np
import copy as cp
from point import Point
# Class used for modeling numbered tiles as in 2048
class Tile:
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Times New Roman ", 20

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self, position = Point(0,0)):
      # BURASI DÜZENLENECEK
      # set the number on the tile
      numbers = [2, 4]
      number = int(np.random.choice(numbers, 1))
      self.number = number
      self.position = Point(position.x, position.y)
      if self.number == 2:
         self.background_color = Color(238, 228, 218)
         self.foreground_color = Color(0, 0, 0)  # foreground (number) color
      elif self.number == 4:
         self.background_color = Color(237, 224, 200)
         self.foreground_color = Color(0, 0, 0)  # foreground (number) color
      self.box_color = Color(0, 0, 0)
   def change (self):
      if self.number == 2:
         self.background_color = Color(238, 228, 218)
         self.foreground_color = Color(0, 0, 0)  # foreground (number) color
      elif self.number == 4:
         self.background_color = Color(237, 224, 200)
         self.foreground_color = Color(0, 0, 0)
      elif self.number == 8:
         self.background_color = Color(242, 177, 121)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 16:
         self.background_color = Color(245, 149, 99)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 32:
         self.background_color = Color(246, 124, 95)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 64:
         self.background_color = Color(246, 94, 59)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 128:
         self.background_color = Color(237, 207, 114)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 256:
         self.background_color = Color(237, 204, 97)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 512:
         self.background_color = Color(237, 200, 80)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 1024:
         self.background_color = Color(237, 197, 63)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      elif self.number == 2048:
         self.background_color = Color(237, 194, 46)
         self.foreground_color = Color(0, 100, 200)  # foreground (number) color
      else:
         self.background_color = Color(0, 0, 0)
         self.foreground_color = Color(0, 100, 200)
         # set the colors of the tile
        # foreground (number) color

   # Method for drawing the tile
   def draw(self, position, length = 1):
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      self.change()
      stddraw.text(position.x, position.y, str(self.number))
   def move(self, dx, dy):
      self.position.translate(dx, dy)