from __future__ import unicode_literals

from lms.lib.nodebb_client.categories import PhiluCategory
from pynodebb import Client
from pynodebb.api.groups import Group
from pynodebb.api.posts import Post
from pynodebb.api.topics import Topic
from pynodebb.api.users import User
from pynodebb.http_client import HttpClient


class NodeBBClient(Client):
    def __init__(self, admin_uid=None):
        """Instantiates the NodeBB API Client.
        Args:
            admin_uid (Optional[str]): When using a master token, requests require
                some form of context (which user made a request) and that context is
                based on a `_uid` field. Defaults to `HttpClient.DEFAULT_ADMIN_UID`.
        """
        username = 'philu'
        password = 'wI86B42hfJR0,4H'
        # api_endpoint = 'http://{}:{}@community.philanthropyu.org'.format(username, password)
        api_endpoint = 'http://172.16.11.7'

        master_token = '59c0f9c9-a087-4487-9a4e-470e3d065cad'

        self.configure(api_endpoint=api_endpoint, master_token=master_token, admin_uid=admin_uid)
        self.http_client = HttpClient()

        self.users = User(self.http_client)
        self.topics = Topic(self.http_client)
        self.posts = Post(self.http_client)
        self.groups = Group(self.http_client)
        self.categories = PhiluCategory(self.http_client)
