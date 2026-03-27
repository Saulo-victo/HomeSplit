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

    def register_expense(self, token, expense_value, date, description, category):
        header = {
            "Authorization": f"Bearer {token}"
        }
        payload = {"expense_value": expense_value,
                   "date": date,
                   "description": description, "category": category}
        return requests.post(f'{self.base_url}/expenses/', json=payload, headers=header)

    def get_data_sumary_month(self, token, search_month):
        header = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            'search_month': search_month,
        }
        response = requests.get(
            f'{self.base_url}/expenses/sumary/', headers=header, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def delete_expense(self, token, id_expense):
        header = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            'id_expense': id_expense
        }
        return requests.delete(f'{self.base_url}/expenses/delete/', headers=header, params=params)
