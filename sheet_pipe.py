import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

class GoogleSheetsPipeline:
    def __init__(self, service_account_info):
        self.service_account_info = service_account_info
        self.credentials = service_account.Credentials.from_service_account_info(self.service_account_info)
        self.service = build('sheets', 'v4', credentials=self.credentials)
    
    def process_llm_response(self, llm_response):
        # Extract the necessary information from the LLM response
        extracted_data = self.extract_information(llm_response)
        # Store the extracted data in Google Sheets
        self.store_in_google_sheets(extracted_data)
    
    def extract_information(self, llm_response):
        # Extract data using regular expressions
        date = self.extract_date(llm_response)
        name = self.extract_name(llm_response)
        overall_performance = self.extract_overall_performance(llm_response)
        admin_msg = self.extract_admin_msg(llm_response)
        employee_msg = self.extract_employee_msg(llm_response)

        return {
            "Date": date,
            "Name": name,
            "Overall Performance": overall_performance,
            "Admin Message": admin_msg,
            "Employee Message": employee_msg
        }
    
    def extract_date(self, text):
        # Extract date from the text
        match = re.search(r'Report Analysis\n\nDate:\s*([^\n]+)', text)
        if match:
            return match.group(1)
        return "Unknown"
    
    def extract_name(self, text):
        match = re.search(r'Admin Message:\s*(\w+)', text)
        if match:
            return match.group(1)
        return "Unknown"
    
    def extract_overall_performance(self, text):
        match = re.search(r'Overall Performance Percentage:\s*Calculation:\s*\(\d+%\s*\+\s*\d+%\s*\+\s*\d+%\s*\+\s*\d+%\)\s*/\s*4\s*=\s*(\d+%)', text)
        if match:
            return match.group(1)
        return "0%"
    
    def extract_admin_msg(self, text):
        match = re.search(r'Admin Message:\n([\s\S]*?)\nEmployee Message', text)
        if match:
            return match.group(1).strip()
        return ""
    
    def extract_employee_msg(self, text):
        match = re.search(r'Employee Message \(in Spanish\):\n([\s\S]*)', text)
        if match:
            return match.group(1).strip()
        return ""

    def store_in_google_sheets(self, data):
        sheet_id = "your_google_sheet_id"
        range_name = "Sheet1!A1:E1"
        body = {
            "values": [list(data.values())]
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result

def main():
    # Add your actual service account details here
    service_account_info = {
        "type": "service_account",
        "project_id": "your_project_id",
        "private_key_id": "your_private_key_id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": "your_service_account_email",
        "client_id": "your_client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your_service_account_email"
    }

    llm_response = """Report Analysis

Task Categorization:

GLT Ad Activations:

Nombre del producto 1

Nombre del producto 2

Nombre del producto 3

Nombre del producto 4

GLT Price Additions (Nulu Business):

Mesa decorativa Umbra $110

Cesta transportadora $33

Batidor Electrico es de $7

Bateria 11 piezas Mageflon $119

Olla de presion Magefesa Roja $99,99. Negra $95

Freidora de aire Oster 3.2 Litros $89

Molde para pan Kitchenaid $20

Balanza Rocia 40 kilos $29,99

Pica todo Prime Home $25

Iros Electronics Ad Activations:

Ventilador de mesa Tropicano 4 Taurus

Ventilador de pared 18" 5 aspas negro Fortunne

Olla arrocera 1.2 litros 4728 Oster

Olla de presión eléctrica 6 litros OPEFR-60G Frigilux

Olla de presión multiuso eléctrica 6 litros digital Roccia

Sartén 38 cm eléctrico cerámica Sankey

Batidora Oster Planetaria 750W 12 Vel 4 Lts C/Accesorios Acero Inox

Batidora De Pedestal GE 350 W Gris

Nombre del producto 9

Nombre del producto 10

Iros Electronics (pagina web):

Nombre del producto 1

Nombre del producto 2

Nombre del producto 3

Nombre del producto 4

Nombre del producto 5

Employee's Work Performance:

GLT Ad Activation Rate:

Daily goal: 4 activations

Actual activations: 4

Calculation: (4 / 4) * 100 = 100%

GLT Price Addition Rate (Nulu Business):

Daily goal: 4 price additions

Actual additions: 9

Calculation: (4 / 4) * 100 = 100% (Note: Extra additions performed are acknowledged but the rate is capped at 100%)

Iros Electronics Ad Activation Rate:

Daily goal: 10 activations

Actual activations: 10

Calculation: (10 / 10) * 100 = 100%

Iros Electronics (pagina web) Rate:

Daily goal: 5 updates

Actual updates: 5

Calculation: (5 / 5) * 100 = 100%

Overall Performance Percentage:

Calculation: (100% + 100% + 100% + 100%) / 4 = 100%

Missing Sections or Data Gaps:

Nota: No ads were published due to administrative issues at the store.

Report Format Check:

The report is in the correct format.

Admin Message:
Karla successfully completed all tasks with 4 GLT Ad Activations, 9 price additions under GLT (Nulu Business), 10 Iros Electronics Ad Activations, and 5 updates on Iros Electronics (pagina web). This results in an overall performance rate of 100%. Extra entries were performed for GLT Price Additions (Nulu Business) which are acknowledged. No ads were published for one category due to administrative issues noted.

Employee Message (in Spanish):
Hola Karla,

Gracias por tu esfuerzo en las activaciones de anuncios y la actualización de precios. Hemos notado que completaste 4 activaciones para GLT y 9 actualizaciones de precios para GLT, superando nuestra meta. También completaste 10 activaciones para Iros Electronics y 5 actualizaciones para Iros Electronics en la página web. Excelente trabajo al alcanzar y superar nuestras metas.

Además, observamos la nota sobre los problemas administrativos que impidieron la publicación de nuevos anuncios.

Tu porcentaje de rendimiento general es del 100%.

¡Ánimo y sigue esforzándote!

Saludos,
Nulu AI Assistant

Calculation Method:

GLT Ad Activation Rate: (4 / 4) * 100 = 100%

GLT Price Addition Rate (Nulu Business): (4 / 4) * 100 = 100%

Iros Electronics Ad Activation Rate: (10 / 10) * 100 = 100%

Iros Electronics (pagina web) Rate: (5 / 5) * 100 = 100%

Overall Performance Percentage: (100% + 100% + 100% + 100%) / 4 = 100%
"""

    pipeline = GoogleSheetsPipeline(service_account_info)
    pipeline.process_llm_response(llm_response)

if __name__ == "__main__":
    main()
