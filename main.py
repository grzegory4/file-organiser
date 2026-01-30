import customtkinter as ctk # Custom Tkinter for modern UI
from tkinter import filedialog, messagebox # For file dialogs and message boxes
import json # For handling JSON configuration
import shutil # For file operations
from pathlib import Path # For path manipulations

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class SettingsWindow(ctk.CTkToplevel): # Settings window for editing sorting rules
    def __init__(self, parent, config, save_callback):
        super().__init__(parent)
        self.title("Edit Rules")
        self.geometry("450x400")
        self.save_callback = save_callback
        self.attributes("-topmost", True)

        self.label = ctk.CTkLabel(self, text="Edit Sorting Rules (JSON)", font=("Roboto", 16, "bold"))
        self.label.pack(pady=10)

        self.text_area = ctk.CTkTextbox(self, width=400, height=250)
        self.text_area.pack(pady=10, padx=20)
        self.text_area.insert("1.0", json.dumps(config, indent=4))

        self.save_btn = ctk.CTkButton(self, text="Save & Close", command=self.save_and_close)
        self.save_btn.pack(pady=10)

    def save_and_close(self):
        try:
            new_config = json.loads(self.text_area.get("1.0", "end"))
            self.save_callback(new_config)
            self.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format!")

class OrganizerApp(ctk.CTk): # Main application window
    def __init__(self):
        super().__init__()

        self.title("Smart File Organizer")
        self.geometry("600x650")

        self.config_path = Path("config.json")
        self.load_settings()

        # --- UI Elements ---
        self.label = ctk.CTkLabel(self, text="File Organizer", font=("Roboto", 26, "bold"))
        self.label.pack(pady=(20, 5))

        self.label = ctk.CTkLabel(self, text="This app is designed to be used in Downloads folder or directories created by user.", font=("Roboto", 14))
        self.label.pack(pady=(0, 10))

        self.warning_label = ctk.CTkLabel(self, text="Warning: Do not organize app folders or system directories!\nThis may break installed software.", text_color="#FF5555")
        self.warning_label.pack(pady=(0, 10))

        # Selection
        self.dir_frame = ctk.CTkFrame(self)
        self.dir_frame.pack(pady=10, padx=30, fill="x")

        self.label = ctk.CTkLabel(self.dir_frame, text="Select destination to organize files in:", font=("Roboto", 14))
        self.label.pack(side="top", padx=10, pady=(15, 0), anchor="w")

        self.path_entry = ctk.CTkEntry(self.dir_frame, placeholder_text="Select folder...")
        self.path_entry.pack(side="left", padx=10, pady=15, expand=True, fill="x")
        self.path_entry.insert(0, str(Path.home() / "Downloads"))

        self.browse_btn = ctk.CTkButton(self.dir_frame, text="Browse", width=80, command=self.browse_folder)
        self.browse_btn.pack(side="right", padx=10)

        # Action Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)

        self.organize_btn = ctk.CTkButton(self.btn_frame, text="Start Organizing", command=self.confirm_and_run, 
                                         fg_color="#28a745", hover_color="#218838", font=("Roboto", 14, "bold"), height=40)
        self.organize_btn.pack(side="left", padx=10)

        self.settings_btn = ctk.CTkButton(self.btn_frame, text="Settings", command=self.open_settings, 
                                         fg_color="#6c757d", hover_color="#5a6268", height=40, width=100)
        self.settings_btn.pack(side="left", padx=10)

        # --- Report Section ---
        self.report_label = ctk.CTkLabel(self, text="Summary Report:", font=("Roboto", 14, "bold"))
        self.report_label.pack(pady=(10, 5), padx=30, anchor="w")

        self.report_frame = ctk.CTkScrollableFrame(self, width=500, height=250)
        self.report_frame.pack(pady=10, padx=30, fill="both", expand=True)

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.pack(side="bottom", pady=5)

    def load_settings(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {"sorting_rules": {"Images": ["jpg", "png"], "Docs": ["pdf", "txt"]}, "default_folder": "Others"}
            self.save_settings(self.config)

    def save_settings(self, new_config):
        self.config = new_config
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=4)
        self.status_label.configure(text="Settings updated!", text_color="#3498db")

    def open_settings(self):
        SettingsWindow(self, self.config, self.save_settings)

    def browse_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, selected)
            self.status_label.configure(text=f"Target: {selected}", text_color="gray")

    def confirm_and_run(self):
        if messagebox.askyesno("Safety Check", "Proceed with organizing?"):
            self.run_organizer()

    def run_organizer(self):
        # Clear previous report
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        target_dir = Path(self.path_entry.get())
        if not target_dir.exists():
            messagebox.showerror("Error", "Folder not found.")
            return

        rules = self.config.get('sorting_rules', {})
        default_name = self.config.get('default_folder', 'Others')
        moved_count = 0

        try:
            for file in target_dir.iterdir():
                if file.is_file() and not file.name.startswith('.') and file.name != "config.json":
                    ext = file.suffix[1:].lower()
                    target_cat = default_name
                    for cat, exts in rules.items():
                        if ext in exts:
                            target_cat = cat
                            break
                    
                    dest_folder = target_dir / target_cat
                    dest_folder.mkdir(exist_ok=True)
                    
                    shutil.move(str(file), str(dest_folder / file.name))
                    
                    # Log entry
                    log_entry = ctk.CTkLabel(self.report_frame, text=f"• {file.name}  →  {target_cat}", 
                                            font=("Roboto", 12), anchor="w")
                    log_entry.pack(fill="x", padx=5, pady=2)
                    
                    moved_count += 1
            
            self.status_label.configure(text=f"Successfully organized {moved_count} files.", text_color="#28a745")
            if moved_count == 0:
                ctk.CTkLabel(self.report_frame, text="No files were moved.").pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = OrganizerApp()
    app.mainloop()