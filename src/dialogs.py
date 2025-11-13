import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from tkinter import filedialog

from src.gui_utils import DoubleScrolledFrame
from src.graphics import Graphics


class ImportDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 allow_folders: bool,
                 path_to_templates: str,
                 g: Graphics,
                 import_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Abgaben importieren")
        self.resizable(True, True)
        self.focus_set()
        self.g = g
        self.allow_folders = allow_folders

        # Read templates
        self.templates = [os.path.splitext(t)[0] for t in os.listdir(path_to_templates)]

        # STATES
        self.import_folder = tk.StringVar(value="")
        self.template_title = tk.StringVar(value="")
        self.team_ids = tk.StringVar(value="")
        self.manual_ids = tk.BooleanVar(value=False)
        self.import_func = import_func

        # WIDGETS
        self.config(bg=self.g.bg_color)

        # Input label
        self.input_label = tk.Label(self,
                                    text="Ordner auswählen:" if allow_folders else "Zip-Archiv auswählen:",
                                    bg=self.g.bg_color)
        self.input_label.pack(padx=10,
                              pady=5,
                              anchor="w")

        # Folder entry field
        self.entry_frame = tk.Frame(self,
                                    bg=self.g.bg_color)
        self.input_entry = tk.Entry(self.entry_frame,
                                    width=50,
                                    textvariable=self.import_folder)
        self.input_entry.pack(anchor="w",
                              side="left",
                              fill="x",
                              expand=True)

        # Search button
        self.search_button = tk.Button(self.entry_frame,
                                       text="Durchsuchen",
                                       bg=self.g.button_color,
                                       command=self.search_folder)
        self.search_button.pack(padx=10,
                                side="right",
                                anchor="e")
        self.entry_frame.pack(padx=10,
                              pady=5,
                              anchor="w",
                              fill="x",
                              expand=True)

        # Template label
        self.template_label = tk.Label(self,
                                       text="Template auswählen:",
                                       bg=self.g.bg_color)
        self.template_label.pack(padx=10,
                                 pady=5,
                                 anchor="w")

        # Template choose box
        self.template_box = ttk.Combobox(self,
                                         state="readonly",
                                         values=self.templates,
                                         textvariable=self.template_title)
        self.template_box.pack(padx=10,
                               pady=5,
                               anchor="w")

        # Team-ID label
        self.id_label = tk.Checkbutton(self, text="Manuelle Eingabe der Team-IDs:", variable=self.manual_ids,
                                       command=self.toggle_id_mode,
                                       bg=self.g.bg_color,
                                       fg="gray")

        # self.id_label = tk.Label(self,
        #                          text="Team-IDs eingeben:",
        #                          bg=self.g.bg_color)
        self.id_label.pack(padx=10,
                           pady=5,
                           anchor="w")

        # Team-ID box
        self.id_box = tk.Text(self,
                              width=20,
                              height=10,
                              state="disabled",
                              bg=self.g.bg_color)
        self.id_box.pack(padx=10,
                         pady=5,
                         anchor="w")

        # Termination frame
        self.terminate_frame = tk.Frame(self,
                                        bg=self.g.bg_color)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame,
                                      text="Abbrechen",
                                      bg=self.g.button_color,
                                      command=self.abort)
        self.abort_button.pack(padx=10,
                               pady=5,
                               anchor="e",
                               side="right")

        # Import button
        self.import_button = tk.Button(self.terminate_frame,
                                       text="Importieren",
                                       bg=self.g.button_color,
                                       command=self.import_data)
        self.import_button.pack(padx=10,
                                pady=5,
                                anchor="e",
                                side="right")

        self.terminate_frame.pack(padx=10,
                                  pady=5,
                                  anchor="w",
                                  fill="x")

    def toggle_id_mode(self):
        if self.manual_ids.get():
            self.id_label.config(fg="black")
            self.id_box.config(state="normal")
            self.id_box.config(bg="white")
        else:
            self.id_label.config(fg="gray")
            self.id_box.config(state="disabled")
            self.id_box.config(bg=self.g.bg_color)

    def search_folder(self):
        if self.allow_folders:
            self.import_folder.set(filedialog.askdirectory(parent=self))
        else:
            self.import_folder.set(filedialog.askopenfilename(parent=self, filetypes=[("ZIP Files", "*.zip")]))

    def import_data(self):
        if self.manual_ids.get():
            # Set text widget to variable
            self.team_ids.set(self.id_box.get("1.0", "end"))
            res = [self.import_folder.get(),
                   self.template_title.get(),
                   [i for i in self.team_ids.get().splitlines() if i != ""]]
        else:
            res = [self.import_folder.get(),
                   self.template_title.get()]
        self.destroy()
        self.import_func(res)

    def abort(self):
        # Set all entries to empty
        self.import_folder.set("")
        self.template_title.set("")
        self.team_ids.set("")

        self.destroy()


class SettingsDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 input_list: list[str],
                 g: Graphics,
                 save_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Kommentar-Einstellungen")
        self.resizable(True, True)
        self.minsize(500, 300)
        self.geometry("600x700")
        self.focus_set()
        self.g = g

        # STATES
        self.compile_error = input_list[0]
        self.plagiat = input_list[1]
        self.name = input_list[2]
        self.id_key = input_list[3]
        self.save_func = save_func

        # WIDGETS
        self.config(bg=self.g.bg_color)

        # Scrollable frame
        self.scroll = DoubleScrolledFrame(self)
        self.scroll.set_color(self.g.bg_color)
        self.scroll.pack(fill="both", expand=True)

        # ID Key comment
        self.id_key_label = tk.Label(self.scroll,
                                     text="Key für automatische Team-IDs:",
                                     anchor="w",
                                     bg=self.g.bg_color,
                                     font=(self.g.header_font, 14))
        self.id_key_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # String box
        self.id_key_entry = tk.Entry(self.scroll, width=50)
        self.id_key_entry.insert(0, self.id_key)
        self.id_key_entry.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        self.id_key_info_label = tk.Label(self.scroll,
                                          text="INFO:\nDieser Key wird für die automatische Zuordnung der Team-IDs "
                                               "benötigt.",
                                          anchor="w",
                                          justify="left",
                                          bg=self.g.bg_color)
        self.id_key_info_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # Compile Error comment
        self.compile_error_label = tk.Label(self.scroll,
                                            text="Compile-Error Kommentar:",
                                            anchor="w",
                                            bg=self.g.bg_color,
                                            font=(self.g.header_font, 14))
        self.compile_error_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # String box
        self.ce_box = tk.Text(self.scroll, width=50, height=5)
        self.ce_box.insert(tk.END, self.compile_error)
        self.ce_box.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        self.compile_error_info_label = tk.Label(self.scroll,
                                                 text="INFO:\nDieser Kommentar wird bei jedem Compile-Error eingefügt.",
                                                 anchor="w",
                                                 justify="left",
                                                 bg=self.g.bg_color)
        self.compile_error_info_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # Plagiat comment
        self.plag_label = tk.Label(self.scroll,
                                   text="Plagiat Kommentar:",
                                   anchor="w",
                                   bg=self.g.bg_color,
                                   font=(self.g.header_font, 14))
        self.plag_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # String box
        self.p_box = tk.Text(self.scroll, width=50, height=5)
        self.p_box.insert(tk.END, self.plagiat)
        self.p_box.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        self.plag_info_label = tk.Label(self.scroll,
                                        text="INFO:\nDieser Kommentar wird bei jedem Plagiat eingefügt.",
                                        anchor="w",
                                        justify="left",
                                        bg=self.g.bg_color)
        self.plag_info_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # Input label
        self.input_label = tk.Label(self.scroll,
                                    text="Persönlicher Kommentar:",
                                    anchor="w",
                                    bg=self.g.bg_color,
                                    font=(self.g.header_font, 14))
        self.input_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # String box
        self.id_box = tk.Text(self.scroll, width=50, height=5)
        self.id_box.insert(tk.END, self.name)
        self.id_box.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        self.info_label = tk.Label(self.scroll,
                                   text="INFO:\nDieser Kommentar wird unter jedem Comment angefügt.",
                                   anchor="w",
                                   justify="left",
                                   bg=self.g.bg_color)
        self.info_label.pack(fill="x", side="top", anchor="w", padx=10, pady=5)
        # Termination frame
        self.terminate_frame = tk.Frame(self.scroll, bg=self.g.bg_color)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame,
                                      text="Abbrechen",
                                      command=self.abort,
                                      bg=self.g.button_color)
        self.abort_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Import button
        self.import_button = tk.Button(self.terminate_frame,
                                       text="Speichern",
                                       command=self.accept,
                                       bg=self.g.button_color)
        self.import_button.pack(padx=10, pady=5, anchor="e", side="right")

        self.terminate_frame.pack(padx=10, pady=5, anchor="w", fill="x")

    def accept(self):
        compile_error = self.ce_box.get("1.0", "end")
        plagiat = self.p_box.get("1.0", "end")
        comment = self.id_box.get("1.0", "end")
        id_key = self.id_key_entry.get()
        res = [compile_error, plagiat, comment, id_key]
        self.destroy()
        self.save_func(res)

    def abort(self):
        self.destroy()


class GraphicsDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 g: Graphics,
                 save_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Grafik-Einstellungen")
        self.resizable(True, True)
        self.focus_set()
        self.g = g

        # STATES
        self.save_func = save_func
        # Fonts
        self.header_font = tk.StringVar(value=self.g.header_font)
        self.test_result_font = tk.StringVar(value=self.g.test_result_font)
        self.points_font = tk.StringVar(value=self.g.points_font)
        # Sizes
        self.header_size = self.g.header_size
        self.test_result_size = self.g.test_result_size
        self.team_title_size = self.g.team_title_size
        self.button_font_size = self.g.button_font_size
        self.total_points_size = self.g.total_points_size
        self.class_font_size = self.g.class_font_size
        self.task_font_size = self.g.task_font_size
        # Colors
        self.header_color = tk.StringVar(value=self.g.header_color)
        self.bg_color = tk.StringVar(value=self.g.bg_color)
        self.button_color = tk.StringVar(value=self.g.button_color)

        # WIDGETS
        self.config(bg=self.g.bg_color)
        self.scroll = DoubleScrolledFrame(self)
        self.scroll.set_color(self.g.bg_color)
        self.scroll.pack(fill="both", expand=True)

        # Background ---------------------------------------------------------------------------------------------------
        header_title = tk.Label(self.scroll,
                                text="Hintergrund",
                                anchor="w",
                                bg=self.g.bg_color,
                                font=(self.g.header_font, 14))
        header_title.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        bg_frame = tk.Frame(self.scroll, bg=self.g.bg_color)
        bg_color_label = tk.Label(bg_frame, text="Hintergrundfarbe:", bg=self.g.bg_color)
        bg_color_label.pack(side="left", padx=5)
        self.bg_color_entry = tk.Entry(bg_frame,
                                       width=20,
                                       textvariable=self.bg_color)
        self.bg_color_entry.pack(side="right", padx=5)
        bg_frame.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # Buttons ------------------------------------------------------------------------------------------------------
        button_title = tk.Label(self.scroll,
                                text="Buttons",
                                anchor="w",
                                bg=self.g.bg_color,
                                font=(self.g.header_font, 14))
        button_title.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        button_s_frame = tk.Frame(self.scroll, bg=self.g.bg_color)
        button_size_label = tk.Label(button_s_frame, text="Schriftgröße:", bg=self.g.bg_color)
        button_size_label.pack(side="left", padx=5)
        self.button_size_entry = ttk.Spinbox(button_s_frame,
                                             from_=8,
                                             to=26,
                                             increment=1,
                                             width=20)
        self.button_size_entry.set(self.button_font_size)
        self.button_size_entry.pack(side="right", padx=5)
        button_s_frame.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        button_c_frame = tk.Frame(self.scroll, bg=self.g.bg_color)
        button_color_label = tk.Label(button_c_frame, text="Grundfarbe:", bg=self.g.bg_color)
        button_color_label.pack(side="left", padx=5)
        self.button_color_entry = tk.Entry(button_c_frame,
                                           width=20,
                                           textvariable=self.button_color)
        self.button_color_entry.pack(side="right", padx=5)
        button_c_frame.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # Header config ------------------------------------------------------------------------------------------------
        header_title = tk.Label(self.scroll,
                                text="Überschriften",
                                anchor="w",
                                bg=self.g.bg_color,
                                font=(self.g.header_font, 14))
        header_title.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        header_frame1 = tk.Frame(self.scroll, bg=self.g.bg_color)
        header_font_label = tk.Label(header_frame1, text="Schriftart:", bg=self.g.bg_color)
        header_font_label.pack(side="left", padx=5)
        self.header_font_entry = tk.Entry(header_frame1,
                                          width=20,
                                          textvariable=self.header_font)
        self.header_font_entry.pack(side="right", padx=5)
        header_frame1.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        header_frame2 = tk.Frame(self.scroll, bg=self.g.bg_color)
        header_size_label = tk.Label(header_frame2, text="Schriftgröße:", bg=self.g.bg_color)
        header_size_label.pack(side="left", padx=5)
        self.header_size_entry = ttk.Spinbox(header_frame2,
                                             from_=8,
                                             to=26,
                                             increment=1,
                                             width=20)
        self.header_size_entry.set(self.header_size)
        self.header_size_entry.pack(side="right", padx=5)
        header_frame2.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        header_frame3 = tk.Frame(self.scroll, bg=self.g.bg_color)
        header_color_label = tk.Label(header_frame3, text="Grundfarbe:", bg=self.g.bg_color)
        header_color_label.pack(side="left", padx=5)
        self.header_color_entry = tk.Entry(header_frame3,
                                           width=20,
                                           textvariable=self.header_color)
        self.header_color_entry.pack(side="right", padx=5)
        header_frame3.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # Feedback config ----------------------------------------------------------------------------------------------
        feedback_title = tk.Label(self.scroll,
                                  text="Test Feedback",
                                  anchor="w",
                                  bg=self.g.bg_color,
                                  font=(self.g.header_font, 14))
        feedback_title.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        feedback_frame1 = tk.Frame(self.scroll, bg=self.g.bg_color)
        feedback_font_label = tk.Label(feedback_frame1, text="Schriftart:", bg=self.g.bg_color)
        feedback_font_label.pack(side="left", padx=5)
        self.feedback_font_entry = tk.Entry(feedback_frame1,
                                            width=20,
                                            textvariable=self.test_result_font)
        self.feedback_font_entry.pack(side="right", padx=5)
        feedback_frame1.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        feedback_frame2 = tk.Frame(self.scroll, bg=self.g.bg_color)
        feedback_size_label = tk.Label(feedback_frame2, text="Schriftgröße:", bg=self.g.bg_color)
        feedback_size_label.pack(side="left", padx=5)
        self.feedback_size_entry = ttk.Spinbox(feedback_frame2,
                                               from_=8,
                                               to=26,
                                               increment=1,
                                               width=20)
        self.feedback_size_entry.set(self.test_result_size)
        self.feedback_size_entry.pack(side="right", padx=5)
        feedback_frame2.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # Points -------------------------------------------------------------------------------------------------------
        points_title = tk.Label(self.scroll,
                                text="Punkte",
                                anchor="w",
                                bg=self.g.bg_color,
                                font=(self.g.header_font, 14))
        points_title.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        points_frame1 = tk.Frame(self.scroll, bg=self.g.bg_color)
        points_font_label = tk.Label(points_frame1, text="Schriftart:", bg=self.g.bg_color)
        points_font_label.pack(side="left", padx=5)
        self.points_font_entry = tk.Entry(points_frame1,
                                          width=20,
                                          textvariable=self.points_font)
        self.points_font_entry.pack(side="right", padx=5)
        points_frame1.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        points_frame2 = tk.Frame(self.scroll, bg=self.g.bg_color)
        id_size_label = tk.Label(points_frame2, text="Schriftgröße ID:", bg=self.g.bg_color)
        id_size_label.pack(side="left", padx=5)
        self.id_size_entry = ttk.Spinbox(points_frame2,
                                         from_=8,
                                         to=26,
                                         increment=1,
                                         width=20)
        self.id_size_entry.set(self.team_title_size)
        self.id_size_entry.pack(side="right", padx=5)
        points_frame2.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        points_frame3 = tk.Frame(self.scroll, bg=self.g.bg_color)
        total_size_label = tk.Label(points_frame3, text="Schriftgröße Gesamtpunkte:", bg=self.g.bg_color)
        total_size_label.pack(side="left", padx=5)
        self.total_size_entry = ttk.Spinbox(points_frame3,
                                            from_=8,
                                            to=26,
                                            increment=1,
                                            width=20)
        self.total_size_entry.set(self.total_points_size)
        self.total_size_entry.pack(side="right", padx=5)
        points_frame3.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        points_frame4 = tk.Frame(self.scroll, bg=self.g.bg_color)
        class_size_label = tk.Label(points_frame4, text="Schriftgröße Klassen:", bg=self.g.bg_color)
        class_size_label.pack(side="left", padx=5)
        self.class_size_entry = ttk.Spinbox(points_frame4,
                                            from_=8,
                                            to=26,
                                            increment=1,
                                            width=20)
        self.class_size_entry.set(self.class_font_size)
        self.class_size_entry.pack(side="right", padx=5)
        points_frame4.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        points_frame5 = tk.Frame(self.scroll, bg=self.g.bg_color)
        task_size_label = tk.Label(points_frame5, text="Schriftgröße Tasks:", bg=self.g.bg_color)
        task_size_label.pack(side="left", padx=5)
        self.task_size_entry = ttk.Spinbox(points_frame5,
                                           from_=8,
                                           to=26,
                                           increment=1,
                                           width=20)
        self.task_size_entry.set(self.task_font_size)
        self.task_size_entry.pack(side="right", padx=5)
        points_frame5.pack(fill="x", side="top", anchor="w", padx=10, pady=5)

        # Termination frame --------------------------------------------------------------------------------------------
        self.terminate_frame = tk.Frame(self, bg=self.g.bg_color)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame,
                                      text="Abbrechen",
                                      command=self.abort,
                                      bg=self.g.button_color)
        self.abort_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Import button
        self.import_button = tk.Button(self.terminate_frame,
                                       text="Speichern",
                                       command=self.accept,
                                       bg=self.g.button_color)
        self.import_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Font button
        self.font_button = tk.Button(self.terminate_frame,
                                     text="Alle Schriftarten",
                                     command=self.open_fonts,
                                     bg=self.g.button_color)
        self.font_button.pack(padx=10, pady=5, anchor="w", side="left")

        self.terminate_frame.pack(padx=10, pady=5, anchor="w", fill="x")

        for i in [self.button_size_entry,
                  self.header_size_entry,
                  self.feedback_size_entry,
                  self.id_size_entry,
                  self.total_size_entry,
                  self.class_size_entry,
                  self.task_size_entry]:
            i.bind("<MouseWheel>", self.disable_spinbox_scroll)

    def disable_spinbox_scroll(self, event):
        # Prevent the spinbox from scrolling with the mouse wheel
        self.scroll._on_mousewheel(event)  # Pass the event to the scroll frame and perform scroll
        return "break"  # Prevent tkinter from further event handling

    def open_fonts(self):
        d = FontsDialog(master=self, g=self.g)

    def accept(self):
        # Get all results in three lists
        fonts = [self.header_font.get(),
                 self.test_result_font.get(),
                 self.points_font.get()]
        sizes = [self.header_size_entry.get(),
                 self.feedback_size_entry.get(),
                 self.id_size_entry.get(),
                 self.button_size_entry.get(),
                 self.total_size_entry.get(),
                 self.class_size_entry.get(),
                 self.task_size_entry.get()]
        colors = [self.header_color.get(),
                  self.bg_color.get(),
                  self.button_color.get()]
        self.destroy()
        self.save_func(fonts, sizes, colors)

    def abort(self):
        self.destroy()


class FontsDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 g: Graphics):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Schriftarten")
        self.resizable(True, True)
        self.focus_set()
        self.config(bg=g.bg_color)

        self.text = tk.Text(self,
                            height=30,
                            width=40,
                            wrap="none",
                            borderwidth=0,
                            bg=g.bg_color)
        self.text.insert("1.0", "\n".join(sorted(g.get_available_fonts())))
        self.text.config(state="disabled")
        self.text.pack(padx=10, pady=10)


class ExportDialog(tk.Toplevel):
    def __init__(self,
                 master,
                 g: Graphics,
                 export_func):
        super().__init__(master=master)
        self.title("AuD-GUI :D - Korrektur exportieren")
        self.resizable(True, True)
        self.focus_set()

        # STATES
        self.export_folder = tk.StringVar(value="")
        self.export_func = export_func

        # WIDGETS
        self.config(bg=g.bg_color)

        # Input label
        self.input_label = tk.Label(self, text="Exportieren als:", bg=g.bg_color)
        self.input_label.pack(padx=10, pady=5, anchor="w", side="top")

        # Folder entry field
        self.input_entry = tk.Entry(self, width=50, textvariable=self.export_folder)
        self.input_entry.pack(anchor="w", side="top", fill="x", expand=True, padx=10)

        # Info label
        self.info_label = tk.Label(self,
                                   text="INFO:\nUm die Korrektur in StudOn hochladen zu können, "
                                        "benötigt der Ordner innerhalb der ZIP einen speziellen Namen.\nDieser kann auf StudOn "
                                        "heruntergeladen werden und hier eingefügt werden.",
                                   justify="left",
                                   anchor="w",
                                   bg=g.bg_color)
        self.info_label.pack(padx=10, pady=5, anchor="w")

        # Termination frame
        self.terminate_frame = tk.Frame(self, bg=g.bg_color)

        # Abort button
        self.abort_button = tk.Button(self.terminate_frame, text="Abbrechen", bg=g.button_color,
                                      command=self.abort)
        self.abort_button.pack(padx=10, pady=5, anchor="e", side="right")

        # Import button
        self.export_button = tk.Button(self.terminate_frame, text="Exportieren", bg=g.button_color,
                                       command=self.export_data)
        self.export_button.pack(padx=10, pady=5, anchor="e", side="right")

        self.terminate_frame.pack(padx=10, pady=5, anchor="w", fill="x")

    def export_data(self):
        self.destroy()
        self.export_func(self.export_folder.get())

    def abort(self):
        self.destroy()
