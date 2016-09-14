#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2013 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import base64
import datetime
import md5
import time
import urllib
import json

import Crypto.Hash.SHA256 as SHA256
import Crypto.PublicKey.RSA as RSA
import Crypto.Signature.PKCS1_v1_5 as PKCS1_v1_5
import requests

# The Google Cloud Storage API endpoint. You should not need to change this.

GCS_API_ENDPOINT = 'https://storage.googleapis.com'


class CloudStorageURLSigner(object):

    """Contains methods for generating signed URLs for Google Cloud Storage."""

    def __init__(self, key, client_id_email, gcs_api_endpoint,
                 expiration=None, session=None):
        """
        Creates a CloudStorageURLSigner that can be used to access signed URLs.

    Args:
      key: A PyCrypto private key or a string.
      client_id_email: GCS service account email.
      gcs_api_endpoint: Base URL for GCS API.
      expiration: An instance of datetime.datetime containing the time when the
               supplied, a new session is created.
                  signed URL should expire.
    """

        if isinstance(key, basestring):
            key = RSA.importKey(key)
        self.key = key
        self.client_id_email = client_id_email
        self.gcs_api_endpoint = gcs_api_endpoint

        self.expiration = expiration or datetime.datetime.now() \
            + datetime.timedelta(days=1)
        self.expiration = int(time.mktime(self.expiration.timetuple()))
        self.session = session or requests.Session()

    def _base64sign(self, plaintext):
        """Signs and returns a base64-encoded SHA256 digest."""

        shahash = SHA256.new(plaintext)
        signer = PKCS1_v1_5.new(self.key)
        signature_bytes = signer.sign(shahash)
        return base64.b64encode(signature_bytes)

    def _make_signature_string(self, verb, path, content_md5, content_type):
        """Creates the signature string for signing according to GCS docs."""

        signature_string = \
            '''{verb}
{content_md5}
{content_type}
{expiration}
{resource}'''

        return signature_string.format(
            verb=verb, content_md5=content_md5, content_type=content_type,
            expiration=self.expiration, resource=path)

    def _make_url(self, verb, path, content_type='', content_md5=''):
        """Forms and returns the full signed URL to access GCS."""

        base_url = '%s%s' % (self.gcs_api_endpoint, path)
        signature_string = self._make_signature_string(
            verb, path, content_md5, content_type)
        signature_signed = self._base64sign(signature_string)
        query_params = {'GoogleAccessId': self.client_id_email,
                        'Expires': str(self.expiration),
                        'Signature': signature_signed}
        return (base_url, query_params)

    def get_url(self, path):
        """Get signed url"""
        base_url, query_params = self._make_url('GET', path)
        query = urllib.urlencode(query_params, doseq=True)
        return '?'.join([base_url, query])

    def get(self, path):
        """Performs a GET request.

    Args:
      path: The relative API path to access, e.g. '/bucket/object'.

    Returns:
      An instance of requests.Response containing the HTTP response.
    """

        (base_url, query_params) = self._make_url('GET', path)
        return self.session.get(base_url, params=query_params)

    def put(self, path, content_type, data):
        """Performs a PUT request.

    Args:
      path: The relative API path to access, e.g. '/bucket/object'.
      content_type: The content type to assign to the upload.
      data: The file data to upload to the new file.

    Returns:
      An instance of requests.Response containing the HTTP response.
    """

        md5_digest = base64.b64encode(md5.new(data).digest())
        (base_url, query_params) = self._make_url(
            'PUT', path, content_type, md5_digest)
        headers = {}
        headers['Content-Type'] = content_type
        headers['Content-Length'] = str(len(data))
        headers['Content-MD5'] = md5_digest
        return self.session.put(base_url, params=query_params,
                                headers=headers, data=data)

    def delete(self, path):
        """Performs a DELETE request.

    Args:
      path: The relative API path to access, e.g. '/bucket/object'.

    Returns:
      An instance of requests.Response containing the HTTP response.
    """

        (base_url, query_params) = self._make_url('DELETE', path)
        return self.session.delete(base_url, params=query_params)


class CloudStorageURLSignerJSONParser(object):
    def __init__(self, path, storage):
        with open(os.path.expanduser(path)) as f:
            data = json.load(f)
        private_key = data['private_key']
        client_email = data['client_email']
        self.signer = CloudStorageURLSigner(private_key, client_email, storage)
