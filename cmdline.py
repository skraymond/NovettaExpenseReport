import sys
sys.path.append("C:\\Program Files\\Tesseract-OCR\\")
sys.path.append("C:\\Program Files\\poppler\\poppler-0.68.0\\bin")

import NER.util.ner_configs
from NER.novetta_expense_report_processor import NERProcessor
import argparse
import os

def main(args):

    processor = NERProcessor()

    files = None
    if args.filenames is not None:
        files = args.filenames
    elif args.file_directory is not None:
        files = [ os.path.join(args.file_directory, x) for x in os.listdir(args.file_directory)]

    else:
        print("filenames, or file directory must be present.")
        sys.exit(-1)

    processor.process(files=files, keep_debug_files=args.debug_keep_files)

    if args.debug_process_only:
        for vendor in processor.processed_vendors:
            print(str(vendor))
        sys.exit(0)

    processor.write_out_expense_report(output_filename=args.report_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line utility to drive the Novetta Expense Report library')

    parser.add_argument('--filenames',
                        action='store',
                        type=str,
                        nargs='+',
                        help='Full Path for PDFs to be added to the expense report')

    parser.add_argument('--file-directory',
                        action='store',
                        type=str,
                        help='A directory full of files to process')


    parser.add_argument('--report-name',
                        action='store',
                        type=str,
                        default='{date}-{user}-expense_report.xls',
                        help='The name of the output expense report')

    parser.add_argument('--debug-keep-files',
                        action='store_true',
                        help='Keeps intermediary files for debugging purposes')

    parser.add_argument('--debug-process-only',
                        action='store_true',
                        help='Keeps intermediary files for debugging purposes')


    args = parser.parse_args()
    main(args)
