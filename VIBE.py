#Rudy Colindres
#CIS261
#WK10 VIBE Coding

"""Student Grade Calculator.

Student records are represented with the Student class (Option B).
"""

from dataclasses import dataclass


FILE_NAME = "student_grades.txt"


@dataclass
class Student:
	"""Store a student's scores and calculated results."""

	name: str
	student_id: str
	test1: float
	test2: float
	test3: float

	@property
	def average(self):
		return (self.test1 + self.test2 + self.test3) / 3

	@property
	def grade(self):
		if self.average >= 90:
			return "A"
		if self.average >= 80:
			return "B"
		if self.average >= 70:
			return "C"
		if self.average >= 60:
			return "D"
		return "F"

	def to_file_line(self):
		return (
			f"{self.name}|{self.student_id}|{self.test1:.2f}|"
			f"{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}\n"
		)


def save_students(students):
	"""Save all records in the required pipe-delimited format."""
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line())
		print(f"Saved {len(students)} student record(s).")
	except OSError as error:
		print(f"Unable to save records: {error}")


def load_students():
	"""Load records from disk, skipping malformed lines with a message."""
	students = []
	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				parts = line.rstrip("\n").split("|")
				if len(parts) != 7:
					print(f"Skipped malformed record on line {line_number}.")
					continue
				try:
					students.append(
						Student(
							parts[0],
							parts[1],
							float(parts[2]),
							float(parts[3]),
							float(parts[4]),
						)
					)
				except ValueError:
					print(f"Skipped invalid scores on line {line_number}.")
		print(f"Loaded {len(students)} student record(s).")
	except FileNotFoundError:
		print("No existing grade file found. Starting with an empty class.")
	except OSError as error:
		print(f"Unable to load records: {error}")
	return students


def get_score(test_number):
	while True:
		try:
			score = float(input(f"Test {test_number} score (0-100): "))
			if 0 <= score <= 100:
				return score
			print("Enter a score from 0 to 100.")
		except ValueError:
			print("Enter a valid number.")


def add_student(students):
	print("\nAdd Student")
	name = input("Student name: ").strip()
	student_id = input("Student ID: ").strip()
	if not name or not student_id:
		print("Name and student ID are required.")
		return
	student = Student(
		name,
		student_id,
		get_score(1),
		get_score(2),
		get_score(3),
	)
	students.append(student)
	print(f"Added {student.name}. Average: {student.average:.2f}, Grade: {student.grade}")


def display_students(students):
	if not students:
		print("No student records to display.")
		return
	print("\nStudent Records")
	print("Name                 ID          Test 1   Test 2   Test 3   Average  Grade")
	print("-" * 78)
	for student in students:
		print(
			f"{student.name[:20]:20} {student.student_id[:10]:10} "
			f"{student.test1:7.2f}  {student.test2:7.2f}  {student.test3:7.2f}  "
			f"{student.average:7.2f}  {student.grade:>5}"
		)


def display_statistics(students):
	if not students:
		print("No student records for statistics.")
		return
	averages = [student.average for student in students]
	print("\nClass Statistics")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average:  {min(averages):.2f}")
	print(f"Class average:   {sum(averages) / len(averages):.2f}")


def search_student(students):
	search_name = input("Search name: ").strip().lower()
	matches = [student for student in students if search_name in student.name.lower()]
	if not matches:
		print("No matching student found.")
		return
	display_students(matches)


def main():
	students = load_students()
	while True:
		print("\nStudent Grade Calculator")
		print("1. Add student")
		print("2. Display all students")
		print("3. Display class statistics")
		print("4. Search by name")
		print("Press ESC to save and exit")
		choice = input("Select an option: ")

		if choice in ("\x1b", "ESC", "esc"):
			save_students(students)
			print("Goodbye!")
			break
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			display_statistics(students)
		elif choice == "4":
			search_student(students)
		else:
			print("Please choose 1, 2, 3, 4, or press ESC.")


if __name__ == "__main__":
	main()

