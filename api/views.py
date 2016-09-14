import boto
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from django.conf import settings

from storage.client import GStorageClient
from storage.signature import CloudStorageURLSignerJSONParser


class Photos(ViewSet):
    def __init__(self, *args, **kwargs):
        super(Photos, self).__init__(*args, **kwargs)
        self.signer = CloudStorageURLSignerJSONParser(
            settings.SERVICE_ACCOUNT_JSON_PATH, settings.STORAGE_URL).signer

    def list(self, request, path=''):
        client = GStorageClient()
        results = client.list_directory(settings.STORAGE_BUCKET, path)
        results = [
            self._process_item(i, settings.STORAGE_BUCKET) for i in results]
        return Response(results)

    def _get_file_props(self, item, bucket_name):
        url = self.signer.get_url('/%s/%s' % (bucket_name, item.name))
        return {'name': item.name, 'is_directory': False,
                'url': url}

    def _get_directory_props(self, item):
        return {'name': item.name[:-1], 'is_directory': True}

    def _process_item(self, item, bucket_name):
        if isinstance(item, boto.gs.key.Key):
            return self._get_file_props(item, bucket_name)
        return self._get_directory_props(item)
