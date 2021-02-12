import json
import hashlib
from requests import request
from requests.exceptions import HTTPError
from django.conf import settings


class MailChimpException(Exception):
    pass


class Connection(object):
    """ mailchimp api connection """

    output = "json"
    version = '3.0'

    def __init__(self, apikey=None, secure=False):
        self._apikey = apikey

        proto = 'https' if secure else 'http'
        dc = apikey.split('-')[1]

        self.root = '{}://{}.api.mailchimp.com/{}/'.format(proto, dc, self.version)

    def make_request(self, method="GET", path=None, **kwargs):
        if path:
            url = '{}{}'.format(self.root, path)
        else:
            url = self.root

        queries = kwargs.get('queries')
        payload = kwargs.get('body') or {}

        if payload:
            payload = json.dumps(payload)

        response = request(
            method,
            url=url,
            params=queries,
            data=payload,
            headers={'content-type': 'application/json'},
            auth=('chimp', self._apikey),
        )

        if response.status_code == 204:
            return {'success': True}

        try:
            response.raise_for_status()
        except HTTPError, e:
            message = "Exception detail: %s, Errors: %s " % (response.json().get('detail', ''),
                                                             str(response.json().get('errors', '')))
            if response.json()['status'] == 404:
                return None
            else:
                raise MailChimpException(message)

        return response.json()

    @classmethod
    def get_connection(cls):
        connection = cls(apikey=settings.MAILCHIMP_API_KEY, secure=True)
        return connection


class ChimpClient(object):
    def __init__(self):
        self.conn = Connection.get_connection()

    def _get_email_hash(self, email):
        md = hashlib.md5()
        md.update(email.lower())
        return md.hexdigest()

    def get_list_members(self, list_id):
        path = "list/{}/members/".format(list_id)
        return self.conn.make_request(path=path)

    def add_list_members_in_batch(self, list_id, data):
        path = '/lists/{list_id}'.format(list_id=list_id)
        return self.conn.make_request(method="POST", path=path, body=data)

    def add_update_member_to_list(self, list_id, email, data):
        email_hash = self._get_email_hash(email.lower())
        path = '/lists/{list_id}/members/{subscriber_hash}'.format(list_id=list_id, subscriber_hash=email_hash)

        return self.conn.make_request(method="PUT", path=path, body=data)

    def delete_user_from_list(self, list_id, email):
        email_hash = self._get_email_hash(email.lower())
        path = '/lists/{list_id}/members/{subscriber_hash}'.format(list_id=list_id, subscriber_hash=email_hash)

        return self.conn.make_request(method="DELETE", path=path)
