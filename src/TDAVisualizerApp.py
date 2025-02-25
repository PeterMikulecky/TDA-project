"""
TDAVisualizerApp.py

This is the main driver script for the TDA Time Series Visualizer package.

The package offers a user-friendly way for non-specialist researchers to assess 
whether their time series data might benefit from topological data analysis (TDA).

This driver makes the app available from a simple GUI. For a CLI-driven interface, 
use the alternative driver, main.py.

Workflow:
1. Prompt the user to browse to select two CSV files, each containing two columns: 
    timestep and signal data.
2. Prompt the user to input parameters for dimension and lag.
3. Validate the data in the provided files.
4. Use the dimension and lag parameters to perform delay-embedding of the time 
    series, producing point clouds.
5. Subject the point clouds to persistence homology analysis to produce persistence
    diagrams, highlighting the persistence of topological features across homology 
    groups (H0: points, H1: holes, H2: volumes).
6. Compare the persistence diagrams of the two time series by calculating the 
    Wasserstein distance, normalized against the standard deviation of the 
    persistence lifetimes of each persistence diagram.
7. Output five plots, saving them to the source code directory and displaying them
    within the GUI:
    - Point cloud for time series 1
    - Point cloud for time series 2
    - Persistence diagram for time series 1
    - Persistence diagram for time series 2
    - Wasserstein distance normalized against the lifetime standard deviation of 
        each persistence diagram

Dependencies:
- data_validator.py: Validates the data in the provided CSV files.
- delay_embedder.py: Delay-embeds the time series to produce point clouds.
- persistence_analyzer.py: Analyzes the point clouds using persistence homology 
    to produce persistence diagrams.
- visualizer.py: Visualizes the point clouds and persistence diagrams, and 
    calculates the Wasserstein distance.
- other python packages from the PSL or installable by pip, as detailed in 
    requirements.txt.

Example:
To run the script, from within /TDA-project/src/, use one of the following commands:
    python TDAVisualizerApp.py
    python3 TDAVisualizerApp.py

Authors:
    Peter Mikulecky and Patrick Hudson

Date:
    2/25/25

"""
# Imports
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import numpy as np
import csv
import data_validator
import delay_embedder
import persistence_analyzer
import visualizer
import tkinter as tk

class TDAVisualizerApp:
    """
    Tkinter GUI for visualizing Topological Data Analysis (TDA) results.
    """
    def __init__(self, root):
        """
        Initializes the TDAVisualizerApp.
        
        Args:
            root (tkinter.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("Topological Data Analysis Visualizer")
        self.root.geometry("800x600")  # Initial size of the window

        # File paths
        self.file1_path = ""
        self.file2_path = ""

        # Labels and entry fields for file selection
        tk.Label(root, text="First Data File").grid(row=0, column=0, pady=2)
        self.file1_entry = tk.Entry(root, width=50)
        self.file1_entry.grid(row=0, column=1, pady=2)
        tk.Button(root, text="Browse", command=self.browse_file1).grid(row=0, column=2, pady=2)

        tk.Label(root, text="Second Data File").grid(row=1, column=0, pady=2)
        self.file2_entry = tk.Entry(root, width=50)
        self.file2_entry.grid(row=1, column=1, pady=2)
        tk.Button(root, text="Browse", command=self.browse_file2).grid(row=1, column=2, pady=2)

        # Labels and entry fields for parameters
        tk.Label(root, text="Dimension").grid(row=2, column=0, pady=2)
        self.dimension_entry = tk.Entry(root)
        self.dimension_entry.grid(row=2, column=1, pady=2)

        tk.Label(root, text="Lag").grid(row=3, column=0, pady=2)
        self.lag_entry = tk.Entry(root)
        self.lag_entry.grid(row=3, column=1, pady=2)

        # Button to start processing
        tk.Button(root, text="Run Analysis", command=self.run_analysis).grid(row=4, columnspan=3, pady=5)

        # Text box to show messages
        self.message_box = tk.Text(root, width=80, height=8)
        self.message_box.grid(row=5, columnspan=3, pady=5)

        # Canvas and Scrollbar for displaying images
        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=6, column=3, sticky="ns")
        self.canvas.grid(row=6, columnspan=3, pady=5, sticky="nsew")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.image_frame = tk.Frame(self.canvas)

        # Ensure the canvas and image_frame expand properly
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.image_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.grid(row=6, columnspan=3, pady=3, sticky="nsew")
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Make sure the row and column expand
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def on_frame_configure(self, event):
        """
        Updates the scroll region of the canvas when the image frame is resized.
        
        Args:
            event (tkinter.Event): The configuration event.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        print(f"Image frame resized: width={self.image_frame.winfo_width()}, height={self.image_frame.winfo_height()}")

    def browse_file1(self):
        """
        Opens a file dialog to select the first CSV file.
        """
        self.file1_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file1_entry.delete(0, tk.END)
        self.file1_entry.insert(0, self.file1_path)

    def browse_file2(self):
        """
        Opens a file dialog to select the second CSV file.
        """
        self.file2_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        self.file2_entry.delete(0, tk.END)
        self.file2_entry.insert(0, self.file2_path)

    def run_analysis(self):
        """
        Runs the TDA analysis based on the selected files and parameters.
        """
        dimension = self.dimension_entry.get()
        lag = self.lag_entry.get()

        try:
            dimension = int(dimension)
            lag = int(lag)
            if dimension <= 0 or lag <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Both dimension and lag must be positive integers.")
            return

        if not self.file1_path or not self.file2_path:
            messagebox.showerror("File Error", "Both data files must be selected.")
            return

        self.message_box.insert(tk.END, "Validating files...\n")
        self.message_box.update()

        validator = data_validator.Validation(self.file1_path, self.file2_path)
        validation_result = validator.validate_files()
        if validation_result != "Both files are successfully validated.":
            self.message_box.insert(tk.END, f"{validation_result}\n")
            return

        self.message_box.insert(tk.END, "Converting files to arrays...\n")
        self.message_box.update()

        timeseries1 = self.read_csv_column(self.file1_path)
        timeseries2 = self.read_csv_column(self.file2_path)

        if timeseries1 is None or timeseries2 is None:
            return

