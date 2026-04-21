import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found.")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.students = [row for row in reader]
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except FileNotFoundError:
            print("Error: file not found")
            return []

    def preview(self, n=5):
        print(f"First {n} rows:")
        print("-" * 30)
        for i in range(min(n, len(self.students))):
            s = self.students[i]
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")
        print("-" * 30)


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        print("Running analysis...")

        try:
            sorted_list = sorted(
                self.students,
                key=lambda x: float(x['final_exam_score']),
                reverse=True
            )
            top_10 = sorted_list[:10]
        except ValueError:
            top_10 = []

        exam_high = list(filter(lambda s: float(s['final_exam_score']) > 95, self.students))
        assign_high = list(filter(lambda s: float(s['assignment_score']) > 90, self.students))
        all_gpas = list(map(lambda s: float(s['GPA']), self.students))

        self.result = {
            "analysis": "Top 10 Students by Exam Score",
            "total_students": len(self.students),
            "exam_over_95": len(exam_high),
            "assignments_over_90": len(assign_high),
            "top_10_students": []
        }

        for i, s in enumerate(top_10, 1):
            self.result["top_10_students"].append({
                "rank": i,
                "id": s['student_id'],
                "country": s['country'],
                "major": s['major'],
                "exam_score": float(s['final_exam_score']),
                "gpa": float(s['GPA'])
            })

        return self.result

    def print_results(self):
        print("\n" + "=" * 30)
        print("TOP 10 STUDENTS BY EXAM SCORE")
        print("=" * 30)
        for s in self.result["top_10_students"]:
            print(f"{s['rank']}. {s['id']} | {s['country']} | Score: {s['exam_score']} | GPA: {s['gpa']}")

        print("\n" + "-" * 30)
        print(f"Students with exam > 95: {self.result['exam_over_95']}")
        print(f"Students with assignment > 90: {self.result['assignments_over_90']}")
        print("-" * 30)


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4)
            print(f"Results saved to {self.output_path}")
        except Exception:
            print("Error while saving JSON")


if __name__ == "__main__":
    file_path = 'global_university_students_performance_habits_10000.csv'

    fm = FileManager(file_path)
    if not fm.check_file():
        exit()

    fm.create_output_folder()

    dl = DataLoader(file_path)
    data = dl.load()

    if data:
        dl.preview(5)

        analyser = DataAnalyser(data)
        analyser.analyse()
        analyser.print_results()

        saver = ResultSaver(analyser.result, 'output/result.json')
        saver.save_json()