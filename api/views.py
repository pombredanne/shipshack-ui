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
        results = [self._process_item(i) for i in results]
        return Response(results)

    def _get_signed_url(self, bucket, item):
        return self.signer.get_url('/%s/%s' % (bucket, item.name))

    def _get_file_props(self, item):
        url = self._get_signed_url(settings.STORAGE_BUCKET, item)
        thumb = self._get_signed_url(settings.THUMBNAIL_BUCKET, item)
        source = self._get_signed_url(settings.SOURCE_BUCKET, item)
        return {'name': item.name, 'is_directory': False,
                'url': url, 'thumbnail': thumb, 'source': source}

    def _get_directory_props(self, item):
        return {'name': item.name[:-1], 'is_directory': True}

    def _process_item(self, item):
        if isinstance(item, boto.gs.key.Key):
            return self._get_file_props(item)
        return self._get_directory_props(item)
