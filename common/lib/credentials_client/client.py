"""Client to communicate with credentials service from lms"""
import json
import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from edx_rest_api_client.client import OAuthAPIClient
from provider.oauth2.models import Client
from rest_framework import status


logger = logging.getLogger(__name__)

VERSION = 'v2'


class CredentialsClient(OAuthAPIClient):

    def __init__(self):
        client = get_object_or_404(Client, name='credentials')
        super(CredentialsClient, self).__init__(settings.LMS_ROOT_URL, client.client_id, client.client_secret)
        self._api_url = '{credentials_url}/api/{version}'.format(credentials_url=client.url, version=VERSION)

    def _get(self, path):
        self.response = self.request('GET', '{api_url}{path}'.format(api_url=self._api_url, path=path))
        return self._handle_response()

    def _handle_response(self):
        status_code = self.response.status_code
        if status_code == status.HTTP_200_OK:
            return json.loads(self.response.text)
        else:
            logger.error(self.response.text)
            logger.error(self.response.status_code)
             #PermissionDenied if status_code == status.HTTP_403_FORBIDDEN else Http404

    def certs(self):
        return self._get('/credentials/?username=edx')
