"""
Author: Alex Hadi
"""

import json

from typing import List


class Alignment:
    """
    Alignment
    Represents a single alignment.
    """

    def __init__(self, index: int, score: int, target_alignment: str, input_alignment: str):
        """
        __init__
        Creates a new Alignment object.

        :param index: The index of the input sequence.
        :param score: The score of the alignment.
        :param target_alignment: The target sequence alignment.
        :param input_alignment: The input sequence alignment.
        """

        self.index = index
        self.score = score
        self.target_alignment = target_alignment
        self.input_alignment = input_alignment

    @staticmethod
    def save_alignments(output_file_path: str, alignments: List['Alignment']) -> None:
        """
        save_alignments
        Save the passed alignments to a JSON file.

        :param output_file_path: The output JSON file path.
        :param alignments: All the alignments to save to the JSON file.
        """

        with open(output_file_path, 'w') as output_file:
            json.dump([
                # Get the dictionary representation of each alignment.
                alignment.__dict__ for alignment in alignments
            ], output_file, indent=4)
