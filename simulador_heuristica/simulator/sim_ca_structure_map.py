# -*- coding:utf-8 -*-
from pathlib import Path
from .constants import Constants

class StructureMap(object):
    """Responsable to store the map fisical informations: doors, walls, etc.

    ...

    Attributes
    ----------
    label : str
        The name of the static map.
        
    map : list of list of int
        The map with values of static fields.

    len_row : int
        The horizontal size of the map.

    len_col : int
        The vertical size of the map.

    path : str
        Directory path which contains the map file.

    Methods
    -------
    load_map()
        Read the map file to construct the structure map.

    get_empty_positions()
        Returns a list which contains the empty positions of the structure map.
    
    Authors
    -------
        Eduardo Miranda <eduardokira08@gmail.com>
        Luiz E. Pereira <luizedupereira000@gmail.com>
    """

    def __init__(self, label, path):
        self.label = label
        if path is None:
            # Caminho relativo ao diretório do simulador
            self.path = Path(__file__).parent.parent / "input" / label / "map.txt"
        else:
            self.path = Path(path)

        self.map = []
        self.len_row = 0
        self.len_col = 0
        self.exits = []

    def load_map(self):
        """Read the map file to construct the structure map.
        """
        if not self.path.exists():
            raise FileNotFoundError(f"Mapa não encontrado em {self.path}")

        with open(self.path, 'r') as file:
            for line in file:
                line = line.strip('\n')
                self.map.append([int(col) for col in line])
                self.len_row += 1

        if self.len_row > 0:
            self.len_col = len(self.map[0])
        self.exits = self.get_exits()

    def get_empty_positions(self):
        """Returns a list which contains the empty positions of the structure map.

        Returns
        -------
        list of tuple
            List that contains the empty positions of the structure map.
        """
        empty_positions = []
        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.map[i][j] == Constants.M_EMPTY):
                    empty_positions.append((i, j))
        return empty_positions

    def isSaida(self, row, col):
        """Returns if the position is an exit or not.
        
        Returns
        -------
        logical
            Return if the structure map in the position i,j is an exit
        """
        if row < 0 or row >= self.len_row or col < 0 or col >= self.len_col:
            return False
        return self.map[row][col] == Constants.M_DOOR 

    def get_exits(self):
        """Returns a list which contains the exits of the structure map.

        Returns
        -------
        list of tuple
            List that contains the exits of the structure map.
        """
        exits = []
        for i in range(self.len_row):
            for j in range(self.len_col):
                if (self.map[i][j] == Constants.M_DOOR):
                    exits.append((i, j))
        return exits

    def rewrite_doors(self, new_doors):
        for exit in self.exits:
            self.map[exit[0]][exit[1]] = Constants.M_WALL
        
        for new_door in new_doors:
            if new_door['direction'] == 'V':
                for i in range(0, new_door['size']):
                    self.map[new_door['row'] + i][new_door['col']]
            else:
                for i in range(0, new_door['size']): 
                    self.map[new_door['row']][new_door['col'] + i]            

        self.exits = self.get_exits()