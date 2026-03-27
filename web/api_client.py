import requests


class HomeSplitApi:
    def __init__(self, BASE_URL):
        self.base_url = BASE_URL

    def user_login(self, user_email, password):
        payload = {"username": user_email,
                   "password": password}
        return requests.post(f'{self.base_url}/token', data=payload)

    def user_register(self, user_name, email, password):
        payload = {"name": user_name, "email": email, "password": password}
        return requests.post(f'{self.base_url}/users/', json=payload)

    def register_expense(self, token, expense_value, description, category):
        header = {
            "Authorization": f"Bearer {token}"
        }
        payload = {"expense_value": expense_value,
                   "description": description, "category": category}
        return requests.post(f'{self.base_url}/expenses/', json=payload, headers=header)
