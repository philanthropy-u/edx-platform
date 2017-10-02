from pynodebb.api.categories import Category


class PhiluCategory(Category):
    def create(self, name, private=True, uid=None, **kwargs):
        """

        :param name:
        :param private:
        :param uid:
        :param kwargs:
        :return:
        """
        payload = {'name': name, 'private': private, 'uid': uid}
        return self.client.post('/api/v2/edx_categories', **payload)
