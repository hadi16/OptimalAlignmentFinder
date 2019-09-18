"""
Author: Alex Hadi
"""

from typing import Dict, List, Optional


class Helpers:
    @staticmethod
    def str_replace_all(text: str, all_replacements: Dict[str, str]) -> str:
        """
        str_replace_all
        Helper function to perform multiple string replacements.

        :param text: The text to perform the replacements on.
        :param all_replacements: All of the replacements as (original_str -> replacement_str)
        :return: The string after replacements are done.
        """

        for original_str, replacement_str in all_replacements.items():
            text = text.replace(original_str, replacement_str)
        return text

    @staticmethod
    def valid_dna_sequence(sequence: str) -> bool:
        """
        valid_dna_sequence
        Determines whether the passed sequence only uses A, T, C, or G.

        :param sequence: The sequence to check.
        :return: True if the sequence is a valid DNA sequence (otherwise False).
        """

        return set(sequence) <= set('ATCG')

    @staticmethod
    def reverse_complement(sequence: str) -> str:
        """
        reverse_complement
        Transform the passed sequence into its proper reverse complement.

        :param sequence: The sequence to perform the reverse complement on.
        :return: The reverse complement as a string.
        """

        nucleotide_complements = {
            'A': 'T',
            'C': 'G',
            'G': 'C',
            'T': 'A'
        }
        sequence = [
            nucleotide_complements[nucleotide]
            for nucleotide in list(sequence)
        ]
        sequence = ''.join(sequence)

        # reverse the whole string and return it.
        return sequence[::-1]

    @staticmethod
    def fasta_file_to_sequence(fasta_file: str) -> Optional[str]:
        """
        fasta_file_to_sequence
        Takes a FASTA file and returns the DNA sequence as a string.

        :param fasta_file: The path to a FASTA file.
        :return: The DNA sequence as a string.
        """

        with open(fasta_file, 'r') as file:
            header = file.readline()
            if not header.startswith('>'):
                print('Input file not in FASTA format!')
                return

            # read in rest of file
            sequence = file.read()

        # remove all return and newline characters
        sequence = Helpers.str_replace_all(sequence, {
            '\r': '',
            '\n': ''
        })

        # make it upper case and return it.
        return sequence.upper()

    @staticmethod
    def create_table(num_rows: int, num_columns: int, value) -> List[list]:
        """
        create_table
        Create a 2D table with the given number of rows and columns.

        :param num_rows: The number of rows.
        :param num_columns: The number of columns.
        :param value: The value to fill the table with.
        :return: The table as a list of lists.
        """

        return [
            [value] * num_columns for _ in range(num_rows)
        ]
