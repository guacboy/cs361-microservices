import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReportFileHandler(FileSystemEventHandler):
    """
    File system event handler for monitoring changes to report.txt.
    """
    
    def __init__(self, gui_app):
        self.gui_app = gui_app
        self.last_content = ""
    
    def on_modified(self, event):
        """
        Handles file modification events.
        """
        if event.src_path.endswith("report.txt"):
            self.process_report_file()
    
    def process_report_file(self):
        """
        Process the report.txt file when modifications are detected.
        
        This method:
        - reads the current content of report.txt
        - checks if the content has changed and is a valid file path
        """
        try:
            with open("report.txt", "r") as f:
                content = f.read().strip()
            
            # only process if content changed and is not empty
            if content and content != self.last_content:
                self.last_content = content
                
                # check if it's a CSV file path
                if os.path.exists(content) and content.lower().endswith('.csv'):
                    print(f"CSV file path detected: {content}")
                    # update GUI in a thread-safe way
                    self.gui_app.root.after(0, lambda: self.gui_app.process_manual_file(content))
                    
            elif not content.startswith("Dataset Summary Report"):
                print("invalid CSV file path detected")
        
        except Exception as e:
            print(f"error processing report file: {e}")

class ReportGenerator:
    """
    A GUI application for generating summary reports from CSV files.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Report Generator")
        self.root.geometry("600x500")
        
        self.csv_file_path = None
        self.report_content = ""
        self.file_monitor = None
        
        self.create_widgets()
        self.start_file_monitoring()
    
    def create_widgets(self):
        """
        Create and arrange all GUI widgets in the main window.
        
        This function sets up:
        - title label
        - file selection area with import button
        - action buttons (save)
        - text area for report display
        """
        # title label
        title_label = tk.Label(self.root,
                               text="CSV Report Generator",
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # file selection frame
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10,
                        fill="x",
                        padx=20)
        
        self.file_label = tk.Label(file_frame,
                                   text="No file selected",
                                   wraplength=400)
        self.file_label.pack(side="left",
                             fill="x",
                             expand=True)
        
        browse_btn = tk.Button(file_frame,
                               text="Import CSV",
                               command=self.import_csv)
        browse_btn.pack(side="right",
                        padx=(10, 0))
        
        # button frame for actions
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        save_btn = tk.Button(button_frame,
                             text="Save Report",
                             command=self.save_report)
        save_btn.pack(side="left",
                      padx=5)
        
        # report display area
        self.report_text = scrolledtext.ScrolledText(self.root,
                                                     height=20,
                                                     width=70)
        self.report_text.pack(pady=10,
                              padx=20,
                              fill="both",
                              expand=True)
    
    def start_file_monitoring(self):
        """
        Start monitoring report.txt for manual file path entries.
        """
        event_handler = ReportFileHandler(self)
        self.file_monitor = Observer()
        self.file_monitor.schedule(event_handler, path=".", recursive=False)
        self.file_monitor.start()
        
        # check for existing content on startup
        threading.Thread(target=self.check_existing_file, daemon=True).start()
    
    def check_existing_file(self):
        """
        Check if report.txt already contains a valid file path on startup.
        """
        time.sleep(1) # wait a bit for GUI to initialize
        try:
            if os.path.exists("report.txt"):
                with open("report.txt", "r") as f:
                    content = f.read().strip()
                
                if os.path.exists(content) and content.lower().endswith('.csv'):
                    self.root.after(0, lambda: self.process_manual_file(content))
        except:
            pass
    
    def process_manual_file(self, file_path):
        """
        Process a manually entered file path from report.txt.
        """
        self.csv_file_path = file_path
        self.file_label.config(text=file_path)
        self.generate_report()
        messagebox.showinfo("Success", "CSV file imported and report generated!")
    
    def import_csv(self):
        """
        Open a file dialog to select a CSV file and import it.
        
        This function:
        - opens a file dialog for CSV file selection
        - writes the file path to report.txt
        - automatically generates and displays the report
        """
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv")]
        )
        
        if file_path:
            self.csv_file_path = file_path
            self.file_label.config(text=file_path)
            
            # write file path to report.txt
            with open("report.txt", "w") as f:
                f.write(file_path)
            
            # automatically generate and display the report
            self.generate_report()
            
            messagebox.showinfo("Success", "CSV file imported and report generated!")
    
    def generate_report(self):
        """
        Generate a summary report from the imported CSV file.
        
        This function:
        - checks if a CSV file has been imported
        - reads the CSV file using pandas
        - creates a comprehensive summary including:
          * file information
          * data preview
        - displays the report in the text area
        - updates report.txt with the full report content
        """
        if not self.csv_file_path:
            return
        
        try:
            # read CSV file
            df = pd.read_csv(self.csv_file_path)
            
            # generate summary report
            self.report_content = f"Dataset Summary Report\n{'='*50}\n\n"
            self.report_content += f"File: {os.path.basename(self.csv_file_path)}\n"
            
            self.report_content += f"\nData Preview (first 5 rows):\n{df.head().to_string()}"
            
            # display report
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(1.0, self.report_content)
            
            # update report.txt with the full report content
            with open("report.txt", "w") as f:
                f.write(self.report_content)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
    
    def save_report(self):
        """
        Save the generated report to a text file.
        
        This function:
        - checks if a report has been generated
        - opens a save file dialog
        - writes the report content to the selected file
        - provides success/error feedback to the user
        """
        if not self.report_content:
            messagebox.showerror("Error", "Please import a CSV file first!")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Report",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            
            if file_path:
                with open(file_path, "w") as f:
                    f.write(self.report_content)
                messagebox.showinfo("Success", "Report saved successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")
    
    def on_closing(self):
        """
        Clean up when the application closes.
        """
        if self.file_monitor:
            self.file_monitor.stop()
            self.file_monitor.join()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReportGenerator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()