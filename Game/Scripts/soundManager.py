import pygame as pg
import numpy as np
import random
from singleton import Singleton


@Singleton
class SoundManager(object):
    def __init__(self):
        self.sounds = {}
        self.sounds['sword'] = pg.mixer.Sound('Sounds/swoosh-fx_C_major.wav')
        self.sounds['hit'] = pg.mixer.Sound('Sounds/minecraft_hit_soundmp3converter.mp3')
        self.sounds['new_round'] = pg.mixer.Sound('Sounds/newRound.wav')

    def play_sound_rand_pitch(self, sound_name):
        self.change_pitch(
            self.sounds[sound_name],
            random.uniform(0.5, 1.5)
        ).play()

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def change_pitch(self, sound, pitch_factor):
        """ Adjust the pitch using NumPy by changing the playback speed """
        sound_array = pg.sndarray.array(sound)
        new_length = int(len(sound_array) / pitch_factor)
        indices = np.round(np.linspace(0, len(sound_array) - 1, new_length)).astype(int)
        new_sound_array = sound_array[indices]
        return pg.sndarray.make_sound(new_sound_array)
