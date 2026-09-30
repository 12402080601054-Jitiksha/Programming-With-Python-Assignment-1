import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os


DATA_FILE = "assignment_data.json"


class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Tracker")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)

        # Main data structure:
        # {
        #   "2201": {
        #       "name": "Asha",
        #       "submissions": [
        #           {
        #               "assignment": "Assignment 1",
        #               "status": "Completed",
        #               "marks": "18/20",
        #               "remarks": ""
        #           }
        #       ]
        #   }
        # }
        self.students = {}

        self.load_data()
        self.create_widgets()
        self.refresh_table()

    # ---------------------------------------------------------
    # FILE PERSISTENCE
    # ---------------------------------------------------------

    def load_data(self):
        """Load saved data from JSON file."""

        if not os.path.exists(DATA_FILE):
            self.students = {}
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                self.students = json.load(file)

        except (json.JSONDecodeError, OSError):
            messagebox.showwarning(
                "Warning",
                "Could not load saved data. Starting with empty data."
            )
            self.students = {}

    def save_data(self):
        """Save all student data to JSON."""

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    self.students,
                    file,
                    indent=4
                )

        except OSError as error:
            messagebox.showerror(
                "File Error",
                f"Could not save data:\n{error}"
            )

    # ---------------------------------------------------------
    # GUI
    # ---------------------------------------------------------

    def create_widgets(self):
        """Create all GUI widgets."""

        title = tk.Label(
            self.root,
            text="Student Assignment Tracker",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)

        # ---------------- STUDENT FRAME ----------------

        student_frame = tk.LabelFrame(
            self.root,
            text="Student Details",
            padx=10,
            pady=10
        )
        student_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            student_frame,
            text="Enrollment:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.enrollment_entry = tk.Entry(
            student_frame,
            width=20
        )
        self.enrollment_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            student_frame,
            text="Name:"
        ).grid(row=0, column=2, padx=5)

        self.name_entry = tk.Entry(
            student_frame,
            width=25
        )
        self.name_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        tk.Button(
            student_frame,
            text="Add Student",
            command=self.add_student
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        # ---------------- SUBMISSION FRAME ----------------

        submission_frame = tk.LabelFrame(
            self.root,
            text="Assignment Submission",
            padx=10,
            pady=10
        )
        submission_frame.pack(
            fill="x",
            padx=15,
            pady=5
        )

        tk.Label(
            submission_frame,
            text="Assignment:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.assignment_entry = tk.Entry(
            submission_frame,
            width=20
        )
        self.assignment_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            submission_frame,
            text="Marks:"
        ).grid(row=0, column=2, padx=5)

        self.marks_entry = tk.Entry(
            submission_frame,
            width=15
        )
        self.marks_entry.grid(
            row=0,
            column=3,
            padx=5
        )

        tk.Label(
            submission_frame,
            text="Status:"
        ).grid(row=0, column=4, padx=5)

        self.status_var = tk.StringVar(
            value="Completed"
        )

        self.status_combo = ttk.Combobox(
            submission_frame,
            textvariable=self.status_var,
            values=["Pending", "Completed"],
            state="readonly",
            width=15
        )
        self.status_combo.grid(
            row=0,
            column=5,
            padx=5
        )

        tk.Label(
            submission_frame,
            text="Remarks:"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.remarks_entry = tk.Entry(
            submission_frame,
            width=50
        )
        self.remarks_entry.grid(
            row=1,
            column=1,
            columnspan=3,
            padx=5
        )

        tk.Button(
            submission_frame,
            text="Add Submission",
            command=self.add_submission
        ).grid(
            row=1,
            column=4,
            padx=5
        )

        tk.Button(
            submission_frame,
            text="Update Marks",
            command=self.update_marks
        ).grid(
            row=1,
            column=5,
            padx=5
        )

        # ---------------- FILTER FRAME ----------------

        filter_frame = tk.Frame(self.root)
        filter_frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        tk.Label(
            filter_frame,
            text="Filter:"
        ).pack(side="left")

        self.filter_var = tk.StringVar(
            value="All"
        )

        self.filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=[
                "All",
                "Pending",
                "Completed"
            ],
            state="readonly",
            width=15
        )
        self.filter_combo.pack(
            side="left",
            padx=5
        )

        self.filter_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.refresh_table()
        )

        tk.Button(
            filter_frame,
            text="Export CSV",
            command=self.export_csv
        ).pack(
            side="right",
            padx=5
        )

        tk.Button(
            filter_frame,
            text="Refresh",
            command=self.refresh_table
        ).pack(
            side="right",
            padx=5
        )

        # ---------------- TABLE ----------------

        table_frame = tk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        columns = (
            "Enrollment",
            "Name",
            "Assignment",
            "Status",
            "Marks",
            "Remarks"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.table.heading(
                column,
                text=column
            )

        self.table.column(
            "Enrollment",
            width=100
        )

        self.table.column(
            "Name",
            width=150
        )

        self.table.column(
            "Assignment",
            width=150
        )

        self.table.column(
            "Status",
            width=100
        )

        self.table.column(
            "Marks",
            width=100
        )

        self.table.column(
            "Remarks",
            width=200
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.table.bind(
            "<Double-1>",
            self.load_selected_record
        )

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def validate_student(self):
        """Validate student information."""

        enrollment = self.enrollment_entry.get().strip()
        name = self.name_entry.get().strip()

        if not enrollment:
            messagebox.showerror(
                "Validation Error",
                "Enrollment number is required."
            )
            return None

        if not enrollment.isdigit():
            messagebox.showerror(
                "Validation Error",
                "Enrollment must contain only digits."
            )
            return None

        if not name:
            messagebox.showerror(
                "Validation Error",
                "Student name is required."
            )
            return None

        return enrollment, name

    def validate_submission(self):
        """Validate assignment information."""

        assignment = self.assignment_entry.get().strip()
        marks = self.marks_entry.get().strip()
        status = self.status_var.get()
        remarks = self.remarks_entry.get().strip()

        if not assignment:
            messagebox.showerror(
                "Validation Error",
                "Assignment name is required."
            )
            return None

        if not marks:
            messagebox.showerror(
                "Validation Error",
                "Marks are required."
            )
            return None

        # Accept formats such as:
        # 18/20
        # 18
        if "/" in marks:
            parts = marks.split("/")

            if len(parts) != 2:
                messagebox.showerror(
                    "Validation Error",
                    "Marks must be in format obtained/total."
                )
                return None

            try:
                obtained = float(parts[0])
                total = float(parts[1])

                if total <= 0 or obtained < 0 or obtained > total:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Validation Error",
                    "Invalid marks."
                )
                return None

        else:
            try:
                value = float(marks)

                if value < 0:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Validation Error",
                    "Marks must be numeric."
                )
                return None

        return assignment, marks, status, remarks

    # ---------------------------------------------------------
    # STUDENT OPERATIONS
    # ---------------------------------------------------------

    def add_student(self):
        """Add a new student."""

        result = self.validate_student()

        if result is None:
            return

        enrollment, name = result

        if enrollment in self.students:
            messagebox.showerror(
                "Error",
                "Student already exists."
            )
            return

        self.students[enrollment] = {
            "name": name,
            "submissions": []
        }

        self.save_data()
        self.refresh_table()

        self.enrollment_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Success",
            "Student added successfully."
        )

    # ---------------------------------------------------------
    # SUBMISSION OPERATIONS
    # ---------------------------------------------------------

    def add_submission(self):
        """Add an assignment submission to a student."""

        enrollment = self.enrollment_entry.get().strip()

        if enrollment not in self.students:
            messagebox.showerror(
                "Error",
                "Student does not exist. Add the student first."
            )
            return

        result = self.validate_submission()

        if result is None:
            return

        assignment, marks, status, remarks = result

        submission = {
            "assignment": assignment,
            "status": status,
            "marks": marks,
            "remarks": remarks
        }

        self.students[enrollment]["submissions"].append(
            submission
        )

        self.save_data()
        self.refresh_table()

        messagebox.showinfo(
            "Success",
            "Submission added successfully."
        )

    def update_marks(self):
        """Update marks of the selected submission."""

        selected = self.table.selection()

        if not selected:
            messagebox.showerror(
                "Error",
                "Select a record first."
            )
            return

        item = self.table.item(selected[0])

        values = item["values"]

        enrollment = str(values[0])
        assignment = str(values[2])

        new_marks = self.marks_entry.get().strip()

        if not new_marks:
            messagebox.showerror(
                "Validation Error",
                "Enter new marks."
            )
            return

        # Validate new marks.
        if "/" in new_marks:
            parts = new_marks.split("/")

            if len(parts) != 2:
                messagebox.showerror(
                    "Validation Error",
                    "Invalid marks format."
                )
                return

            try:
                obtained = float(parts[0])
                total = float(parts[1])

                if total <= 0 or obtained < 0 or obtained > total:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Validation Error",
                    "Invalid marks."
                )
                return

        else:
            try:
                if float(new_marks) < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Validation Error",
                    "Marks must be numeric."
                )
                return

        for submission in self.students[enrollment]["submissions"]:

            if submission["assignment"] == assignment:
                submission["marks"] = new_marks
                submission["status"] = "Completed"

                break

        self.save_data()
        self.refresh_table()

        messagebox.showinfo(
            "Success",
            "Marks updated successfully."
        )

    # ---------------------------------------------------------
    # TABLE OPERATIONS
    # ---------------------------------------------------------

    def refresh_table(self):
        """Refresh table according to selected filter."""

        for item in self.table.get_children():
            self.table.delete(item)

        selected_filter = self.filter_var.get()

        for enrollment in sorted(self.students.keys()):

            student = self.students[enrollment]

            for submission in student["submissions"]:

                if (
                    selected_filter != "All"
                    and submission["status"] != selected_filter
                ):
                    continue

                self.table.insert(
                    "",
                    tk.END,
                    values=(
                        enrollment,
                        student["name"],
                        submission["assignment"],
                        submission["status"],
                        submission["marks"],
                        submission["remarks"]
                    )
                )

    def load_selected_record(self, event=None):
        """Load selected table record into input fields."""

        selected = self.table.selection()

        if not selected:
            return

        item = self.table.item(selected[0])

        values = item["values"]

        self.enrollment_entry.delete(
            0,
            tk.END
        )
        self.enrollment_entry.insert(
            0,
            values[0]
        )

        self.name_entry.delete(
            0,
            tk.END
        )
        self.name_entry.insert(
            0,
            values[1]
        )

        self.assignment_entry.delete(
            0,
            tk.END
        )
        self.assignment_entry.insert(
            0,
            values[2]
        )

        self.status_var.set(
            values[3]
        )

        self.marks_entry.delete(
            0,
            tk.END
        )
        self.marks_entry.insert(
            0,
            values[4]
        )

        self.remarks_entry.delete(
            0,
            tk.END
        )
        self.remarks_entry.insert(
            0,
            values[5]
        )

    # ---------------------------------------------------------
    # CSV EXPORT
    # ---------------------------------------------------------

    def export_csv(self):
        """Export all assignment records to CSV."""

        if not self.students:
            messagebox.showerror(
                "Error",
                "There is no data to export."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save CSV Report",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ]
        )

        if not file_path:
            return

        try:
            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "Enrollment",
                        "Name",
                        "Assignment",
                        "Status",
                        "Marks",
                        "Remarks"
                    ]
                )

                for enrollment in sorted(self.students.keys()):

                    student = self.students[enrollment]

                    for submission in student["submissions"]:

                        writer.writerow(
                            [
                                enrollment,
                                student["name"],
                                submission["assignment"],
                                submission["status"],
                                submission["marks"],
                                submission["remarks"]
                            ]
                        )

            messagebox.showinfo(
                "Export Successful",
                f"CSV report saved to:\n{file_path}"
            )

        except OSError as error:
            messagebox.showerror(
                "File Error",
                f"Could not export CSV:\n{error}"
            )


def main():
    root = tk.Tk()

    app = AssignmentTracker(root)

    root.mainloop()


if __name__ == "__main__":
    main()