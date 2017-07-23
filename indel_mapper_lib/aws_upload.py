import boto3


class AwsUpload(object):
    BUCKET_NAME = "indel-mapper"

    def __init__(self, s3_access_key, s3_secret_key, file, destination_filename):
        self.s3_access_key = s3_access_key
        self.s3_secret_key = s3_secret_key
        self._try_uploading(file, destination_filename)

    def _try_uploading(self, file, destination_filename):
        try:
            self._upload(file, destination_filename)
            self._make_public(destination_filename)

            self.succeeded = True
            self.url = self._url_for(destination_filename)
        except Exception as e:
            print(e)
            self.succeeded = False
            self.url = None

    def _s3(self):
        return boto3.resource("s3",
                              aws_access_key_id=self.s3_access_key,
                              aws_secret_access_key=self.s3_secret_key)

    def _upload(self, file, filename):
        self._s3().Bucket(self.BUCKET_NAME).upload_fileobj(file, filename)

    def _make_public(self, filename):
        object_acl = self._s3().ObjectAcl(self.BUCKET_NAME, filename)
        object_acl.put(ACL="public-read")

    def _url_for(self, filename):
        return "https://{}.s3.amazonaws.com/{}".format(self.BUCKET_NAME, filename)
