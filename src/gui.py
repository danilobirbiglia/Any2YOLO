# GUI for Any2YOLO
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from converter import JSONToTXTConverter
from logger import log_action
import webbrowser


class Any2YOLOApp:
    def __init__(self):
        #Initialize the application

        self.root = tk.Tk()
        self.root.title("💻Any2YOLO Converter")
        self.root.geometry("800x700")  # Default windows size
        self.root.resizable(False, False) # Fized windows size

        self.root.iconbitmap("assets/any2yolo.ico") # Application icon

        # Files and labels
        self.input_files = []
        self.selected_labels = []
        self.available_labels = []
        self.file_label_map = {}

        # GUI elements
        self.global_label_frame = None  # Frame for label controls
        self.upload_button = None  # Button for uploading files
        self.convert_button = None  # Button for conversion

        # Setup styles, menu and GUI
        self._setup_styles()
        self._setup_menu()
        self._setup_gui()

    def run(self):
        self.root.mainloop()

    def _setup_styles(self):
        # Custom styles
        self.bg_color = "#F9FAFB"  # Light background
        self.header_color = "#005F9E"  # Header color
        self.button_color = "#007ACC"  # Button button
        self.hover_color = "#005F9E"  # Hover color
        self.text_color = "#333333"  # Standard text color
        self.highlight_text_color = "#FF5722" # Highlighted text color

    def _setup_menu(self):
        # Menu bar
        menu_bar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg=self.text_color, activebackground=self.hover_color)
        file_menu.add_command(label="📂 Upload JSON Files", command=self._upload_files)
        file_menu.add_separator()

        file_menu.add_command(label="🚪 Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Log Menu
        file_menu.add_separator()
        menu_bar.add_command(label="📜 View Logs", command=self._view_logs)

        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0, bg="white", fg=self.text_color, activebackground=self.hover_color)
        help_menu.add_command(label="📖 Manual", command=self._open_manual)  # Manual section
        help_menu.add_command(label="📖 About This App", command=self._about_app)  # About section
        menu_bar.add_cascade(label="Help", menu=help_menu)  # Add Help menu to menu bar

        # Attach complete menu to root window
        self.root.config(menu=menu_bar)

    def _setup_gui(self):
        # Set up main GUI layout
        self.root.geometry("600x400") # Start with a compact window size

        # Top Header
        frame_top = tk.Frame(self.root, bg=self.header_color, pady=10)
        frame_top.pack(fill=tk.X)

        logo_image = Image.open("assets/any2yolo.ico")
        logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.header_logo = ImageTk.PhotoImage(logo_image)

        #logo_label = tk.Label(frame_top, image=self.header_logo, bg=self.header_color)
        #logo_label.pack(side=tk.LEFT, padx=10)

        tk.Label(
            frame_top,
            text="Any2YOLO Converter",
            font=("Arial", 28, "bold"),
            fg="white",
            bg=self.header_color,
        ).pack(side=tk.LEFT)

        # Global Label Controls
        self.global_label_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        self.global_label_frame.pack(fill=tk.X)

        # Upload Section
        self.upload_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        self.upload_frame.pack(fill=tk.X)

        center_frame = tk.Frame(self.upload_frame, bg=self.bg_color)
        center_frame.pack(side=tk.TOP, expand=True)

        self.upload_button = self._create_button(
            center_frame, "📂 Upload JSON Files", self._upload_files, centered=True, highlight=True
        )
        self.upload_button.pack()

        # Placeholder for Delete All button
        self.delete_all_button = None

        # Middle Section
        self.frame_middle = tk.Frame(self.root, bg=self.bg_color, pady=10)
        self.frame_middle.pack(fill=tk.BOTH, expand=True)

        self.scroll_canvas = tk.Canvas(self.frame_middle, bg=self.bg_color, highlightthickness=0)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollable_frame = tk.Frame(self.scroll_canvas, bg=self.bg_color)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        )
        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scroll_canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.scrollbar = ttk.Scrollbar(self.frame_middle, orient="vertical", command=self.scroll_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.pack_forget()
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bottom Controls
        frame_bottom = tk.Frame(self.root, bg=self.bg_color, pady=10)
        frame_bottom.pack(fill=tk.X)

        self.convert_button = self._create_button(
            frame_bottom, "Convert", self._start_conversion, centered=True
        )
        self.convert_button.pack_forget()

        self._update_global_label_controls()


    def _create_button(self, parent, text, command, centered=False, smaller=False, highlight=False):
        # Button with hover effects
        bg_color = self.button_color if not highlight else "#FF5722"  # Highlight for important buttons
        hover_color = self.hover_color if not highlight else "#E64A19"

        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 9 if smaller else 10, "bold"),  # Smaller font for compact buttons
            bg=bg_color,
            fg="white",
            activebackground=hover_color,
            activeforeground="white",
            relief="flat",
            command=command,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=5,
        )
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))
        if centered:
            button.pack(pady=10, ipadx=10, ipady=5, anchor="center")  # Centered with padding
        else:
            button.pack(pady=5, padx=10, ipadx=10, ipady=5, anchor="w")  # Default alignment
        return button

    def _on_mousewheel(self, event):
        # Handle mousewheel scrolling
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _setup_header(self):
        # Application header
        frame_top = tk.Frame(self.root, bg=self.header_color, pady=10)
        frame_top.pack(fill=tk.X)

        logo_image = Image.open("assets/any2yolo.ico").resize((50, 50), Image.Resampling.LANCZOS)
        self.header_logo = ImageTk.PhotoImage(logo_image)

        tk.Label(frame_top, image=self.header_logo, bg=self.header_color).pack(side=tk.LEFT, padx=10)
        tk.Label(
            frame_top,
            text="Any2YOLO Converter",
            font=("Arial", 28, "bold"),
            fg="white",
            bg=self.header_color,
        ).pack(side=tk.LEFT)

    def _setup_middle_section(self):
        # Scrollable middle section
        self.scroll_frame = tk.Frame(self.root, bg=self.bg_color)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scroll_frame, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def _setup_footer(self):
        # Footer with convert button
        self.convert_button = tk.Button(
            self.root,
            text="Convert",
            font=("Arial", 12, "bold"),
            bg=self.highlight_text_color,
            fg="white",
            command=self._start_conversion,
        )
        self.convert_button.pack(pady=20)
        self.convert_button.pack_forget()

    def _upload_files(self):
        new_files = filedialog.askopenfilenames(title="Select JSON Files", filetypes=[("JSON Files", "*.json")])
        imported_files = []
        for file in new_files:
            if file not in self.input_files:
                self.input_files.append(file)
                imported_files.append(file)
                log_action(f"Imported file: {file}", "info")
            if imported_files:
                self.root.geometry("800x700")
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                log_action(f"Total {len(imported_files)} files successfully imported.", "info")
            else:
                log_action("No new files were imported.", "info")
        self._update_available_labels()
        self._update_global_label_controls()
        self._update_convert_button()
        self._update_delete_all_button() 
        

    def _update_gui(self):
        # Update GUI elements based on uploaded files
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if self.input_files:
            for file in self.input_files:
                file_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color, pady=5, padx=10)
                file_frame.pack(fill=tk.X, pady=5)

                # File label
                tk.Label(
                    file_frame, text=file, bg=self.bg_color, fg=self.text_color, anchor="w"
                ).pack(side=tk.LEFT, expand=True)

                # Remove file button
                tk.Button(
                    file_frame,
                    text="✕",
                    font=("Arial", 10, "bold"),
                    bg="red",
                    fg="white",
                    command=lambda f=file: self._remove_file(f),
                ).pack(side=tk.RIGHT)
            self.convert_button.pack()  # Show Convert button
            self._update_delete_all_button()
        else:
            self.convert_button.pack_forget()  # Hide Convert button
            self._update_delete_all_button()

    def _remove_file(self, file):
        # Remove an individual file
        if file in self.input_files:
            self.input_files.remove(file)
            log_action(f"Removed file: {file}", "warning")
            self._update_gui()

    def _update_delete_all_button(self):
        # Show or hide the Delete All button
        if self.input_files:
            if not self.delete_all_button:
                self.delete_all_button = tk.Button(
                    self.upload_frame,
                    text="🗑️Delete All Files",
                    font=("Arial", 9, "bold"),
                    bg="red",
                    fg="white",
                    activebackground="#CC0000",
                    activeforeground="white",
                    relief="flat",
                    command=self._clear_all_files,
                    bd=0,
                    highlightthickness=0,
                    padx=5,
                    pady=2,
                )

                # Hover effect for Delete All button
                self.delete_all_button.bind(
                    "<Enter>", lambda e: self.delete_all_button.config(bg="#CC0000", fg="white")
                )
                self.delete_all_button.bind(
                    "<Leave>", lambda e: self.delete_all_button.config(bg="red", fg="white")
                )

                # Place button to the left of the frame
                self.delete_all_button.place(x=20, y=20)
        else:
            if self.delete_all_button:
                self.delete_all_button.destroy()
                self.root.geometry("600x400")
                self.scrollbar.pack_forget()
                self.delete_all_button = None

    def _update_convert_button(self):
        # Show or hide the Convert button based on uploaded files 
        if self.input_files:
            if self.convert_button:
                self.convert_button.pack(side=tk.TOP, pady=10)  # Show the Convert button
        else:
            if self.convert_button:
                self.convert_button.pack_forget()  # Hide the Convert button

    def _update_available_labels(self):
        if self.input_files:
            converter = JSONToTXTConverter(self.input_files, self.selected_labels)
            self.available_labels, self.file_label_map = converter.extract_labels()
            self._update_file_label_mapping()
        else:
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

    def _update_global_label_controls(self):
        # Update the global label selection controls 
        for widget in self.global_label_frame.winfo_children():
            widget.destroy()

        if self.input_files:
            tk.Label(
                self.global_label_frame,
                text="Select Your Preferences:",
                font=("Arial", 12, "bold"),
                bg=self.bg_color,
                fg=self.text_color,
            ).pack(side=tk.LEFT, padx=10)

            self._create_button(
                self.global_label_frame, "🔘 Select All", self._select_all_labels, smaller=True
            ).pack(side=tk.LEFT, padx=2, pady=2)
            self._create_button(
                self.global_label_frame, "🚫 Deselect All", self._deselect_all_labels, smaller=True
            ).pack(side=tk.LEFT, padx=2, pady=2)

            if self.convert_button:
                self.convert_button.pack(side=tk.TOP, pady=10)
        else:
            tk.Label(
                self.global_label_frame,
                text="Upload JSON files to begin your journey!",
                font=("Arial", 12, "italic"),
                bg=self.bg_color,
                fg=self.text_color,
            ).pack(side=tk.LEFT, padx=10)
            if self.convert_button:
                self.convert_button.pack_forget()


    def _clear_all_files(self):
        # Clear all uploaded files
        self.input_files.clear()
        log_action("All files removed.", "warning")
        self._update_available_labels()
        self._update_global_label_controls()
        self._update_delete_all_button()
        self._update_convert_button()
        self._update_delete_all_button

    def _select_all_labels(self):
        # Select all labels globally
        self.selected_labels = self.available_labels.copy()
        log_action("All labels selected globally.", "info")
        self._update_file_label_mapping()

    def _deselect_all_labels(self):
        # Deselect all labels globally
        self.selected_labels.clear()
        log_action("All labels deselected globally.", "info")
        self._update_file_label_mapping()

    def _update_file_label_mapping(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for file, labels in self.file_label_map.items():
            file_frame = tk.Frame(self.scrollable_frame, bg=self.bg_color, pady=5, padx=10)
            file_frame.pack(fill=tk.X, pady=5)

            # File Name and X Button
            file_header = tk.Frame(file_frame, bg=self.bg_color)
            file_header.pack(fill=tk.X)
            tk.Label(
                file_header, text=f"File: {file}", font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.text_color
            ).pack(side=tk.LEFT, padx=10)

            remove_btn = tk.Button(
                file_header,
                text="✕",
                font=("Arial", 12, "bold"),
                bg="red",
                fg="white",
                activebackground="#CC0000",
                activeforeground="white",
                relief="flat",
                command=lambda f=file: self._remove_file(f),
                bd=0,
                highlightthickness=0,
                padx=5,
            )
            remove_btn.pack(side=tk.RIGHT, padx=5)

            # Labels with Checkboxes
            labels_frame = tk.Frame(file_frame, bg=self.bg_color, pady=5)
            labels_frame.pack(fill=tk.X)

            tk.Label(labels_frame, text="Labels:", font=("Arial", 12, "bold"), bg=self.bg_color, fg=self.text_color).pack(
                anchor="w", pady=2
            )

            for label in labels:
                chk_var = tk.IntVar(value=1 if label in self.selected_labels else 0)
                chk_btn = tk.Checkbutton(
                    labels_frame,
                    text=label,
                    variable=chk_var,
                    bg=self.bg_color,
                    fg=self.text_color,
                    activebackground=self.bg_color,
                    activeforeground=self.text_color,
                    command=lambda l=label, v=chk_var: self._toggle_label_selection(l, v),
                )
                chk_btn.pack(anchor="w", padx=20)

    def _toggle_label_selection(self, label, variable):
        if variable.get():
            if label not in self.selected_labels:
                self.selected_labels.append(label)
        else:
            if label in self.selected_labels:
                self.selected_labels.remove(label)
        log_action(f"{'Selected' if variable.get() else 'Deselected'} label: {label}", "info")

    def _remove_file(self, file):
        if file in self.input_files:
            self.input_files.remove(file)
            log_action(f"Removed file: {file}", "warning")
            self._update_available_labels()
            self._update_global_label_controls()
            self._update_delete_all_button()

    def _start_conversion(self):
        if not self.input_files or not self.selected_labels:
            messagebox.showerror("Error", "Please select files and labels before conversion.")
            return

        log_action(f"Starting conversion with selected labels: {', '.join(self.selected_labels)}", "info")
        try:
            converter = JSONToTXTConverter(self.input_files, self.selected_labels)
            results = converter.convert_files()
            result_message = "\n".join([f"{file}: {result}" for file, result in results.items()])
            log_action(f"Conversion results:\n{result_message}", "info")
            messagebox.showinfo("Conversion Results", result_message)

            # Clear inputs after successful conversion
            self.input_files.clear()
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            self._update_global_label_controls()
            self._update_delete_all_button()
        except Exception as e:
            error_message = f"An error occurred during conversion: {e}"
            log_action(error_message, "error")
            messagebox.showerror("Error", error_message)

    def _view_logs(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Application Logs")
        log_window.geometry("800x400")
        log_window.resizable(False, False)

        log_text = tk.Text(log_window, wrap=tk.WORD, bg="white", fg=self.text_color, font=("Courier", 10))
        log_text.insert(tk.END, open("logs/converter.log").read())
        log_text.config(state=tk.DISABLED)
        log_text.pack(fill=tk.BOTH, expand=True)

        self._create_button(log_window, "Close", log_window.destroy).pack(pady=10)

    def _about_app(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About This App")
        about_window.geometry("500x300")
        about_window.resizable(False, False)
        about_window.configure(bg=self.bg_color)
        about_window.iconbitmap("assets/any2yolo.ico")

        logo_image = Image.open("assets/any2yolo.ico")
        logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
        self.about_logo = ImageTk.PhotoImage(logo_image)
        #logo_label = tk.Label(about_window, image=self.about_logo, bg=self.bg_color)
        #logo_label.pack(pady=10)

        tk.Label(
            about_window,
            text="✨ Any2YOLO Converter ✨",
            font=("Arial", 18, "bold"),
            fg=self.highlight_text_color,
            bg=self.bg_color,
        ).pack(pady=10)

        tk.Label(
            about_window,
            text="Making YOLO detections out of your data chaos! 🐱‍💻",
            font=("Arial", 12, "italic"),
            fg=self.text_color,
            bg=self.bg_color,
        ).pack(pady=5)

        tk.Label(
            about_window,
            text="👨‍💻 Created by: Danilo Birbiglia",
            font=("Arial", 12),
            fg=self.text_color,
            bg=self.bg_color,
        ).pack(pady=5)

        linkedin_label = tk.Label(
            about_window,
            text="🔗 LinkedIn: Danilo Birbiglia",
            font=("Arial", 11, "underline"),
            fg=self.button_color,
            bg=self.bg_color,
            cursor="hand2",
        )
        linkedin_label.pack(pady=5)
        linkedin_label.bind("<Button-1>", lambda e: self._open_url("https://www.linkedin.com/in/danilo-birbiglia/"))

        email_label = tk.Label(
            about_window,
            text="📧 Email: danilobirbiglia@gmail.com",
            font=("Arial", 11, "underline"),
            fg=self.button_color,
            bg=self.bg_color,
            cursor="hand2",
        )
        email_label.pack(pady=5)
        email_label.bind("<Button-1>", lambda e: self._open_url("mailto:danilobirbiglia@gmail.com"))

    def _open_manual(self):
        """Display a manual with instructions on how to use the application."""
        manual_window = tk.Toplevel(self.root)
        manual_window.title("Manual")
        manual_window.geometry("600x400")
        manual_window.resizable(False, False)
        manual_window.configure(bg=self.bg_color)

        # Manual Header
        tk.Label(
            manual_window,
            text="📖 Manual for Any2YOLO",
            font=("Arial", 18, "bold"),
            fg=self.highlight_text_color,
            bg=self.bg_color,
        ).pack(pady=10)

        # Instructions Text
        manual_text = (
            "1. Upload Files:\n"
            "   - Go to File -> Upload JSON Files or click on the upload button\n"
            "   - Select the JSON files you want to process\n\n"
            "2. Manage Files:\n"
            "   - Review the uploaded files in the middle section\n"
            "   - Use the delete button next to a file to remove it\n"
            "   - Use 'Delete All' to clear all uploaded files\n\n"
            "3. Select Labels:\n"
            "   - Choose labels globally or per file\n"
            "   - Use 'Select All' or 'Deselect All' to manage global labels\n\n"
            "4. Convert Files:\n"
            "   - Click the 'Convert' button to process the files\n"
            "   - Results will be saved in the output folder and shown in a popup\n\n"
            "5. View Logs:\n"
            "   - Access logs through the Logs menu to see app activity\n\n"
            "6. Help and About:\n"
            "   - View this manual or details about the app under the Help menu"
        )

        # Add scrollable text for the manual
        text_widget = tk.Text(manual_window, wrap=tk.WORD, bg="white", fg=self.text_color, font=("Arial", 12))
        text_widget.insert(tk.END, manual_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Close Button
        self._create_button(manual_window, "Close", manual_window.destroy, centered=True).pack(pady=10)
    
    def _open_url(self, url):
        # Open a URL in the default web browser, why this? ....... Just linkedin and mail
        webbrowser.open_new(url)
