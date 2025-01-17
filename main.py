import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import streamlit as st

# path variables
downloads_path = ""
destination_path = ""
threshold_time = 0

class ImageMoverHandler(FileSystemEventHandler):
    def __init__(self, downloads_path, destination_path, threshold_time):
        self.downloads_path = downloads_path
        self.destination_path = destination_path
        self.threshold_time = threshold_time

    def on_created(self, event):
        print("Event triggered")
        # waiting files to download completely
        time.sleep(4)

        # If the created event is a directory, just return
        if event.is_directory:
            return

        # Search through the Downloads folder for images
        self.search_and_move_images()

    def search_and_move_images(self):
        # Iterate over all files in the downloads folder
        for root, dirs, files in os.walk(self.downloads_path):
            # skip the directories
            dirs[:] = []  
            for file in files:  
                file_path = os.path.join(root, file)
                creation_time = os.path.getctime(file_path)

                # Skip the old files in downloads folder
                if creation_time < self.threshold_time:
                    continue  
                
                # sort the image files
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    try:
                        # Moving files to destination folder
                        new_path = os.path.join(self.destination_path, os.path.basename(file_path))
                        shutil.move(file_path, new_path)
                        print(f"Moved {file_path} to {new_path}")
                    except Exception as e:
                        print(f"Error moving file: {e}")

def start_program():
    event_handler = ImageMoverHandler(downloads_path, destination_path, threshold_time)
    observer.schedule(event_handler, downloads_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":

    # setting observer here to control it with buttons
    observer = Observer()


    st.title("Images Mover")
    st.divider()

    # Input for downloads folder path
    downloads_path = st.text_input("Downloads Folder", value=r"C:\Users\yashk\Downloads").strip()
    st.divider()

    # Input for destination folder
    destination_path = st.text_input("Destination Folder", value=r"C:\Users\yashk\Downloads\downloaded_imgs").strip()
    # st.write(f"Destination path set to: {destination_path}")
    st.divider()
    col1 , col2 = st.columns(2)

    with col1:
        start = st.button("Start")
    with col2:
        stop = st.button("Stop")
    
    

    if start:
        current_time = time.time()
        # Time threshold: 20 seconds ago
        threshold_time = current_time - 20

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        if os.path.exists(downloads_path) and os.path.isdir(downloads_path):
            if os.path.exists(destination_path) or os.makedirs(destination_path, exist_ok=True):
                st.write("Starting image mover...")
                start_program()
            else:
                st.error("Invalid destination folder. Could not create directory.")
        else:
            st.error("Invalid downloads folder path. Please check the input.")

    if stop:
        st.write("Stopping the program...")
        observer.stop()
       
