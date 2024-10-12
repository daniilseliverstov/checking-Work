import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox


class ResultsWindow:
    def __init__(self, root, db_path):
        self.root = root
        self.root.title("Результаты")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.tree = ttk.Treeview(self.root,
                                 columns=("ID", "Start Time", "Elapsed Time", "Total Checked", "Success Rate"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Start Time", text="Начало работы")
        self.tree.heading("Elapsed Time", text="Затраченное время")
        self.tree.heading("Total Checked", text="Всего проверено")
        self.tree.heading("Success Rate", text="Успеваемость (%)")
        self.tree.pack(fill="both", expand=True)

        self.tree.column("ID", width=50)
        self.tree.column("Start Time", width=150)
        self.tree.column("Elapsed Time", width=100)
        self.tree.column("Total Checked", width=120)
        self.tree.column("Success Rate", width=120)

        self.delete_button = tk.Button(self.root, text="Удалить выбранное", command=self.delete_selected)
        self.delete_button.pack(pady=10)

        self.fetch_results()

    def fetch_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM results ORDER BY start_time DESC")
        results = self.cursor.fetchall()

        for result in results:
            self.tree.insert("", "end", values=result)

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите запись для удаления.")
            return

        item_id = self.tree.item(selected_item,"values")[0]
        self.cursor.execute("DELETE FROM results WHERE id = ?", (item_id,))
        self.conn.commit()

        self.reorder_ids()
        self.fetch_results()

        messagebox.showinfo("Успех", "Запись успешно удалена.")

    def reorder_ids(self):
        self.cursor.execute("SELECT * FROM results ORDER BY start_time DESC")
        results = self.cursor.fetchall()

        for new_id, result in enumerate(results, start=1):
            old_id = result[0]
            self.cursor.execute("UPDATE results SET id = ? WHERE id = ?", (new_id, old_id))

        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ResultsWindow(root, "results.db")
    root.mainloop()
