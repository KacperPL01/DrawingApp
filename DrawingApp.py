import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox


class SimplePaintApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DrawingApp")
        self.geometry("1000x800")

        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.start_path)
        self.canvas.bind("<B1-Motion>", self.add_point_to_path)
        self.canvas.bind("<ButtonRelease-1>", self.end_path)

        self.current_color = "black"
        self.brush_size = 5
        self.paths = []
        self.undone_paths = []
        self.path_colors = []
        self.undone_path_colors = []
        self.path_sizes = []
        self.undone_path_sizes = []

        control_panel = tk.Frame(self)
        control_panel.pack(side=tk.BOTTOM)

        select_color_button = tk.Button(control_panel, text="Wybierz Kolor", command=self.select_color, background="black" , foreground="white")
        select_color_button.pack(side=tk.LEFT)

        brush_size_label = tk.Label(control_panel, text="Rozmiar Pędzla:")
        brush_size_label.pack(side=tk.LEFT)

        brush_size_slider = tk.Scale(control_panel, from_=1, to=10, orient=tk.HORIZONTAL, length=100,
                                     command=self.set_brush_size)
        brush_size_slider.set(5)
        brush_size_slider.pack(side=tk.LEFT)

        save_button = tk.Button(control_panel, text="Zapisz Obraz", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        undo_button = tk.Button(control_panel, text="Cofnij", command=self.undo)
        undo_button.pack(side=tk.LEFT)

        redo_button = tk.Button(control_panel, text="Przywróć", command=self.redo)
        redo_button.pack(side=tk.LEFT)

        self.current_path = None
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)

        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Zapisz", command=self.save_image)
        self.file_menu.add_command(label="Cofnij", command=self.undo)
        self.file_menu.add_command(label="Przywróć", command=self.redo)
        self.menu_bar.add_cascade(label="Plik", menu=self.file_menu)
        self.config(menu=self.menu_bar)

    def start_path(self, event):
        self.current_path = [event.x, event.y]
        self.paths.append(self.current_path)
        self.path_colors.append(self.current_color)
        self.path_sizes.append(self.brush_size)

    def add_point_to_path(self, event):
        if self.current_path:
            self.current_path.extend([event.x, event.y])
            self.draw_path()

    def end_path(self):
        if self.current_path:
            if len(self.current_path) < 4:
                self.paths.pop()
                self.path_colors.pop()
                self.path_sizes.pop()
            self.current_path = None

    def draw_path(self):
        if self.current_path:
            self.canvas.delete("path")
            for i in range(len(self.paths)):
                path = self.paths[i]
                color = self.path_colors[i]
                size = size = self.path_sizes[i]
                points = [(path[j], path[j + 1]) for j in range(0, len(path), 2)]
                self.canvas.create_line(points, fill=color, width=size, smooth=True, tags="path")

    def undo(self):
        if self.paths:
            removed_path = self.paths.pop()
            removed_color = self.path_colors.pop()
            removed_size = self.path_sizes.pop()
            self.undone_paths.append(removed_path)
            self.undone_path_colors.append(removed_color)
            self.undone_path_sizes.append(removed_size)
            self.draw_path()

    def redo(self):
        if self.undone_paths:
            restored_path = self.undone_paths.pop()
            restored_color = self.undone_path_colors.pop()
            restored_size = self.undone_path_sizes.pop()
            self.paths.append(restored_path)
            self.path_colors.append(restored_color)
            self.path_sizes.append(restored_size)
            self.draw_path()

    def select_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def set_brush_size(self, size):
        self.brush_size = int(size)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            try:
                x = self.winfo_rootx() + self.canvas.winfo_x()
                y = self.winfo_rooty() + self.canvas.winfo_y()
                x1 = x + self.canvas.winfo_width()
                y1 = y + self.canvas.winfo_height()
                image = self.grab((x, y, x1, y1))
                image.save(file_path)
                messagebox.showinfo("Sukces", "Obraz został pomyślnie zapisany.")
            except Exception as e:
                messagebox.showerror("Błąd", "Nie udało się zapisać obrazu.")

if __name__ == "__main__":
    app = SimplePaintApp()
    app.mainloop()
