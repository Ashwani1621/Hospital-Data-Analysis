import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables for dataframes
general_df = None
prenatal_df = None
sports_df = None
merged_df = None

# File loading functions
def load_general_file():
    global general_df
    file_path = filedialog.askopenfilename(title="Select General Hospital CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        general_df = pd.read_csv(file_path)
        lbl_general_status.config(text="File Loaded Successfully", fg="green")

def load_prenatal_file():
    global prenatal_df
    file_path = filedialog.askopenfilename(title="Select Prenatal Hospital CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        prenatal_df = pd.read_csv(file_path)
        lbl_prenatal_status.config(text="File Loaded Successfully", fg="green")

def load_sports_file():
    global sports_df
    file_path = filedialog.askopenfilename(title="Select Sports Hospital CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        sports_df = pd.read_csv(file_path)
        lbl_sports_status.config(text="File Loaded Successfully", fg="green")

# Merge dataframes and give user options
def merge_dataframes():
    global merged_df
    if general_df is not None and prenatal_df is not None and sports_df is not None:
        # Clean column names
        prenatal_df.rename(columns={"HOSPITAL": "hospital", "Sex": "gender"}, inplace=True)
        sports_df.rename(columns={"Hospital": "hospital", "Male/female": "gender"}, inplace=True)

        # Merge the data
        merged_df = pd.concat([general_df, prenatal_df, sports_df], ignore_index=True)
        
        # Remove unnecessary columns and clean data
        if "Unnamed: 0" in merged_df.columns:
            merged_df.drop(columns=["Unnamed: 0"], inplace=True)
        merged_df.dropna(how="all", inplace=True)

        # Clean and standardize the 'gender' column
        merged_df["gender"] = merged_df["gender"].replace(["man", "male"], "m")
        merged_df["gender"] = merged_df["gender"].replace(["woman", "female", np.nan], "f")

        # Fill missing values with 0 for simplicity
        merged_df.fillna(0, inplace=True)

        # Remove rows where hospital has 0 values
        merged_df["hospital"] = merged_df["hospital"].astype(str).str.strip()
        merged_df = merged_df[merged_df["hospital"] != "0"]

        lbl_merge_status.config(text="Data Merged Successfully!", fg="green")

        # Show download and visualize buttons
        btn_download.grid(row=4, column=4, padx=10, pady=10)
        btn_visualize.grid(row=5, column=4, padx=10, pady=10)
    else:
        messagebox.showerror("Error", "Please load all files before merging.")

# Save merged data to file
def download_merged_data():
    if merged_df is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path.endswith('.xlsx'):
            merged_df.to_excel(file_path, index=False)
        else:
            merged_df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Data saved to {file_path}")
    else:
        messagebox.showerror("Error", "No data to save.")

# Visualization placeholder
def visualize_data():
    # Create a new window for visualization
    visualize_window = tk.Toplevel()
    visualize_window.title("Data Visualization")
    
    visualize_window.configure(bg='#f0f0f0')
    visualize_window.state("zoomed")

    # Define a function to display each type of plot
    def show_bar_chart():
        plt.figure(figsize=(6, 4))
        merged_df["hospital"].value_counts().plot(kind="bar", title="Number of Patients per Hospital")
        plt.ylabel("Number of Patients")
        plt.xlabel("Hospital Type")
        plt.show()

    def show_pie_chart():
        plt.figure(figsize=(6, 4))
        merged_df["diagnosis"].value_counts().plot(kind="pie", title="Diagnosis Distribution", autopct='%1.1f%%')
        plt.ylabel("")
        plt.show()

    def show_violin_plot():
        plt.figure(figsize=(6, 4))
        sns.violinplot(data=merged_df, x="hospital", y="height")
        plt.title("Height Distribution by Hospital")
        plt.show()

    def show_gender_breakdown_chart():
        plt.figure(figsize=(6, 4))
        gender_hospital_counts = merged_df.groupby(['hospital', 'gender']).size().unstack()
        gender_hospital_counts.plot(kind='bar', stacked=True, title="Gender Breakdown by Hospital")
        plt.ylabel("Number of Patients")
        plt.xlabel("Hospital")
        plt.legend(title="Gender")
        plt.tight_layout()  # Adjust layout to fit labels and titles
        plt.show()

    # Add buttons for each visualization
    lbl_heading = tk.Label(visualize_window,text="Following Reports are generated for the given sample of Hospital Data:",font=("Arial", 32,"bold"),)
    lbl_heading.pack(pady=40)

    btn_bar_chart = tk.Button(visualize_window, text="Bar Chart of Patients per Hospital",font=("Arial", 20), command=show_bar_chart, bg='#4CAF50', fg='white')
    btn_bar_chart.pack(pady=10)

    btn_pie_chart = tk.Button(visualize_window, text="Pie Chart of Diagnosis Distribution",font=("Arial", 20), command=show_pie_chart, bg='#4CAF50', fg='white')
    btn_pie_chart.pack(pady=10)

    btn_violin_plot = tk.Button(visualize_window, text="Violin Plot of Height Distribution",font=("Arial", 20), command=show_violin_plot, bg='#4CAF50', fg='white')
    btn_violin_plot.pack(pady=10)

    btn_gender_breakdown = tk.Button(visualize_window, text="Gender Breakdown by Hospital",font=("Arial", 20), command=show_gender_breakdown_chart, bg='#4CAF50', fg='white')
    btn_gender_breakdown.pack(pady=10)

    # Add an exit button to close the visualization window
    btn_close = tk.Button(visualize_window, text="Back",font=("Arial", 20), command=visualize_window.destroy, bg='#f44336', fg='white')
    btn_close.pack(pady=30)

# File Upload GUI
def create_file_upload_gui():
    global lbl_general_status, lbl_prenatal_status, lbl_sports_status, lbl_merge_status, btn_download, btn_visualize

    root = tk.Tk()
    root.title("Data Analysis for Hospitals")
    root.configure(bg='#f0f0f0')
    root.state("zoomed")

    # General hospital file load button and status label
    btn_load_general = tk.Button(root, text="Load General Hospital Data",font=("Arial", 20), command=load_general_file, bg='#4CAF50', fg='white')
    btn_load_general.grid(row=0, column=3, padx=10, pady=10)
    lbl_general_status = tk.Label(root, text="Not Loaded", font=("Arial", 20),fg="red")
    lbl_general_status.grid(row=0, column=4, padx=10)

    # Prenatal hospital file load button and status label
    btn_load_prenatal = tk.Button(root, text="Load Prenatal Hospital Data",font=("Arial", 20), command=load_prenatal_file, bg='#4CAF50', fg='white')
    btn_load_prenatal.grid(row=1, column=3, padx=10, pady=10)
    lbl_prenatal_status = tk.Label(root, text="Not Loaded",font=("Arial", 20), fg="red")
    lbl_prenatal_status.grid(row=1, column=4, padx=10)

    # Sports hospital file load button and status label
    btn_load_sports = tk.Button(root, text="Load Sports Hospital Data",font=("Arial", 20), command=load_sports_file, bg='#4CAF50', fg='white')
    btn_load_sports.grid(row=2, column=3, padx=10, pady=10)
    lbl_sports_status = tk.Label(root, text="Not Loaded",font=("Arial", 20), fg="red")
    lbl_sports_status.grid(row=2, column=4, padx=10)

    # Merge data button
    lbl_merge_status = tk.Label(root, text="",font=("Arial", 20), fg="green")
    lbl_merge_status.grid(row=3, column=4, padx=10)

    btn_merge_data = tk.Button(root, text="Merge Data",font=("Arial", 20), command=merge_dataframes, bg='#4CAF50', fg='white')
    btn_merge_data.grid(row=3, column=3, padx=10, pady=10)

    # Download merged data button (hidden initially)
    btn_download = tk.Button(root, text="Download Merged Data",font=("Arial", 20), command=download_merged_data, bg='#4CAF50', fg='white')
    btn_download.grid(row=4, column=4, padx=10, pady=20)
    btn_download.grid_remove()

    # Visualize data button (hidden initially)
    btn_visualize = tk.Button(root, text="Visualize Data",font=("Arial", 20), command=visualize_data, bg='#4CAF50', fg='white')
    btn_visualize.grid(row=5, column=4, padx=10, pady=20)
    btn_visualize.grid_remove()

    # Exit button
    btn_quit = tk.Button(root, text="Exit", command=root.destroy,font=("Arial", 20), bg='#f44336', fg='white')
    btn_quit.grid(row=6, column=4, padx=10, pady=30, columnspan=2)

    root.mainloop()


# Intro GUI
def create_intro_window():
    intro_window = tk.Tk()
    intro_window.title("Welcome to Hospital Data Analysis")
    intro_window.geometry("400x300")
    intro_window.configure(bg='#f0f0f0')
    intro_window.state("zoomed")

    lbl_welcome = tk.Label(intro_window, text="Welcome to the Hospital Data Analysis App!", font=("Arial", 48, "bold"), bg='#f0f0f0')
    lbl_welcome.pack(pady=20)

    lbl_description = tk.Label(intro_window, text="This app helps analyze hospital data and generate reports on various statistics.\n You can load hospital data files, merge them, and perform analysis.", font=("Arial", 24), bg='#f0f0f0')
    lbl_description.pack(pady=20)

    btn_get_started = tk.Button(intro_window, text="Get Started", font=("Arial", 20), bg='#4CAF50', fg='white', command=lambda: [intro_window.destroy(), create_file_upload_gui()])
    btn_get_started.pack(pady=20)

    btn_quit = tk.Button(intro_window, text="Quit", font=("Arial", 20), bg='#f44336', fg='white', command=intro_window.destroy)
    btn_quit.pack(pady=20)
    intro_window.mainloop()

# Start the app with the intro window
create_intro_window()
