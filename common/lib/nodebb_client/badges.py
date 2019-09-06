from pynodebb.api import Resource


class ForumUser(Resource):

    def save(self, data):
        """
        save badge configuration
        """
        payload = data
        return self.client.post('/api/v2/badge-config/1', **payload)

    def delete(self, data):
        """
        delete badge configuration
        """
        payload = data
        return self.client.delete('/api/v2/badge-config/1', **payload)
