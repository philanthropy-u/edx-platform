from pynodebb.api.users import User


class PhiluUser(User):

    def join(self, group_name, user_name, **kwargs):
        payload = {'group_name': group_name, 'user_name': user_name}
        return self.client.post('/api/v2/users/join', **payload)
