"""
Author: Alex Hadi
"""

from alignment import Alignment
from constants import MATCH, MISMATCH, GAP
from helpers import Helpers
from typing import List, Optional, Tuple


class SmithWaterman:
    """
    SmithWaterman
    Class for the implementation of the Smith Waterman algorithm,
    a dynamic programming algorithm for local alignment.
    """

    def __init__(self, target_sequence: str, input_sequence: str):
        """
        __init__
        Creates a new SmithWaterman object.

        :param target_sequence: The target sequence as a string.
        :param input_sequence: The input sequence as a string.
        """

        self.target_sequence = target_sequence
        self.input_sequence = input_sequence

        # Set the score threshold to 3/4 of the max possible score (a perfect match).
        self.score_threshold = int(0.75 * MATCH * len(input_sequence))

        # Divide the input sequence into substrings that are 1.5x the length of the target sequence,
        # since a string any longer will have too many gaps to be an optimal match
        self.input_sequence_substring_length = int(3 / 2 * len(target_sequence))

    def optimal_local_alignment(self, input_sequence_index: int) -> Optional[Alignment]:
        """
        optimal_local_alignment
        Determine the score of the optimal local alignment of two strings.
        Smith Waterman algorithm is used (dynamic programming algorithm for local alignment).

        :param input_sequence_index: Input sequence index.
        :return: The maximum alignments, based on the highest score.
        """

        # Get the substring of the input sequence to check.
        input_sequence = self.input_sequence[
            input_sequence_index:input_sequence_index+self.input_sequence_substring_length
        ]

        # Initialize list of optimal alignments.
        optimal_alignments = []

        # Set table size
        num_rows = len(input_sequence) + 1
        num_columns = len(self.target_sequence) + 1

        # Create scores and directions tables.
        # For directions, use "D", "L", "T", and "F" for diagonal, left, top, and restart alignment.
        scores = Helpers.create_table(num_rows, num_columns, 0)
        directions = Helpers.create_table(num_rows, num_columns, '')

        scores[0][0] = 0
        directions[0][0] = "F"
        # Set first column and first row to 0 and 'F' for score and direction respectively.
        for row in range(1, num_rows):
            scores[row][0] = 0
            directions[row][0] = "F"
        for column in range(1, num_columns):
            scores[0][column] = 0
            directions[0][column] = "F"

        for row in range(1, num_rows):
            for column in range(1, num_columns):
                # Determine if it is a match or mismatch.
                if input_sequence[row - 1] == self.target_sequence[column - 1]:
                    diagonal_cost = MATCH
                else:
                    diagonal_cost = MISMATCH

                # Dictionary mapping score cost to the corresponding direction.
                alignment_options = {
                    0: 'F',
                    scores[row][column-1] + GAP: 'L',
                    scores[row-1][column] + GAP: 'T',
                    scores[row-1][column-1] + diagonal_cost: 'D'
                }

                # Find the score and direction.
                score = max(alignment_options)
                direction = alignment_options[score]

                # Set the score and direction in the corresponding table.
                scores[row][column] = score
                directions[row][column] = direction

                # if the local alignment score is above the threshold, then save to a file
                if score >= self.score_threshold:
                    target_alignment, input_alignment = self._align(
                        directions, input_sequence, row, column
                    )
                    optimal_alignments.append(Alignment(
                        input_sequence_index, score, target_alignment, input_alignment
                    ))

        # If no alignments reaching the score threshold were found, returns None implicitly.
        if optimal_alignments:
            # Return the highest-scoring alignment.
            return max(optimal_alignments, key=lambda x: x.score)

    def _align(self, directions: List[List[str]], input_sequence: str,
               row_number: int, column_number: int) -> Tuple[str, str]:
        """
        _align
        Helper method to reconstruct the optimal alignments and return them as a tuple.

        :param directions: The 2D directions table
        :param row_number: The row number to start at.
        :param column_number: The column number to start at.
        :return: Tuple of two strings: (target_alignment, input_alignment)
        """

        # Initialize alignments.
        target_alignment = ''
        input_alignment = ''

        # Initialize the direction.
        current_direction = directions[row_number][column_number]
        while current_direction != "F":
            # Add gap to target alignment and letter to input alignment.
            if current_direction == "T":
                target_alignment += "-"
                input_alignment += input_sequence[row_number - 1]
                row_number -= 1
            # Add letter to target alignment and gap to input alignment.
            elif current_direction == "L":
                target_alignment += self.target_sequence[column_number - 1]
                input_alignment += "-"
                column_number -= 1
            # Add letter to both target alignment and input alignment.
            elif current_direction == "D":
                target_alignment += self.target_sequence[column_number - 1]
                input_alignment += input_sequence[row_number - 1]
                column_number -= 1
                row_number -= 1
            # Update the current direction to evaluate.
            current_direction = directions[row_number][column_number]

        # Reverse strings and return them (alignments were found in reverse)
        return target_alignment[::-1], input_alignment[::-1]
