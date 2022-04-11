from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes
import numpy as np
import lib.stddraw as stddraw
from sound import *
from gui_helper import *
from tile import *
from point import Point


''' A 2048 Tetris game created by Ayhan Aysoy, Cem Baysal, and Recep Barkın Topcu'''
# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
class Tetris:
   def start(self):
      # set the dimensions of the game grid
      grid_h, grid_w = 20, 20
      game_width = 12
      # set the size of the drawing canvas
      canvas_h, canvas_w = 40 * grid_h, 40 * grid_w
      stddraw.setCanvasSize(canvas_w, canvas_h)
      # set the scale of the coordinate system
      stddraw.setXscale(-0.5, grid_w - 0.5)
      stddraw.setYscale(-0.5, grid_h - 0.5)

      # Keeps the round count of the game
      self.round_count = 0
      # create the game grid
      sound = MusicSound()
      grid = GameGrid(grid_h, game_width)
      gui_helper = GUI_helper()

      # Create current tetromino and next tetrominos
      n = 1
      tetrominos = self.create_tetromino(grid_h, game_width)
      tetrominos_saver = tetrominos[9]
      current_tetromino = tetrominos[0]
      next_tetromino = tetrominos[1]
      hold_tetromino = None
      grid.current_tetromino = current_tetromino
      grid.next_tetromino = next_tetromino
      tile =  Tile(position = Point(0,0))
      self.show_next_piece_position(next_tetromino)
      self.empty_hold_tetromino = False


      # Keeps information if the game restarted
      self.restart = False
      # Keeps information if the game paused
      self.is_paused = False
      # Keeps information if the game finished
      self.is_finished = False
      self.game_over = False

      # display a simple menu before opening the game
      self.display_game_menu(grid_h, grid_w, grid, sound,gui_helper)
      # create the first tetromino to enter the game grid
      # by using the create_tetromino function defined below



      # the main game loop (keyboard interaction for moving the tetromino)
      while True:
         # check user interactions via the keyboard
         if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
            key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
            # if the left arrow key has been pressed
            if key_typed == "left":
               # move the active tetromino left by one
               current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # move the active tetromino right by one
               current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
               # move the active tetromino down by one
               # (soft drop: causes the tetromino to fall down faster)
               current_tetromino.move(key_typed, grid)
            # Turn the tetromino 90 degrees clockwise.
            elif key_typed == "up":
               current_tetromino.rotate(grid, current_tetromino)
            # Turn the tetromino 90 degrees counterclockwise.
            elif key_typed == "z":
               current_tetromino.reverse_rotate(grid, current_tetromino)
            # drop the piece bottom
            elif key_typed =="space":
               self.drop_piece(current_tetromino,grid)
            # hold the current tetromino
            elif key_typed == "h":
               current_tetromino,hold_tetromino,n = self.hold_tetromino(current_tetromino,next_tetromino,hold_tetromino,n,grid,tetrominos,grid_h,game_width)
            # clear the queue of the pressed keys for a smoother interaction
            elif key_typed == "p":
               # Pauses the game
               self.is_paused = not self.is_paused
               self.display_game_menu(grid_h, grid_w, grid, sound,gui_helper)
            stddraw.clearKeysTyped()
         if not self.is_paused:
            success = current_tetromino.move("down", grid)

         # move the active tetromino down by one at each iteration (auto fall)
         # place the active tetromino on the grid when it cannot go down anymore
         if not success:
            # get the tile matrix of the tetromino without empty rows and columns
            # and the position of the bottom left cell in this matrix
            tiles, pos = grid.current_tetromino.get_min_bounded_tile_matrix(True)
            # update the game grid by locking the tiles of the landed tetromino
            self.game_over = grid.update_grid(tiles, pos)
            row = self.clear_full_lines(grid_h, grid_w, grid)
            index = 0
            tetrominos, n, current_tetromino, next_tetromino,tetrominos_saver = self.show_next_piece(tetrominos,n,current_tetromino,next_tetromino,tetrominos_saver,grid,grid_h,game_width)

            merge = self.check_merge(grid,tile)
            while merge:
               merge = self.check_merge(grid,tile)

            while index < grid_h:
               while row[index]:
                  self.update_grid(row, grid)
                  row = self.clear_full_lines(grid_h, grid_w, grid)
               index += 1
            # end the main game loop if the game is over
            # merge = check_merge(grid)
            # while merge:
            #    merge = check_merge(grid)

            if self.game_over:
               print("Game Over")
               self.is_finished = True
               self.display_game_menu(grid_h, grid_w, grid,sound,gui_helper)
            self.round_count += 1
            grid.current_tetromino = current_tetromino
            if self.round_count == 8:
               self.tetrominos = list()
               self.round_count = 0
               self.create_tetromino(grid_h, game_width)
         if self.restart:
            for a in range(0,20):
               for b in range(12):
                   grid.tile_matrix[a][b] = None
            self.restart = False
            grid.game_over = False
            grid.current_tetromino = current_tetromino

         # display the game grid and the current tetromino
         grid.display()

   def clear_full_lines(self, grid_h, grid_w, grid):
      row = [False for i in range(grid_h)]
      point = 0
      for i in range(grid_h):
         counter = 0
         for j in range(grid_w):
            if grid.is_occupied(i, j):
               counter += 1
            if counter == 12:
               point = 0
               for x in range(12):
                  point += grid.tile_matrix[i][x].number
               row[i] = True
      grid.point += point
      grid.last_point += point
      return row

   def update_grid(self, row, grid):
      for index, i in enumerate(row):
         if i:
            for a in range(index, 19):
               row = np.copy(grid.tile_matrix[a + 1])
               grid.tile_matrix[a] = row
               for b in range(12):
                  if grid.tile_matrix[a][b] is not None:
                     grid.tile_matrix[a][b].move(0, -1)
            break

   # If the numbers of two tiles in a row are equal, match them.
   def check_merge(self, grid, tile):
      changed = False
      #  check every row and column
      for i in range(0, 19):
         for j in range(12):
            # Check the selected line and the one above it
            if grid.tile_matrix[i][j] != None and grid.tile_matrix[i + 1][j] != None:
               if grid.tile_matrix[i][j].number == grid.tile_matrix[i + 1][j].number:
                  # add the top and bottom and explode the top
                  grid.tile_matrix[i][j].number += grid.tile_matrix[i + 1][j].number
                  grid.tile_matrix[i + 1][j] = None
                  number = 16
                  ra = 5
                  if i < number:
                     # If there are idle tiles on top, drop them
                     for a in range(1, ra):
                        if grid.tile_matrix[i + a][j] != None and grid.tile_matrix[i + a - 1][j] == None:
                           grid.tile_matrix[i + a - 1][j] = grid.tile_matrix[i + a][j]
                           grid.tile_matrix[i + a][j] = None
                           if i == 15:
                              number += 1
                              ra -= 1
                  grid.point += grid.tile_matrix[i][j].number
                  changed = True
      self.eliminate_gapes(grid)
      return changed

   # If you have tile left in the air, add it number the point
   def eliminate_gapes(self, grid):
      for a in range(1, 19):
         for b in range(11):
            # check out the bras up to 9
            if b <= 9:
               # When only one tile is alone and around empty
               if grid.tile_matrix[a][b] != None and grid.tile_matrix[a][b + 1] == None and grid.tile_matrix[a][
                  b - 1] == None:
                  # If the bottom line is empty, delete it and add it number to point.
                  if grid.tile_matrix[a - 1][b] == None and grid.tile_matrix[a - 1][b - 1] == None and \
                          grid.tile_matrix[a - 1][b + 1] == None:
                     grid.point += grid.tile_matrix[a][b].number
                     grid.tile_matrix[a][b] = None
               # Empty it with the tile on your right
               if grid.tile_matrix[a][b] != None and grid.tile_matrix[a][b + 1] != None and grid.tile_matrix[a][
                  b - 1] == None:
                  # If the bottom line is empty, delete it and add it number to point.
                  if grid.tile_matrix[a][b - 1] == None and grid.tile_matrix[a - 1][b - 1] == None and \
                          grid.tile_matrix[a - 1][b] == None and \
                          grid.tile_matrix[a - 1][b + 1] == None and grid.tile_matrix[a - 1][b + 2] == None and \
                          grid.tile_matrix[a][b + 2] == None:
                     grid.point += grid.tile_matrix[a][b].number
                     grid.point += grid.tile_matrix[a][b + 1].number
                     grid.tile_matrix[a][b + 1] = None
                     grid.tile_matrix[a][b] = None
               # If it is empty along with the tile to the left
               if b <= 8:
                  if grid.tile_matrix[a][b] != None and grid.tile_matrix[a][b + 1] == None and grid.tile_matrix[a][
                     b - 1] != None:
                     # If the bottom line is empty, delete it and add it number to point.
                     if grid.tile_matrix[a - 1][b + 1] == None and grid.tile_matrix[a - 1][b] == None and \
                             grid.tile_matrix[a - 1][b - 1] == None and grid.tile_matrix[a - 1][b - 2] == None and \
                             grid.tile_matrix[a][b - 2] == None:
                        grid.point += grid.tile_matrix[a][b].number
                        grid.point += grid.tile_matrix[a][b - 1].number
                        grid.tile_matrix[a][b - 1] = None
                        grid.tile_matrix[a][b] = None
               if b == 9:
                  # if the column number is equal to 9, to prevent the error that will occur here
                  if grid.tile_matrix[a][b + 1] != None and grid.tile_matrix[a][b + 2] != None and grid.tile_matrix[a][
                     b] == None:
                     # If the bottom line is empty, delete it and add it number to point.
                     if grid.tile_matrix[a - 1][b + 1] == None and grid.tile_matrix[a - 1][b] == None and \
                             grid.tile_matrix[a - 1][b + 2] == None:
                        grid.point += grid.tile_matrix[a][b + 1].number
                        grid.point += grid.tile_matrix[a][b + 2].number
                        grid.tile_matrix[a][b + 2] = None
                        grid.tile_matrix[a][b + 1] = None
               # If all three are empty together
               if grid.tile_matrix[a][b] != None and grid.tile_matrix[a][b + 1] != None and grid.tile_matrix[a][
                  b - 1] != None:
                  # If the bottom line is empty, delete it and add it number to point.
                  if grid.tile_matrix[a][b - 2] == None and grid.tile_matrix[a][b + 2] == None and \
                          grid.tile_matrix[a - 1][b - 2] == None and grid.tile_matrix[a - 1][b - 1] == None and \
                          grid.tile_matrix[a - 1][b] == None \
                          and grid.tile_matrix[a - 1][b + 1] == None and grid.tile_matrix[a - 1][b + 2] == None:
                     grid.point += grid.tile_matrix[a][b].number
                     grid.point += grid.tile_matrix[a][b - 1].number
                     grid.point += grid.tile_matrix[a][b + 1].number
                     grid.tile_matrix[a][b + 1] = None
                     grid.tile_matrix[a][b - 1] = None
                     grid.tile_matrix[a][b] = None
               # destroy the trio that will remain on the right in case Z or S arrives
               if grid.tile_matrix[a][b] != None and grid.tile_matrix[a][b + 1] != None and grid.tile_matrix[a + 1][
                  b] != None:
                  # If the bottom line is empty, delete it and add it number to point.
                  if grid.tile_matrix[a - 1][b - 1] == None and grid.tile_matrix[a - 1][b] == None and \
                          grid.tile_matrix[a - 1][b + 1] == None and grid.tile_matrix[a - 1][b + 2] == None and \
                          grid.tile_matrix[a][b - 1] == None and grid.tile_matrix[a][b + 2] == None and \
                          grid.tile_matrix[a + 1][b - 1] == None and grid.tile_matrix[a + 1][b + 1] == None and \
                          grid.tile_matrix[a + 1][b + 2] == None and \
                          grid.tile_matrix[a + 2][b - 1] == None and grid.tile_matrix[a + 2][b] == None and \
                          grid.tile_matrix[a + 2][b + 1] == None:
                     grid.point += grid.tile_matrix[a][b]
                     grid.point += grid.tile_matrix[a][b + 1]
                     grid.point += grid.tile_matrix[a + 1][b]
                     grid.tile_matrix[a][b + 1] = None
                     grid.tile_matrix[a + 1][b] = None
                     grid.tile_matrix[a][b] = None
               # destroy the trio that will remain on the left in case Z or S arrives
               if grid.tile_matrix[a][b] != None and grid.tile_matrix[a][b + 1] != None and grid.tile_matrix[a - 1][
                  b] != None:
                  # If the bottom line is empty, delete it and add it number to point.
                  if grid.tile_matrix[a - 1][b + 1] == None and grid.tile_matrix[a - 1][b] == None and \
                          grid.tile_matrix[a - 1][b - 1] == None and grid.tile_matrix[a - 1][b - 2] == None and \
                          grid.tile_matrix[a][b + 1] == None and grid.tile_matrix[a][b - 2] == None and \
                          grid.tile_matrix[a + 1][b + 1] == None and grid.tile_matrix[a + 1][b - 1] == None and \
                          grid.tile_matrix[a + 1][b - 2] == None and \
                          grid.tile_matrix[a + 2][b + 1] == None and grid.tile_matrix[a + 2][b] == None and \
                          grid.tile_matrix[a + 2][b - 1] == None:
                     grid.point += grid.tile_matrix[a][b]
                     grid.point += grid.tile_matrix[a][b + 1]
                     grid.point += grid.tile_matrix[a - 1][b]
                     grid.tile_matrix[a][b + 1] = None
                     grid.tile_matrix[a - 1][b] = None
                     grid.tile_matrix[a][b] = None
            # if the row number is equal to 10, check the ones on the left and do the operation
            if b == 10:
               # If the bottom line is empty, delete it and add it number to point.
               if grid.tile_matrix[a][b + 1] != None and grid.tile_matrix[a][b] == None:
                  if grid.tile_matrix[a - 1][b] == None and grid.tile_matrix[a - 1][b + 1] == None:
                     grid.point += grid.tile_matrix[a][b + 1].number
                     grid.tile_matrix[a][b + 1] = None

   # A fucntion that creates tetromino
   def create_tetromino(self,grid_height, grid_width):
      # type (shape) of the tetromino is determined randomly
      tetromino_types = ['I', 'O', 'Z', 'S', 'T', 'L', 'J']
      # Save the tetrominos in list
      tetrominos = []
      for x in range(10):
         random_index = random.randint(0, len(tetromino_types) - 1)
         random_type = tetromino_types[random_index]
         # create and return the tetromino
         tetromino = Tetromino(random_type, grid_height, grid_width)
         tetrominos.append(tetromino)
      return tetrominos
   # A function that shows next current tetromino
   def show_next_piece(self,tetrominos, n, current_tetromino, next_tetromino, tetrominos_saver, grid, grid_h, game_width):
      current_tetromino = tetrominos[n]
      current_tetromino.bottom_left_cell.y = grid_h
      current_tetromino.bottom_left_cell.x = random.randint(0, game_width - len(current_tetromino.tile_matrix))
      next_tetromino = tetrominos[n + 1]
      n = n + 1
      grid.current_tetromino = current_tetromino
      grid.next_tetromino = next_tetromino
      self.show_next_piece_position(next_tetromino)
      # If last tetromino comes, save the last tetromino and restart n
      if n == 9:
         tetrominos = self.create_tetromino(grid_h, game_width)
         tetrominos.insert(0, tetrominos_saver)
         tetrominos_saver = tetrominos[9]
         tetrominos.pop(10)
         n = 0
      return tetrominos, n, current_tetromino, next_tetromino, tetrominos_saver
   # Position of next tetromino
   def show_next_piece_position(self,next_tetromino):
      # position of O tetromino
      if len(next_tetromino.tile_matrix) == 2:
         next_tetromino.bottom_left_cell.y = 11
         next_tetromino.bottom_left_cell.x = 15.3
      # position of I tetromino
      elif len(next_tetromino.tile_matrix) == 4:
         next_tetromino.bottom_left_cell.y = 10
         next_tetromino.bottom_left_cell.x = 14.8
      # position of other tetrominos
      else:
         next_tetromino.bottom_left_cell.y = 10
         next_tetromino.bottom_left_cell.x = 14.8
   # A function that holds the current tetromino and change with hold tetromino
   def hold_tetromino(self,current_tetromino,next_tetromino,hold_tetromino,n,grid,tetromino,grid_h,game_width):
      # If there is nothing in hold tetromino, do current tetromino as hold tetromino and show next tetromino
      if self.empty_hold_tetromino == False:
         hold_tetromino = current_tetromino
         grid.hold_tetromino = hold_tetromino
         self.show_hold_tetromino_position(hold_tetromino)
         current_tetromino = next_tetromino
         current_tetromino.bottom_left_cell.y = grid_h
         current_tetromino.bottom_left_cell.x = random.randint(0, game_width - len(current_tetromino.tile_matrix))
         grid.current_tetromino = current_tetromino
         next_tetromino = tetromino[n+1]
         grid.next_tetromino = next_tetromino
         self.show_next_piece_position(next_tetromino)
         n = n+1
         self.empty_hold_tetromino = True
         return current_tetromino, hold_tetromino,n
      # If there is a tetromino in hold tetromino, change with current tetromino
      else:
         positon_saver_y = current_tetromino.bottom_left_cell.y
         positon_saver_x = current_tetromino.bottom_left_cell.x
         hold_tetromino_saver = current_tetromino
         current_tetromino = hold_tetromino
         current_tetromino.bottom_left_cell.y = positon_saver_y
         current_tetromino.bottom_left_cell.x = positon_saver_x
         grid.current_tetromino = current_tetromino
         hold_tetromino = hold_tetromino_saver
         grid.hold_tetromino = hold_tetromino
         self.show_hold_tetromino_position(hold_tetromino)
         return current_tetromino, hold_tetromino, n
   # Position of hold tetromino
   def show_hold_tetromino_position(self,hold_tetromino):
      # position of O tetromino
      if len(hold_tetromino.tile_matrix) == 2:
         hold_tetromino.bottom_left_cell.y = 5
         hold_tetromino.bottom_left_cell.x = 15.3
      # position of I tetromino
      elif len(hold_tetromino.tile_matrix) == 4:
         hold_tetromino.bottom_left_cell.y = 4
         hold_tetromino.bottom_left_cell.x = 14.8
      # position of other tetrominos
      else:
         hold_tetromino.bottom_left_cell.y = 4
         hold_tetromino.bottom_left_cell.x = 14.8
   # A function that drops the piece in bottom
   def drop_piece(self,current_tetromino,grid):
      while current_tetromino.can_be_moved("down",grid):
         current_tetromino.bottom_left_cell.y -= 1


   def display_game_menu(self, grid_height, grid_width, grid, sound,gui_helper):
      # colors used for the menu
      sound.play_sound(stopped=True)
      background_color = Color(0, 0, 0)
      button_color = Color(25, 255, 228)
      text_color = Color(31, 160, 239)
      # clear the background canvas to background_color
      stddraw.clear(background_color)
      # get the directory in which this python code file is placed
      current_dir = os.path.dirname(os.path.realpath(__file__))
      # path of the image file
      img_file = current_dir + "/images/menu_image.png"
      # center coordinates to display the image
      img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
      # image is represented using the Picture class
      image_to_display = Picture(img_file)
      # display the image
      stddraw.picture(image_to_display, img_center_x, img_center_y)
      # dimensions of the start game button
      button_w, button_h = grid_width - 1.5, 2
      # coordinates of the bottom left corner of the start game button
      button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
      # display the start game button as a filled rectangle
      stddraw.setPenColor(button_color)
      # display the text on the start game button
      stddraw.setFontFamily("Arial")
      stddraw.setFontSize(25)
      stddraw.setPenColor(text_color)
      gui_helper.main_menu()
      START = False
      OPTIONS = False

      # Game pause
      if not self.is_finished and self.is_paused:
            gui_helper.pause_menu()
            while True:
               stddraw.show(50)
               clicked = stddraw.mousePressed()
               if clicked:
                  mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
                  # Closes the menu end continue to game
                  if mouse_x >= 6.5 and mouse_x <= 12.5:
                     if mouse_y >= 7 and mouse_y <= 9:
                        self.is_paused = False
                        break
               # Go back the menu
                  if mouse_x >= 6.5 and mouse_x <= 12.5:
                     if mouse_y >= 4 and mouse_y <= 6:
                        self.is_paused = False
                        self.restart = True
                        self.is_finished = False
                        self.game_over = False
                        grid.point = 0
                        self.display_game_menu(grid_height,grid_width, grid, sound,gui_helper)
                        hold_tetromino = None
                        grid.hold_tetromino = None
                        self.empty_hold_tetromino = False
                        break
      # Game over
      elif self.is_finished:
         sound.game_over_sound()
         gui_helper.game_over(grid.score)
         while True:
            stddraw.show(50)
            if stddraw.mousePressed():
               # get the x and y coordinates of the location at which the mouse has
               # most recently been left-clicked
               mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
               if mouse_x >= 6.5 and mouse_x <= 12.5:
                  if mouse_y >= 7 and mouse_y <= 9:
                     self.restart = True
                     grid.speed_increased_counter = 0
                     self.is_paused = False
                     self.is_finished = False
                     self.game_over = False
                     # resets the score
                     grid.score = 0
                     grid.point = 0
                     # back to menu
                     self.display_game_menu(grid_height, grid_width, grid, sound,gui_helper)
                     break
      else:
         # Main menu
         while True:
            # display the menu and wait for a short time (50 ms)
            stddraw.show(50)
            clicked = stddraw.mousePressed()
            # Checks to that user if clicks Start or options
            if clicked and START is False and OPTIONS is False:
               mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
               #If user clicked start button show the speed options
               if mouse_x >= 6.5 and mouse_x <= 12.5:
                  if mouse_y >= 7 and mouse_y <= 9:
                     START = True
                     # Calling speed buttons
                     gui_helper.speed_choose()
                     clicked = False
               #If user clicked options button show the options
               if mouse_x >= 6.5 and mouse_x <= 12.5:
                  if mouse_y >= 4 and mouse_y <= 6:
                     OPTIONS = True
                     gui_helper.options(current_dir)
                     clicked = False
            # If user clicked Start button show speed buttons
            if clicked and START is True:
               mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
               #Let user to chose speed of tetrominos
               if mouse_x >= 1 and mouse_x <= 5 and mouse_y >= 7 and mouse_y <= 9:
                     grid.game_speed = 500
                     break
               elif mouse_x >= 7.5 and mouse_x <= 11.5 and mouse_y >= 7 and mouse_y <= 9:
                     grid.game_speed = 200
                     break
               elif mouse_x >= 14 and mouse_x <= 18 and mouse_y >= 7 and mouse_y <= 9:
                     grid.game_speed = 75
                     break
               #If user clicked go back menu, back to menu
               elif mouse_x >= 6.5 and mouse_x <= 12.5 and mouse_y >= 4 and mouse_y <= 6:
                     START = False
                     gui_helper.clear_buttons()
                     gui_helper.main_menu()
            # If user clicked options button, show options
            if clicked and OPTIONS is True:
               mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
               # if user change sound, change sound
               if mouse_x >= 5.75 and mouse_x <= 6 and mouse_y >= 7.75 and mouse_y <= 8.325:
                     # if user clicked off sound logo, sound volume is off
                     sound_text ="off"
                     gui_helper.clear_buttons()
                     gui_helper.options(current_dir)
                     gui_helper.sound_buttons(sound_text)
                     sound.sound_volume = 0
               elif mouse_x >= 7.75 and mouse_x <= 8 and mouse_y >= 7.75 and mouse_y <= 8.325:
                    # if user clicked low sound logo, sound volume is low
                     sound_text ="low"
                     gui_helper.clear_buttons()
                     gui_helper.options(current_dir)
                     gui_helper.sound_buttons(sound_text)
                     sound.sound_volume = 0.2
               elif mouse_x >= 9.85 and mouse_x <= 10.15 and mouse_y >= 7.75 and mouse_y <= 8.325:
                    # if user clicked medium sound logo, sound volume is medium
                     sound_text ="med"
                     gui_helper.clear_buttons()
                     gui_helper.options(current_dir)
                     gui_helper.sound_buttons(sound_text)
                     sound.sound_volume = 0.5
               elif mouse_x >= 12.25 and mouse_x <=12.4 and mouse_y >= 7.75 and mouse_y <= 8.325:
                     # if user clicked high sound logo, sound volume is high
                     sound_text ="high"
                     gui_helper.clear_buttons()
                     gui_helper.options(current_dir)
                     gui_helper.sound_buttons(sound_text)
                     sound.sound_volume = 1
                     # If user cicked go back menu button, go back menu
               elif mouse_x >= 6.5 and mouse_x <= 12.5 and mouse_y >= 4 and mouse_y <= 6:
                     OPTIONS = False
                     gui_helper.clear_buttons()
                     gui_helper.main_menu()

      if not self.is_paused:
         sound.play_sound()

game = Tetris()
game.start()