#        self.message_box.insert(tk.END, f"Timeseries1 Length: {len(timeseries1)}\n")
#        self.message_box.insert(tk.END, f"Timeseries2 Length: {len(timeseries2)}\n")
#        self.message_box.update()

        self.message_box.insert(tk.END, "Performing delay embedding...\n")
        self.message_box.update()

        embedding1 = delay_embedder.DelayEmbedding(timeseries1, dimension, lag).generate_embedding()
        embedding2 = delay_embedder.DelayEmbedding(timeseries2, dimension, lag).generate_embedding()

#        self.message_box.insert(tk.END, f"Embedding1 Shape: {embedding1.shape}\n")
#        self.message_box.insert(tk.END, f"Embedding2 Shape: {embedding2.shape}\n")
#        self.message_box.update()

        self.message_box.insert(tk.END, "Performing persistence analysis...this could take a minute...\n")
        self.message_box.update()

        persistence_analysis = persistence_analyzer.PersistenceAnalysis(embedding1, embedding2)
        persistence_analysis.diagrams1 = persistence_analysis.generate_persistence_homology(embedding1)
        persistence_analysis.diagrams2 = persistence_analysis.generate_persistence_homology(embedding2)

        wasserstein_dist = persistence_analysis.compute_wasserstein_distance(persistence_analysis.diagrams1, persistence_analysis.diagrams2)
        std_lifetimes1 = persistence_analysis.compute_std_lifetimes(persistence_analysis.diagrams1)
        std_lifetimes2 = persistence_analysis.compute_std_lifetimes(persistence_analysis.diagrams2)

        self.message_box.insert(tk.END, f"Wasserstein Distance: {wasserstein_dist}\n")
#        self.message_box.insert(tk.END, f"Standard Deviation of Lifetimes (File 1): {std_lifetimes1}\n")
#        self.message_box.insert(tk.END, f"Standard Deviation of Lifetimes (File 2): {std_lifetimes2}\n")
        self.message_box.update()

        if std_lifetimes1 is None or std_lifetimes2 is None:
            messagebox.showerror("Analysis Error", "Failed to compute standard deviation of lifetimes for the persistence diagrams.")
            return

        self.message_box.insert(tk.END, "Generating visualizations...\n")
        self.message_box.update()

        self.clear_image_frame()
        visualization = visualizer.Visualization()
        visualization.plot_point_cloud(embedding1)
        visualization.plot_point_cloud(embedding2)
        visualization.plot_persistence_homology(persistence_analysis.diagrams1)
        visualization.plot_persistence_homology(persistence_analysis.diagrams2)
        visualization.plot_normalized_wasserstein(wasserstein_dist, std_lifetimes1, std_lifetimes2)

        self.display_image('point_cloud_0.png')
        self.display_image('point_cloud_1.png')
        self.display_image('persistence_diagram_combined_0.png')
        self.display_image('persistence_diagram_combined_1.png')
        self.display_image('normalized_wasserstein.png')

        self.message_box.insert(tk.END, "Analysis complete! These plots are also saved to source directory.\n")

    def display_image(self, img_path):
        """
        Displays an image in the image frame.
        
        Args:
            img_path (str): The path to the image file.
        """
        try:
            print(f"Loading image from: {img_path}")
            self.root.update_idletasks()
    
            img = Image.open(img_path)
            img.thumbnail((350, 350)) #added image resizing.
            img_tk = ImageTk.PhotoImage(img)
    
            img_label = tk.Label(self.image_frame, image=img_tk)
            img_label.image = img_tk
            img_label.pack()
    
            self.image_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
            print(f"Image loaded and displayed from: {img_path}")
        except Exception as e:
            self.message_box.insert(tk.END, f"Error displaying image: {e}\n")
            self.message_box.update()

    def clear_image_frame(self):
        """
        Clears all widgets from the image frame.
        """
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def read_csv_column(self, file_path):
        """
        Reads the second column of a CSV file and returns it as a NumPy array.
        
        Args:
            file_path (str): The path to the CSV file.
        
        Returns:
            numpy.ndarray: The second column of the CSV file as a NumPy array, or None if an error occurs.
        """
        try:
            second_column = []
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    second_column.append(row[1])
            return np.array(second_column, dtype=float)
        except Exception as e:
            messagebox.showerror("File Error", f"An error occurred while reading the file: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = TDAVisualizerApp(root)
    root.mainloop()
