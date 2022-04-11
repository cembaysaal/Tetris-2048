from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes
import numpy as np
import lib.stddraw as stddraw
from sound import *
class GUI_helper:
    # A function that create main_menu
    def main_menu(self):
        # START BUTTON
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        stddraw.setPenColor(Color(167, 255, 255))
        stddraw.filledCircle(7.5, 8, 1)
        stddraw.filledCircle(11.5, 8, 1)
        stddraw.filledRectangle(7.5, 7, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.55, 8, "START")
        # OPTIONS
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        stddraw.setPenColor(Color(167, 255, 255))
        stddraw.filledCircle(7.5, 5, 1)
        stddraw.filledCircle(11.5, 5, 1)
        stddraw.filledRectangle(7.5, 4, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.55, 5, "OPTIONS")

    def speed_choose(self):
        # Clear Other Buttons
        self.clear_buttons()

        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        # SLOW START
        stddraw.setPenColor(Color(0, 204, 0))
        stddraw.filledRectangle(1, 7, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(3, 8, "Slow")
        # NORMAL START
        stddraw.setPenColor(Color(0, 255, 255))
        stddraw.filledRectangle(7.5, 7, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.5, 8, "Normal")
        # FAST START
        stddraw.setPenColor(Color(255, 0, 0))
        stddraw.filledRectangle(14, 7, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(16, 8, "Fast")
        # Back to Menu
        stddraw.setPenColor(Color(167, 255, 255))
        stddraw.filledRectangle(6.5, 4, 6, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.5, 5, "Go Back Menu")
    # A function that clears buttons
    def clear_buttons(self):
        # clear buttons
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.filledRectangle(0, 0, 20, 10)
    # A function that clears everything
    def clear_everything(self):
        # clear everything
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.filledRectangle(0, 0, 20, 20)

    def options(self, current_dir):
        # Clear Other Buttons
        self.clear_buttons()
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        # stddraw.setPenColor(Color(255, 255, 255))
        # stddraw.filledRectangle(2,1,15,9)
        # stddraw.setPenColor(Color(0, 0, 0))
        # stddraw.filledRectangle(2, 7, 13, 2.5)

        # Sound logos
        sound = "Sound"
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.text(4, 8, sound)
        img_file_1 = current_dir + "/images/sound_on.png"
        image_to_display_1 = Picture(img_file_1)
        stddraw.picture(image_to_display_1, 12, 9)

        img_file_2 = current_dir + "/images/sound_med.png"
        image_to_display_2 = Picture(img_file_2)
        stddraw.picture(image_to_display_2, 10, 9)

        img_file_3 = current_dir + "/images/sound_low.png"
        image_to_display_3 = Picture(img_file_3)
        stddraw.picture(image_to_display_3, 8, 9)

        img_file_4 = current_dir + "/images/sound_off.png"
        image_to_display_4 = Picture(img_file_4)
        stddraw.picture(image_to_display_4, 6, 9.05)

        # Sound choosing points
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.filledRectangle(5.8, 8, 6.5, 0.1)
        # Sound off
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.filledRectangle(5.8, 7.75, 0.1, 0.6)
        # Sound low
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.filledRectangle(7.8, 7.75, 0.1, 0.6)
        # Sound medium
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.filledRectangle(10, 7.75, 0.1, 0.6)
        # Sound high
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.filledRectangle(12.3, 7.75, 0.1, 0.6)

        # Go back menu
        stddraw.setPenColor(Color(167, 255, 255))
        stddraw.filledRectangle(6.5, 4, 6, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.5, 5, "Go Back Menu")
    # Sound buttons
    def sound_buttons(self, sound):
        if sound == "off":
            stddraw.setPenColor(Color(0, 128, 255))
            stddraw.filledRectangle(5.8, 7.75, 0.1, 0.6)
        elif sound == "low":
            stddraw.setPenColor(Color(0, 128, 255))
            stddraw.filledRectangle(5.8, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(7.8, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(5.8, 8, 2, 0.1)
        elif sound == "med":
            stddraw.setPenColor(Color(0, 128, 255))
            stddraw.filledRectangle(5.8, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(7.8, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(10, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(5.8, 8, 4.3, 0.1)
        elif sound == "high":
            stddraw.setPenColor(Color(0, 128, 255))
            stddraw.filledRectangle(5.8, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(7.8, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(10, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(12.3, 7.75, 0.1, 0.6)
            stddraw.filledRectangle(5.8, 8, 6.5, 0.1)
    # Pause menu
    def pause_menu(self):
        self.clear_buttons()
        # Continue button
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        stddraw.setPenColor(Color(167, 255, 255))
        stddraw.filledCircle(7.5, 8, 1)
        stddraw.filledCircle(11.5, 8, 1)
        stddraw.filledRectangle(7.5, 7, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.55, 8, "Continue")
        # Go back menu button
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        stddraw.setPenColor(Color(167, 255, 255))
        stddraw.filledCircle(7.5, 5, 1)
        stddraw.filledCircle(11.5, 5, 1)
        stddraw.filledRectangle(7.5, 4, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.55, 5, "Go back menu")

    def game_over(self,score):
        # clear everything
        self.clear_everything()
        # show game over text
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(100)
        game_over_text = "GAME OVER"
        stddraw.setPenColor(Color(212, 0, 0))
        stddraw.text(9.75, 15, game_over_text)

        # show user the score
        stddraw.setFontSize(40)
        stddraw.setPenColor(Color(255, 255, 255))
        score_text =str(score)
        stddraw.text(9.5, 12, score_text)


        # show go back menu button
        stddraw.setFontFamily("cursive")
        stddraw.setFontSize(40)
        stddraw.setPenColor(Color(0, 255, 94))
        stddraw.filledCircle(7.5, 8, 1)
        stddraw.filledCircle(11.5, 8, 1)
        stddraw.filledRectangle(7.5, 7, 4, 2)
        stddraw.setPenColor(Color(0, 0, 0))
        stddraw.text(9.55, 8, "Go back menu")

