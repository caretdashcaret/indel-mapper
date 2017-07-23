import datetime
from indel_mapper_lib.aws_upload import AwsUpload


class CsvUpload(object):
    def __init__(self, s3_access_key, s3_secret_key, file):
        upload = AwsUpload(s3_access_key, s3_secret_key, file, self._csv_filename())
        self.succeeded = upload.succeeded
        self.url = upload.url

    def _csv_filename(self):
        now = datetime.datetime.now()
        return now.strftime("results-%Y-%m-%d-%H-%M-%S-%f.csv")


class NullCsvUpload(object):
    def __init__(self):
        self.succeeded = False
        self.url = None
