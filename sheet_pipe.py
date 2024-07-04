import google.auth
from googleapiclient.discovery import build
from google.oauth2 import service_account

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
        # Your logic to extract information from the LLM response
        return {"key": "value"}  # Replace with actual extraction logic
    
    def store_in_google_sheets(self, data):
        sheet_id = "your_google_sheet_id"
        range_name = "Sheet1!A1"
        body = {
            "values": [list(data.values())]
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result
