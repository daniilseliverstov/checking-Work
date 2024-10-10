import tkinter as tk
import sqlite3
from tkinter import ttk


class ResultsWindow:
    def __init__(self, root, db_path):
        self.root = root
        self.root.title("Результаты")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.tree = tk.ttk.Treeview(self.root, columns=("ID", "Timestamp", "Start Time", "Elapsed Time", "Total Checked", "Success Rate"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Timestamp", text="Дата и время")
        self.tree.heading("Start Time", text="Начало работы")
        self.tree.heading("Elapsed Time", text="Затраченное время")
        self.tree.heading("Total Checked", text="Проверено всего")
        self.tree.heading("Success Rate", text="Успеваемость (%)")
        self.tree.pack(fill="both", expand=True)

        self.fetch_results()

    def fetch_results(self):
        self.cursor.execute("SELECT * FROM results ORDER BY timestamp DESC")
        results = self.cursor.fetchall()

        for result in results:
            self.tree.insert("", "end", values=result)


if __name__ == "__main__":
    root = tk.Tk()
    app = ResultsWindow(root, "results.db")
    root.mainloop()