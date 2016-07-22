from os.path import join
import pygame


class LevelMapHandler:

    def __init__(self):
        self.n_rows = -1
        self.n_cols = -1

    def load(self,n_level):

        #Tile s positioning data
        file_level = open(join('media','levels','level{}.txt'.format(n_level)))
        self.matrix_level = [list(linea) for linea in file_level.readlines()]
        file_level.close()

        #Tile s image
        self.tiles = pygame.image.load(join('media','sprites','tiles-level{}.bmp'.format(n_level)))