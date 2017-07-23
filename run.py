import argparse
import csv
import pysam
from indel_mapper_lib.sam_parser import SamParser
from indel_mapper_lib.reference_parser import ReferenceParser
from indel_mapper_lib.presenter import Presenter
from indel_mapper_lib.csv_writer import CsvWriter
from indel_mapper_lib.json_writer import JsonWriter


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-a', '--alignment', help="Alignment SAM file", required=True)
    parser.add_argument('-r', '--reference', help="Reference CSV file", required=True)
    parser.add_argument('-o', '--output', help="Output file, as CSV", required=True)
    parser.add_argument('-m', '--metadata', help="Output a separate file containing the JSON metadata", action="store_true")

    return parser.parse_args()

def main(args):
    reference_name_to_reads = SamParser(pysam.AlignmentFile(args.alignment, "rb")).reference_name_to_reads_dict()
    references = ReferenceParser(csv.reader(open(args.reference)), reference_name_to_reads).references()
    presenter_results = Presenter([reference for reference in references if reference.is_valid]).present()

    CsvWriter(presenter_results).write_to(args.output)

    if args.metadata:
        JsonWriter(presenter_results).write_to("{}.json".format(args.output))

if __name__ == '__main__':
    main(get_args())
