import boto3


class PresignedPost(object):
    BUCKET_NAME = "indel-mapper"

    def __init__(self, s3_access_key, s3_secret_key, file_name, file_type):
        self.s3_access_key = s3_access_key
        self.s3_secret_key = s3_secret_key
        if file_type != "text/csv":
            file_type = "text"
        self._try_creating_presigned_post(file_name, file_type)

    def _try_creating_presigned_post(self, file_name, file_type):
        try:
            presigned_data = self._s3().meta.client.generate_presigned_post(
                Bucket = self.BUCKET_NAME,
                Key = file_name,
                Fields = {"acl": "public-read", "Content-Type": file_type},
                Conditions = [
                    {"acl": "public-read"},
                    {"Content-Type": file_type}
                ],
                ExpiresIn = 3600
            )

            self.presigned_data = presigned_data
            self.succeeded = True
            self.url = self._url_for(file_name)
        except Exception as e:
            print(e)
            self.presigned_data = {}
            self.succeeded = False
            self.url = None

    def _s3(self):
        return boto3.resource("s3",
                              aws_access_key_id=self.s3_access_key,
                              aws_secret_access_key=self.s3_secret_key)

    def _upload(self, file, filename):
        self._s3().Bucket(self.BUCKET_NAME).upload_fileobj(file, filename)

    def _url_for(self, filename):
        return "https://{}.s3.amazonaws.com/{}".format(self.BUCKET_NAME, filename)
