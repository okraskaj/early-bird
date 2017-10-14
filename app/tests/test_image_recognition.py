import unittest
from datetime import datetime
from ImageClassifier import ImageClassifier


class TestImageTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image_classifier = ImageClassifier('krzysztof-krawczyk.jpg')

    def test_get_exif(self):
        target_exif = {'ExifTool Version Number': '9.74', 'File Name': 'krzysztof-krawczyk.jpg', 'Directory': '.',
                       'File Size': '34 kB', 'File Modification Date/Time': '2017:10:14 04:37:13+02:00',
                       'File Access Date/Time': '2017:10:14 04:37:25+02:00',
                       'File Inode Change Date/Time': '2017:10:14 04:37:19+02:00', 'File Permissions': 'rw-r--r--',
                       'File Type': 'JPEG', 'MIME Type': 'image/jpeg', 'JFIF Version': '1.01',
                       'Resolution Unit': 'None', 'X Resolution': '1', 'Y Resolution': '1', 'Image Width': '643',
                       'Image Height': '482', 'Encoding Process': 'Baseline DCT, Huffman coding',
                       'Bits Per Sample': '8', 'Color Components': '3', 'Y Cb Cr Sub Sampling': 'YCbCr4:2:0 (2 2)',
                       'Image Size': '643x482'}
        self.assertDictEqual(self.image_classifier._get_exif_data(), target_exif)

    def test_validate(self):
        self.assertEqual(0, self.image_classifier.validate(datetime.now()))
