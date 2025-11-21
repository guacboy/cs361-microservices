import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime

class SuggestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Suggestion Box")
        self.root.geometry("500x400")
        
        # initialize suggestions array
        self.suggestions = []
        
        self.setup_ui()
        
    def create_main_frame(self):
        """
        Create and return the main frame.
        """
        main_frame = tk.Frame(self.root,
                              padx=20,
                              pady=20)
        main_frame.pack(fill=tk.BOTH,
                        expand=True)
        return main_frame
    
    def create_title_section(self, parent):
        """
        Create the title section.
        """
        title_label = tk.Label(parent, 
                               text="Submit Your Suggestion", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
    
    def create_input_section(self, parent):
        """
        Create the suggestion input section.
        """
        entry_label = tk.Label(parent,
                               text="Enter your suggestion:", 
                               font=("Arial", 12))
        entry_label.pack(anchor="w",
                         pady=(20, 5))
        
        self.entry_box = tk.Text(parent,
                                 height=8,
                                 width=50, 
                                 font=("Arial", 10))
        self.entry_box.pack(fill=tk.BOTH,
                            expand=True,
                            pady=5)
    
    def create_file_attachment_section(self, parent):
        """
        Create the file attachment section.
        """
        self.file_label = tk.Label(parent,
                                   text="No file attached", 
                                   fg="gray",
                                   font=("Arial", 9))
        self.file_label.pack(anchor="w",
                             pady=(5, 0))
    
    def create_button_section(self, parent):
        """
        Create the button section.
        """
        button_frame = tk.Frame(parent)
        button_frame.pack(fill=tk.X,
                          pady=20)
        
        self.create_attach_button(button_frame)
        self.create_submit_button(button_frame)
    
    def create_attach_button(self, parent):
        """
        Create the attach file button.
        """
        self.attach_btn = tk.Button(parent,
                                    text="Attach File", 
                                    command=self.attach_file,
                                    font=("Arial", 10))
        self.attach_btn.pack(side=tk.LEFT,
                             padx=(0, 10))
    
    def create_submit_button(self, parent):
        """
        Create the submit button.
        """
        self.submit_btn = tk.Button(parent, 
                                    text="Submit Suggestion", 
                                    command=self.submit_suggestion,
                                    font=("Arial", 10, "bold"),
                                    bg="#4CAF50",
                                    fg="white")
        self.submit_btn.pack(side=tk.RIGHT)
    
    def setup_ui(self):
        """
        Setup the user interface by composing smaller functions.
        """
        main_frame = self.create_main_frame()
        self.create_title_section(main_frame)
        self.create_input_section(main_frame)
        self.create_file_attachment_section(main_frame)
        self.create_button_section(main_frame)
        
    def attach_file(self):
        """
        Open file picker to attach an image or document.
        """
        file_types = [
            ("All supported files", "*.jpg *.jpeg *.png *.pdf *.doc *.docx *.txt"),
            ("Images", "*.jpg *.jpeg *.png"),
            ("Documents", "*.pdf *.doc *.docx *.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select a file to attach",
            filetypes=file_types
        )
        
        if filename:
            self.attached_file = filename
            file_name = os.path.basename(filename)
            self.file_label.config(text=f"Attached: {file_name}", fg="green")
    
    def submit_suggestion(self):
        """
        Submit the suggestion to the file.
        """
        suggestion_text = self.entry_box.get("1.0", tk.END).strip()
        
        if not suggestion_text:
            messagebox.showwarning("Warning", "Please enter a suggestion before submitting.")
            return
        
        try:
            # create suggestion object
            suggestion_data = {
                "suggestion": suggestion_text,
                "timestamp": datetime.now().isoformat(),
                "has_attachment": self.attached_file is not None,
                "attachment_path": self.attached_file if self.attached_file else None
            }
            
            # add to suggestions array
            self.suggestions.append(suggestion_data)
            
            # write to suggestion.txt
            with open("suggestion.txt", "a", encoding="utf-8") as f:
                f.write(json.dumps(suggestion_data) + "\n")
            
            # show success message
            messagebox.showinfo("Success", "Your suggestion has been received and will be reviewed.")
            
            # clear the form
            self.entry_box.delete("1.0", tk.END)
            self.file_label.config(text="No file attached", fg="gray")
            self.attached_file = None
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit suggestion: {str(e)}")

def main():
    """
    Main function to run the suggestion app.
    """
    root = tk.Tk()
    app = SuggestionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()