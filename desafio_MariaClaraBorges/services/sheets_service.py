import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from models.student import Student


class SheetsService:
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    spreadsheet_id = "1nS6jyIuizVXH912kWmYv3eN28c3uj34YnO4o2UbXW5Q"

    def get_students(self) -> [Student]:
        # Sheets information and authorization
        print(f"Creating get students request")
        range_name = "engenharia_de_software!A2:F"
        creds = None

        # Create authorization token or refresh the existing one
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            # Get sheet
            print(f"Sending get students request")
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=self.spreadsheet_id, range=range_name)
                .execute()
            )
            values = result.get("values", [])

            print(f"Getting the total number of classes")
            # Get the total number of classes
            total_classes = values[0]
            total_classes = int(total_classes[0][28:])

            # Mapper rows to Students model
            students = []

            print(f"Mapping students")
            for row in values[2:]:
                student = Student(
                    registry=int(row[0]),
                    name=row[1],
                    absences=int(row[2]),
                    grades=[
                        float(row[3]),
                        float(row[4]),
                        float(row[5])
                    ],
                    total_classes=total_classes
                )

                # Update student
                student.get_average_grade()
                student.get_status()

                students.append(student)

            return students

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def update_students(self, students: [Student]):
        # Sheets information and authorization
        print(f"Creating update students request")
        range_name = "engenharia_de_software!G4:H"
        creds = None

        # Create authorization token or refresh the existing one
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)

            values = []

            # Get the status and final grades of the students to update them
            for student in students:
                values.append([student.status, student.final_note])

            data = [
                {"range": range_name, "values": values}
            ]
            body = {"valueInputOption": "USER_ENTERED", "data": data}

            print(f"Sending update students request")
            result = (
                service.spreadsheets()
                .values()
                .batchUpdate(spreadsheetId=self.spreadsheet_id, body=body)
                .execute()
            )
            print(f"{(result.get('totalUpdatedCells'))} cells updated")

        except HttpError as error:
            print(f"An error occurred: {error}")
            return error
