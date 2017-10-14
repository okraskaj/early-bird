import re
import subprocess
from datetime import datetime
import timestring
import logging
import face_recognition


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ImageClassifier')
ALL_GOOD = 0
WRONG_EXIF = 1
NO_FACE_IN_PHOTO = 2


class ImageClassifier:
    STATUS_CODES = {
        ALL_GOOD: "Everything was ok",
        WRONG_EXIF: "There was wrong exif in photo",
        NO_FACE_IN_PHOTO: "There was no face in photo or was not recognized"
    }

    def __init__(self, imagePath: str):
        self.imagePath = imagePath

    def validate(self, ref_time) -> int:
        """
        Validate if photo has correct
        :return: error codes accoring to error_codes dict
        """
        exif_data = self._get_exif_data()
        if not self._validate_exif(exif_data, ref_time):
            return WRONG_EXIF
        if not self._check_face_in_photo():
            return NO_FACE_IN_PHOTO
        return ALL_GOOD

    def _validate_exif(self, exif_data, ref_time) -> bool:
        """
        Check if image has exif before current time
        :return: True or False if exif was correct
        """
        date_fields = ['Create Date', 'Modify Date', 'Metadata Date']
        photo_date = None
        for date_field in date_fields:
            if date_field in exif_data:
                photo_date = timestring.Date(exif_data[date_field])
                break
        if photo_date is None:
            logger.error('This picture has no appropiate metadata tag for creation data')
            return True
        return photo_date < ref_time

    def _check_face_in_photo(self):
        image = face_recognition.load_image_file(self.imagePath)
        face_locations = face_recognition.face_locations(image)
        return face_locations is not None

    def _get_exif_data(self) -> dict:
        exif_tags = subprocess.run(['exiftool', '-h', self.imagePath], stdout=subprocess.PIPE).stdout.decode('utf-8')
        exif_data = {}
        for i in exif_tags.split('\n'):
            c = re.findall(r'<tr><td>(.*)<\/td><td>(.*)<\/td><\/tr>', i)
            if c:
                record = c[0]
                if len(record) == 2:
                    exif_data[record[0]] = record[1]
        return exif_data


if __name__ == '__main__':
    ic = ImageClassifier('/home/alcaster/Projects/wakeup/tests/krzysztof-krawczyk.jpg')
    print(ic.validate(datetime.now()))
