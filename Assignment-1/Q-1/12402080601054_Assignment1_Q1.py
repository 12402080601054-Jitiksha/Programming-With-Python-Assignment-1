"""
Q1 - Campus Merit Analyzer using Compound Data Structures

Python Version: 3.10 or above

Data Structures Used:
1. Lists       - store all student records and semester groups
2. Tuples      - store each student's immutable record and marks
3. Dictionaries - group students semester-wise

Time Complexity:
O(n*m + n log n)

Space Complexity:
O(n*m)
"""


def validate_student(enrollment, name, semester, cpi, marks, m):
    """
    Validate all values of a student record.
    Raises ValueError if any input is invalid.
    """

    if not enrollment:
        raise ValueError("Enrollment number cannot be empty.")

    if not name:
        raise ValueError("Student name cannot be empty.")

    if not 1 <= semester <= 8:
        raise ValueError("Semester must be between 1 and 8.")

    if not 0.0 <= cpi <= 10.0:
        raise ValueError("CPI must be between 0 and 10.")

    if len(marks) != m:
        raise ValueError("Incorrect number of subject marks.")

    for mark in marks:
        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")


def read_student(m):
    """
    Read and validate one student record.

    Returns:
        tuple: (enrollment, name, semester, cpi, marks)
    """

    parts = input().split()

    if len(parts) != 4 + m:
        raise ValueError(
            f"Each student record must contain {4 + m} values."
        )

    enrollment = parts[0]
    name = parts[1]

    try:
        semester = int(parts[2])
        cpi = float(parts[3])
        marks = tuple(int(mark) for mark in parts[4:])
    except ValueError:
        raise ValueError(
            "Semester, CPI and marks must contain valid numeric values."
        )

    validate_student(
        enrollment,
        name,
        semester,
        cpi,
        marks,
        m
    )

    # Tuple is used for the complete student record.
    return (enrollment, name, semester, cpi, marks)


def calculate_average(marks):
    """
    Calculate average marks of a student.
    """

    return sum(marks) / len(marks)


def display_top_students(semester_students, k, m):
    """
    Display top K students for every semester.

    Sorting priority:
    1. Higher CPI
    2. Higher average marks
    3. Lexicographically smaller enrollment number
    """

    for semester in sorted(semester_students):

        students = semester_students[semester]

        students.sort(
            key=lambda student: (
                -student[3],
                -calculate_average(student[4]),
                student[0]
            )
        )

        top_students = students[:k]

        enrollments = [
            student[0]
            for student in top_students
        ]

        print(
            f"Semester {semester}: "
            + " ".join(enrollments)
        )


def display_subject_toppers(students, m):
    """
    Display topper(s) for every subject.

    If multiple students have the same highest mark,
    all their enrollment numbers are displayed in
    lexicographically sorted order.
    """

    for subject_index in range(m):

        highest_mark = max(
            student[4][subject_index]
            for student in students
        )

        toppers = []

        for student in students:
            if student[4][subject_index] == highest_mark:
                toppers.append(student[0])

        # Lexicographically smaller enrollment first.
        toppers.sort()

        print(
            f"S{subject_index + 1}: "
            + " ".join(toppers)
        )


def main():
    """
    Main function of the Campus Merit Analyzer.
    """

    try:
        # Read n, k and m.
        first_line = input().split()

        if len(first_line) != 3:
            raise ValueError(
                "First line must contain n, k and m."
            )

        try:
            n, k, m = map(int, first_line)
        except ValueError:
            raise ValueError(
                "n, k and m must be integers."
            )

        # Validate constraints.
        if not 1 <= n <= 100000:
            raise ValueError(
                "n must be between 1 and 100000."
            )

        if not 1 <= k <= 50:
            raise ValueError(
                "k must be between 1 and 50."
            )

        if not 1 <= m <= 12:
            raise ValueError(
                "m must be between 1 and 12."
            )

        students = []

        # Dictionary groups students according to semester.
        semester_students = {}

        for _ in range(n):

            student = read_student(m)

            students.append(student)

            semester = student[2]

            if semester not in semester_students:
                semester_students[semester] = []

            semester_students[semester].append(student)

        # Display semester-wise top K students.
        display_top_students(
            semester_students,
            k,
            m
        )

        # Display subject-wise toppers.
        display_subject_toppers(
            students,
            m
        )

    except ValueError as error:
        print(f"Input Error: {error}")


if __name__ == "__main__":
    main()
