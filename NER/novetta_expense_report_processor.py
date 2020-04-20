import shutil
import NER.vendors
import NER.util.ner_configs
from NER.vendors.southwest import Southwest
from NER.vendors.enterprise import Enterprise
from NER.vendors.uber import Uber
from NER.spreadsheet.spreadsheet import SanAntonio2020SpreadSheet
import logging
import datetime
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path


class NERProcessor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vendors = []
        self.vendors.append(Southwest)
        self.vendors.append(Enterprise)
        self.vendors.append(Uber)
        self.processed_vendors = []

    def write_out_expense_report(self, output_filename="{date}-expense_report.xls"):
        """
        After files have been processed, create an expense reports from the extracted data
        :param output_filename: The name of the file to be written ('{date}' will be replaced by the current date)
        """

        spreadsheet = SanAntonio2020SpreadSheet(output_filename=output_filename.replace('{date}', datetime.datetime.now().strftime("%Y%m%d")))
        spreadsheet.set_vendors(self.processed_vendors)
        spreadsheet.create_and_open_output_file()
        spreadsheet.process_static_information()
        spreadsheet.process_date_information()
        spreadsheet.process_vendors()

    def process(self, files, keep_debug_files=False):
        """
        Loop through all files to extract text data. Then create vendor objects when available

        :param files: A list of pdf files, to be converted to JPG then OCR'd
        :param keep_debug_files: If True, won't remove temp files
        """

        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            tmp_dir = os.path.join(os.curdir, timestamp)
            os.mkdir(tmp_dir)
            self._process(files=files, tmp_dir=tmp_dir)
        except Exception as e:
            self.logger.exception("There was an error while processing files:" + str(e))
        finally:
            if not keep_debug_files:
                try:
                    shutil.rmtree(os.path.join(os.curdir, timestamp))
                except:
                    self.logger.exception("Unable to cleanup files")


    def _process(self, files, tmp_dir):

        pdfs_to_jpg = {}

        # Ste 1, convert all the pdf files to JPEGs so we can OCR pictures
        self.logger.info("Converting PDFs to JPG")
        for file_path in files:
            filename = os.path.basename(file_path)
            filename_base = filename.replace(".pdf", "")
            self.logger.info("Converting file: '%s'", filename)
            self.logger.debug("Full path: '%s'", file_path)

            try:
                if not filename.endswith(".pdf"):
                    self.logger.warning("Attempting to pdf-to-jpg a file without a pdf extension, '%s'", filename)
                pdf_pages = convert_from_path(file_path, 500)

                counter = 0
                pdfs_to_jpg[filename] = []
                for cur_page in pdf_pages:
                    jpeg_out_filename = os.path.join(tmp_dir, "%s_%d.jpeg" % (filename_base, counter))
                    pdfs_to_jpg[filename].append(jpeg_out_filename)
                    cur_page.save(jpeg_out_filename, 'JPEG')
                    counter += 1
            except Exception as e:
                self.logger.exception("Unable to process %s", filename)

        # OCR all the PDFS (in image form) and find the vendor for them
        for filename in pdfs_to_jpg:
            self.logger.info("OCRing file: %s", filename)
            ocr_text = ""
            for img_filename in pdfs_to_jpg[filename]:
                self.logger.debug("Processing Image: %s", img_filename)
                img = Image.open(img_filename)
                ocr_text += pytesseract.image_to_string(img)

            # Loop through known vendors, process the OCR text if we find a matching one
            matched = False
            for vendor in self.vendors:
                if vendor.matches_vendor(ocr_text):
                    matched = True
                    self.logger.debug("Vendor (%s) found for %s", vendor.get_vendor_name(), filename)
                    v = vendor(ocr_text)
                    if v.parsed_correctly():
                        self.processed_vendors.append(v)

            # When developing new vendors, this allows us to see what text is printed via OCR
            if not matched:
                self.logger.debug("%s did not find a vendor match with the following OCR text:", filename)
                self.logger.debug(repr(ocr_text))
