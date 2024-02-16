import math

class Student:
    registry: int
    name: str
    absences: int
    grades: [float]
    total_classes: int
    status: str
    average_grade: float = 0.0
    final_grade: float = 0.0

    def __init__(self, registry, name, absences, grades, total_classes):
        self.registry = registry
        self.name = name
        self.absences = absences
        self.grades = grades
        self.total_classes = total_classes

    def get_average_grade(self):
        for i in range(len(self.grades)):
            self.average_grade = self.grades[i] + self.average_grade

            if i == len(self.grades) - 1:
                self.average_grade = math.ceil(self.average_grade / 3)

    def get_status(self):
        if self.absences > math.ceil(self.total_classes * 0.25):
            self.status = "Reprovado por falta"
        elif self.average_grade < 50:
            self.status = "Reprovado por Nota"
            return
        elif 50 <= self.average_grade < 70:
            self.status = "Exame Final"
            self.final_grade = math.ceil(10 - self.average_grade)
            return
        else:
            self.status = "Aprovado"
            self.final_grade = 0
