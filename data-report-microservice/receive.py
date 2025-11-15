import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReportFileHandler(FileSystemEventHandler):
    """
    File system event handler for monitoring changes to report.txt.
    """
    
    def __init__(self):
        self.last_content = ""
    
    def on_modified(self, event):
        """
        Handle file modification events.
        """
        if event.src_path.endswith("report.txt"):
            self.process_report_file()
    
    def process_report_file(self):
        """
        Process the report.txt file when modifications are detected.
        
        This function:
        - reads the current content of report.txt
        - checks if the content has changed and is valid
        - detects CSV file imports and report generation
        """
        try:
            with open("report.txt", "r") as f:
                content = f.read().strip()
            
            # only process if content changed and is not empty
            if content and content != self.last_content:
                self.last_content = content
                
                # check if it's a CSV file path
                if os.path.exists(content) and content.lower().endswith('.csv'):
                    print(f"file path detected in report.txt: {content}")
                    print("report.py will automatically generate a report from this file...")
                
                # check if it's a report (starts with 'Dataset Summary Report')
                elif content.startswith("Dataset Summary Report"):
                    print("report generated and saved to report.txt\n")
                    # extract first few lines for preview
                    lines = content.split('\n')[:15]
                    for line in lines:
                        print(line)
                    if len(content.split('\n')) > 15:
                        print("... (full report saved in report.txt)")
                    print("=" * 60)
        
        except Exception as e:
            print(f"error processing report file: {e}")

def monitor_report_file():
    """
    Monitor the report.txt file for changes.
    
    This function:
    - sets up a file system observer
    - starts monitoring the current directory for changes
    - processes existing content on startup
    - runs continuously until interrupted
    """
    event_handler = ReportFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    
    print("monitoring report.txt for file path/report...")
    
    try:
        # process existing file on startup
        event_handler.process_report_file()
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    monitor_report_file()