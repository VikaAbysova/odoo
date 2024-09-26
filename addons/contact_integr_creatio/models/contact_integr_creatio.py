import requests
from odoo import models, fields, api


class Contact(models.Model):
    _inherit = 'res.partner'
    _description = "Integration with Creatio"

    # Adding new column for writting log info from Creatio response
    creatio_response_log = fields.Text(string="Creatio Response Log")

    @api.model
    def create(self, vals_list):
        # Overrite Odoo creatio contact method
        contacts = super(Contact, self).create(vals_list)
        # Perform authorization and receive BPMCSRF
        csrf_token_session = self.authenticate_creatio()
        for contact in contacts:
            # Send contact data to Creatio with BPMCSRF
            self.send_to_creatio(contact, csrf_token_session)

        return contacts

    def authenticate_creatio(self):
        """
        Авторизуемся на Creatio и получаем токен BPMCSRF
        """
        url = "http://localhost:8076/ServiceModel/AuthService.svc/Login"  # URL авторизации на Creatio
        auth_data = {
            "UserName": "Supervisor",
            "UserPassword": "Supervisor"
        }
        headers = {'Content-Type': 'application/json'}

        # Send request to authorization
        session = requests.Session()  # Create session for saving cookies
        response = session.post(url, json=auth_data, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error during authentication: {response.text}")

        # Ищем токен BPMCSRF в куках
        csrf_token = session.cookies.get('BPMCSRF')

        if not csrf_token:
            raise Exception("BPMCSRF token not found in cookies")

        return csrf_token, session

    def send_to_creatio(self, contact, csrf_token_session):
        """
        Отправляем данные контакта на Creatio
        """
        csrf_token, session = csrf_token_session
        url = "http://localhost:8076/0/rest/DevOdooIntegration/CreateContact"  # URL сервиса в Creatio
        headers = {
            'Content-Type': 'application/json',
            'BPMCSRF': csrf_token  # Вставляем токен BPMCSRF в заголовок
        }
        data = {
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone
        }

        # Отправляем POST-запрос с данными контакта и заголовком BPMCSRF
        response = session.post(url, json=data, headers=headers)
        print("data", data)
        if response.status_code != 200:
            contact.creatio_response_log = response.text
            contact.message_post(
                body=f"Creatio error response: {response.text}"
            )
            raise Exception(f"Error in sending data to Creatio: {response.text}")
        
        # Set response in to column creatio_response_log
        contact.creatio_response_log = f"Response from Creatio: \n status code: {response.status_code} \n message: {response.text}"
        contact.message_post(
                body=f"{contact.creatio_response_log}",
                subject="Creatio integration",
                message_type='notification'
            )
        print(f"contact.creatio_response_log: {contact.creatio_response_log}")
        
        return response
