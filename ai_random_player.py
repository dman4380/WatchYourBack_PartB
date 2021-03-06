#-------------------------------------------------------------------------------
# Name:         ai_random_player.py
# Purpose:      An AI player that purposefully plays a 'bad' game, by 'randomly'
#               placing and moving pieces. Used for testing purposes.
#
# Author:       Daniel Blain and Anjana Basani
#
# Created:      27/04/2018
#-------------------------------------------------------------------------------

import player_functions
from sys import exit
import random # need this to handle randomness

class Player:
    """Class for a 'bad' AI player which behaves randomly"""
    def __init__(self, colour):
        """
        Initialise a human player
        Exits program if input is invalid

        :param colour: the colour of the player, either 'black' or 'white'
        """
        self.colour = colour
        self.board = player_functions.board_init()
        self.placed = 0
        if colour == 'white':
            self.my_piece = 'O'
            self.op_piece = '@'
        elif colour == 'black':
            self.my_piece = '@'
            self.op_piece = 'O'
        else:
            # if colour invalid, abort program
            print("Invalid colour! Use 'white' or 'black'")
            exit()
        random.seed() # 'randomise' the seed

    def print_board(self):
        """
        Prints the current state of the board, as this player sees it
        """
        for r in range(8):
            s = ""
            for c in range(8):
                s = s + self.board[c][r] + " "
            print(s)

    def place(self):
        """
        Have the player attempt to place a piece (during placing phase)

        :return: a tuple if valid placement occurs, None otherwise
        """
        i_r = 0
        i_c = 0
        while True:
            # randomly select a place to put a piece. Loop until an
            # available space is found
            i_r = random.randrange(0,8)
            i_c = random.randrange(0,8)
            # check that the position is in the player's starting zone
            if self.colour == 'white' and i_r > 5:
                # retry
                continue
            elif self.colour == 'black' and i_r < 2:
                # retry
                continue
            # check that a spot is available
            if self.board[i_c][i_r] == '-':
                # available spot found, break loop
                break
        # place piece
        self.board[i_c][i_r] = self.my_piece
        return (i_c, i_r)

    def move(self, shrinks):
        """
        Have a player attempt a move, assuming one is possible

        :param shrinks: the number of times the board has shrunk
        :return: a tuple of tuples for a valid move, or None if input invalid
        """
        # get locations of my pieces first
        l_pieces = []
        for r in range(8):
            for c in range(8):
                # found own piece, note its location
                if self.board[c][r] == self.my_piece:
                    l_pieces.append([r,c])
        # list of directions
        directions = ["left","right","up","down"]
        while True:
            d = random.choice(directions) # pick a direction
            p = random.choice(l_pieces) # pick a piece
            # attempt to move
            m = (p[1], p[0])
            if player_functions.can_move(self.board,p[0],p[1],shrinks,d):
                # can move this piece, so do it
                m = player_functions.piece_move(self.board,p[0],p[1],d)
                break
            elif player_functions.can_jump(self.board,p[0],p[1],shrinks,d):
                # can move this piece, so do it
                m = player_functions.piece_jump(self.board,p[0],p[1],d)
                break
        # movement occured, yay
        return ((p[1], p[0]), m)


    def update(self, action):
        """
        Update this player's board based on the opponent's action

        :param action: the opponent's last move
        """
        player_functions.update(
            self.board,action, self.my_piece, self.op_piece)

    def action(self, turns):
        """
        Have the player take a turn

        :param turns: the number of turns which have passed so far
        :return: the move which occured, assuming one did
        """
        r_val = None # return value
        # know how many times board has shrunk
        shrinks = player_functions.get_shrinks(turns)
        if int(turns/2) == 64:
            # 64 turns have passed for each player
            player_functions.shrink(self.board,shrinks)
            player_functions.eliminate(self.board, self.op_piece, self.my_piece)
        elif int(turns/2) == 96:
            # 96 turns have passed for each player
            player_functions.shrink(self.board,shrinks)
            player_functions.eliminate(self.board, self.op_piece, self.my_piece)
        if self.placed < 12:
            # placing phase
            r_val = self.place()
            self.placed += 1
        else:
            # moving phase
            # check if can do anything
            m = player_functions.moves_available(
                self.board,self.my_piece,shrinks)
            if m == 0:
                r_val = None
            else:
                r_val = self.move(shrinks)
        player_functions.eliminate(self.board, self.op_piece, self.my_piece)
        n_shrinks = player_functions.get_shrinks(turns+1)
        if n_shrinks != shrinks:
            player_functions.shrink(self.board, n_shrinks)
        return r_val

