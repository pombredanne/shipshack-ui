import boto


def storage_uri(path):
    return boto.storage_uri(path, 'gs')


class GStorageClient(object):
    def list_buckets(self):
        uri = storage_uri('')
        return uri.get_all_buckets()

    def get_bucket(self, bucket):
        uri = storage_uri(bucket)
        return uri.get_bucket()

    def list_directory(self, bucket_name, directory=''):
        if directory and not directory.endswith('/'):
            directory += '/'
        bucket = self.get_bucket(bucket_name)
        return bucket.list(directory, '/')
