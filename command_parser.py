"""
Author: Alex Hadi
"""

import click
import os

from alignment import Alignment
from constants import RESULTS_DIRECTORY
from helpers import Helpers
from histogram import Histogram
from optimal_alignment_finder import OptimalAlignmentFinder


@click.command()
@click.option('--target-sequence', '-t',
              help='The target DNA sequence as a string.',
              type=str,
              required=True)
@click.option('--input-fasta-file', '-i',
              help='Input FASTA file. This sequence will be searched for the target sequence.',
              type=click.Path(exists=True),
              required=True)
def parse_input(target_sequence: str, input_fasta_file: str) -> None:
    """
    parse_input

    :param target_sequence: The target sequence as a string.
    :param input_fasta_file: The path to a FASTA file.
    """

    if not Helpers.valid_dna_sequence(target_sequence):
        raise click.UsageError('The target sequence is not a valid DNA sequence.')

    input_sequence = Helpers.fasta_file_to_sequence(input_fasta_file)
    if not input_sequence:
        raise click.UsageError('Passed input file not in FASTA format.')

    optimal_alignment_finder = OptimalAlignmentFinder(
        target_sequence, input_sequence
    )

    # If the results directory doesn't exist, create it.
    if not os.path.exists(RESULTS_DIRECTORY):
        os.makedirs(RESULTS_DIRECTORY)

    Alignment.save_alignments(
        f'{RESULTS_DIRECTORY}forward_alignments.json',
        optimal_alignment_finder.forward_alignments
    )
    Histogram.save_histograms(
        optimal_alignment_finder.forward_alignments, True
    )

    Alignment.save_alignments(
        f'{RESULTS_DIRECTORY}reverse_complement_alignments.json',
        optimal_alignment_finder.reverse_complement_alignments
    )
    Histogram.save_histograms(
        optimal_alignment_finder.reverse_complement_alignments, False
    )
