from bogglecube import BoggleCube
from gambler import Shuffler, PredictableShuffler, SixSidedDie, PredictableDie

# The sixteen letter cubes provided with the standard game of Boggle.
CUBE_FACES = [("A", "A", "C", "I", "O", "T"),  # cube 0
              ("T", "Y", "A", "B", "I", "L"),  # cube 1
              ("J", "M", "O", "Qu", "A", "B"), # cube 2
              ("A", "C", "D", "E", "M", "P"),  # cube 3
              ("A", "C", "E", "L", "S", "R"),  # cube 4
              ("A", "D", "E", "N", "V", "Z"),  # cube 5
              ("A", "H", "M", "O", "R", "S"),  # cube 6
              ("B", "F", "I", "O", "R", "X"),  # cube 7
              ("D", "E", "N", "O", "S", "W"),  # cube 8
              ("D", "K", "N", "O", "T", "U"),  # cube 9
              ("E", "E", "F", "H", "I", "Y"),  # cube 10
              ("E", "G", "I", "N", "T", "V"),  # cube 11
              ("E", "G", "K", "L", "U", "Y"),  # cube 12
              ("E", "H", "I", "N", "P", "S"),  # cube 13
              ("E", "L", "P", "S", "T", "U"),  # cube 14
              ("G", "I", "L", "R", "U", "W")]  # cube 15

# helper function for the grid that will be called if we need to use the board
def _setup_board(cubes):
        # Slice the array into 4 parts of 4 elements
    return [cubes[i-4:i] for i in range(4,len(cubes)+1,4)]  
def _create_position_dict(board):
    position_dict={}
    for i in range(4):
        for j in range(4):
            id=board[i][j].get_id()
            position_dict[id]=(i,j)
    return position_dict 


class BoggleBoard:
    """A BoggleBoard represents a 4x4 grid of BoggleCube objects."""

    def __init__(self, lexicon):
        """Initializes a new BoggleBoard.
        
        Parameters
        ----------
        lexicon : set[str]
            The set of valid Boggle words.
        """
        # TODO: part 1b

        self._lexicon = lexicon
        self._cubes= [BoggleCube(i,CUBE_FACES[i],self) for i in range(16)]
        #this is for completed word attribute
        self._completed_words = []
        self._selected_cubes= []
        #create a 4*4 grid
        # Slice the array and get 4 of the most recent values
        self._board= _setup_board(self._cubes)
        self._positions= _create_position_dict(self._board)
        
         # Even if the board is shuffled keep track of the ids
        # Consider creating its own method
           



    def get_cube(self, row, col):
        """Returns the BoggleCube currently at the specified row and column.
        
        Parameters
        ----------
        row : int
            The desired row (should be between 0 and 3)
        col : int
            The desired column (should be between 0 and 3)
        
        Returns
        -------
        BoggleCube
            the cube currently at the specified row and column.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.get_cube(0, 0).get_letter()
        'A'
        >>> board.get_cube(3, 3).get_letter()
        'G'
        """
        # TODO: part 1b

        return self._board[row][col]

        
    def shake_cubes(self, shuffler=Shuffler(), die=SixSidedDie()):
        """Shakes the cubes.
        
        First, the cubes should be shuffled by the provided Shuffler.
        Then, each cube should be independently rolled using the provided SixSidedDie.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).get_letter()
        'U'
        >>> board.get_cube(1, 2).get_letter()
        'T'
        """
        # TODO: part 1b
    
    
        self._cubes=shuffler.shuffle(self._cubes)
        for i in range(len(self._cubes)):
          self._cubes[i].roll(die)
    
        self._board=_setup_board(self._cubes)
        self._positions= _create_position_dict(self._board)
       
    def adjacent(self, cube1, cube2):
        """Determines whether two cubes are adjacent.
        
        Two cubes are adjacent if they are vertically, horizontally, or diagonally adjacent.

        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.adjacent(board.get_cube(1, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 2), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(0, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 1), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(2, 3), board.get_cube(1, 2))
        True
        >>> board.adjacent(board.get_cube(1, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 2), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(3, 1), board.get_cube(1, 2))
        False
        >>> board.adjacent(board.get_cube(2, 0), board.get_cube(0, 1))
        False
        """
        # TODO: part 1b

        id_1= cube1.get_id()
        id_2= cube2.get_id()
        row1, col1 = self._positions[id_1][0], self._positions[id_1][1]
        row2, col2 = self._positions[id_2][0], self._positions[id_2][1]

        if row1 == row2 and abs(col1 - col2) == 1:
            return True
        if col1 == col2 and abs(row1 - row2) == 1:
            return True
        if abs(row1 - row2) == 1 and abs(col1 - col2) == 1:
            return True

        return False

    def unselect_all(self):
        """Sets the status of all cubes to 'unselected'.
        
        >>> board = BoggleBoard({'EXAMPLE', 'LEXICON'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.get_cube(0, 0).set_status("selected")
        >>> board.get_cube(2, 3).set_status("selected")
        >>> board.unselect_all()
        >>> board.get_cube(0, 0).get_status()
        'unselected'
        >>> board.get_cube(2, 3).get_status()
        'unselected'
        """        
        # TODO: part 1b
        for i in range(4):
            for j in range(4):
                self._board[i][j].set_status('unselected')

    def report_selection(self, cube_id):
        """Reports that the cube with the specified id has been selected by the player.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        >>> board = BoggleBoard({'GET', 'PUT', 'APT'})
        >>> board.shake_cubes(PredictableShuffler(), PredictableDie())
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(9)
        >>> board.get_word_so_far()
        'PUT'
        >>> board.report_selection(9)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        >>> board.report_selection(13)
        >>> board.report_selection(12)
        >>> board.report_selection(11)
        >>> board.get_word_so_far()
        'PU'
        >>> board.report_selection(12)
        >>> board.get_completed_words()
        ['PUT']
        >>> board.get_word_so_far()
        ''
        """
        # TODO: part 1c
        coordinates= self._positions[cube_id]
        row = coordinates[0]
        col= coordinates[1]
        current_cube= self._board[row][col]
        letters_so_far= self.get_word_so_far()

        if len(self._selected_cubes) == 0 or (current_cube not  in  self._selected_cubes and self.adjacent(current_cube,self._selected_cubes[-1])):
        #case one if no cubes are selected so far
            if len(self._selected_cubes) >0:
                self._selected_cubes[-1].set_status('selected')
            current_cube.set_status('most recently selected')
            self._selected_cubes.append(current_cube)

        elif self._selected_cubes[-1]== current_cube:
            #case 2 if cube selected is same as last one
            if letters_so_far in self._lexicon:
                self._completed_words.append(letters_so_far)
            self.unselect_all()
            #reset the list to cube_selected_so_far
            self._selected_cubes = []


    def get_completed_words(self):
        """Returns the list of completed words.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        """
        # TODO: part 1c
        return self._completed_words

    def get_word_so_far(self):
        """Returns the word corresponding to the letters selected so far.
        
        ** THIS METHOD IS IMPLEMENTED DURING PART 1C OF THE LAB. **

        See doctests for `report_selection` to get an example of the intended behavior.
        
        """
        # TODO: part 1c
        letters_so_far=''
        for current_cube in self._selected_cubes:
            letter=current_cube.get_letter()
            letters_so_far += letter
        return letters_so_far

    def __str__(self):
        """A string representation of the BoggleBoard."""
        row_strs = []
        for row in range(4):
            column = [str(self.get_cube(row, col)) for col in range(4)]
            row_strs.append(' '.join(column))
        return '\n'.join(row_strs)
if __name__ == "__main__":
    from doctest import testmod
    testmod()