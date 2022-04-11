import pygame.mixer_music
import pygame
import os
class MusicSound:
    def __init__(self):
        pygame.mixer.init()
        self.sound_volume=0.4

    def play_sound(self, stopped=False):
        pygame.mixer_music.load(os.path.join('original_tetris.mp3'))
        if not stopped:
            pygame.mixer_music.play(0)
            pygame.mixer_music.set_volume(self.sound_volume)
        else:
            pygame.mixer_music.pause()
    def game_over_sound(self,stopped=False):
        pygame.mixer_music.load(os.path.join('game_over.mp3'))
        if not stopped:
            pygame.mixer_music.play(0)
            pygame.mixer_music.set_volume(self.sound_volume)
        else:
            pygame.mixer_music.pause()
