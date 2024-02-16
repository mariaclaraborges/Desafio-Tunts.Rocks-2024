from services.sheets_service import SheetsService
from models.student import Student


def main():
    # Needs credential.json https://console.cloud.google.com/apis/credentials to be in the same folder of main.py
    service = SheetsService() 

    print(f"Getting students")
    students: [Student] = service.get_students()

    print(f"Updating students")
    service.update_students(students=students)


main()
