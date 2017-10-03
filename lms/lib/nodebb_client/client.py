from __future__ import unicode_literals

from django.conf import settings
from pynodebb import Client
from pynodebb.api.groups import Group
from pynodebb.api.posts import Post
from pynodebb.api.topics import Topic
from pynodebb.http_client import HttpClient

from lms.lib.nodebb_client.categories import PhiluCategory
from lms.lib.nodebb_client.users import PhiluUser


class NodeBBClient(Client):
    def __init__(self, admin_uid=None):
        """Instantiates the NodeBB API Client.
        Args:
            admin_uid (Optional[str]): When using a master token, requests require
                some form of context (which user made a request) and that context is
                based on a `_uid` field. Defaults to `HttpClient.DEFAULT_ADMIN_UID`.
        """
        self.configure(api_endpoint=settings.NODEBB_ENDPOINT,
                       master_token=settings.NODEBB_MASTER_TOKEN,
                       admin_uid=admin_uid)

        self.http_client = HttpClient()

        self.users = PhiluUser(self.http_client)
        self.topics = Topic(self.http_client)
        self.posts = Post(self.http_client)
        self.groups = Group(self.http_client)
        self.categories = PhiluCategory(self.http_client)
