from pynodebb.api.users import User


class PhiluUser(User):

    def join(self, group_name, user_name, uid=1, **kwargs):
        payload = {'name': group_name, 'user_name': user_name, '_uid': uid}
        return self.client.post('/api/v2/users/join', **payload)
