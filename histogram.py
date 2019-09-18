"""
Author: Alex Hadi
"""

import matplotlib.pyplot as plt

from alignment import Alignment
from constants import RESULTS_DIRECTORY
from typing import List


class Histogram:
    @staticmethod
    def save_histograms(alignments: List[Alignment], forward_strand: bool) -> None:
        indices = [x.index for x in alignments]
        plt.hist(indices, bins='auto')
        plt.title(
            'Forward Alignment Indices' if forward_strand else 'Reverse Complement Indices'
        )
        plt.xlabel('Input Sequence Index')
        plt.ylabel('Frequency')
        plt.savefig(
            f'{RESULTS_DIRECTORY}forward_alignment_indices.png' if forward_strand
            else f'{RESULTS_DIRECTORY}reverse_complement_alignment_indices.png'
        )
        plt.gcf().clear()

        scores = [x.score for x in alignments]
        plt.hist(scores, bins='auto')
        plt.title(
            'Forward Alignment Scores' if forward_strand else 'Reverse Complement Alignment Scores'
        )
        plt.xlabel('Alignment Score')
        plt.ylabel('Frequency')
        plt.savefig(
            f'{RESULTS_DIRECTORY}forward_alignment_scores' if forward_strand
            else f'{RESULTS_DIRECTORY}reverse_complement_alignment_scores.png'
        )
        plt.gcf().clear()
