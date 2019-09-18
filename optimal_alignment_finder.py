"""
Author: Alex Hadi
"""

import os

from alignment import Alignment
from helpers import Helpers
from multiprocessing import Pool
from smith_waterman import SmithWaterman
from typing import List


class OptimalAlignmentFinder:
    def __init__(self, target_sequence: str, input_sequence: str):
        # Get all the indices for the input sequence.
        # Create an iterable to allow for multiple processes
        input_sequence_indices = [
            x for x in range(0, len(input_sequence), 5)
        ]

        smith_waterman_forward = SmithWaterman(
            target_sequence, input_sequence
        )
        self.forward_alignments = self.find_forward_alignments(
            smith_waterman_forward, input_sequence_indices
        )

        smith_waterman_reverse_complement = SmithWaterman(
            target_sequence, Helpers.reverse_complement(input_sequence)
        )
        self.reverse_complement_alignments = self.find_forward_alignments(
            smith_waterman_reverse_complement, input_sequence_indices
        )

    def find_forward_alignments(self, smith_waterman_forward: SmithWaterman,
                                input_sequence_indices: List[int]) -> List[Alignment]:
        process_pool = Pool(int(0.8*os.cpu_count()))
        forward_alignments = process_pool.map(
            smith_waterman_forward.optimal_local_alignment, input_sequence_indices
        )
        return [
            x for x in forward_alignments if x is not None
        ]

    def find_reverse_complement_alignments(self, smith_waterman_reverse_complement: SmithWaterman,
                                           input_sequence_indices: List[int]) -> List[Alignment]:
        process_pool = Pool(int(0.8*os.cpu_count()))
        reverse_complement_alignments = process_pool.map(
            smith_waterman_reverse_complement.optimal_local_alignment, input_sequence_indices
        )
        return [
            x for x in reverse_complement_alignments if x is not None
        ]
