import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import rcParams


sns.set(style="whitegrid")
rcParams.update({'font.size': 9, 'figure.figsize': (8, 6)})  # Set global font size and figure size for matplotlib


bg_color = "#f0f0f0"
button_color = "#007acc"
text_color = "#ffffff"
font_spec = "Helvetica 10 bold"


window = tk.Tk()
window.title("EV Data Analysis Toolkit")
window.configure(bg=bg_color)


def load_data():
    global ev_data
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        ev_data = pd.read_csv(file_path)
        messagebox.showinfo("Information", "Data Loaded Successfully")
        enable_buttons()

def display_plot(figure):
    new_window = tk.Toplevel(window)
    new_window.configure(bg=bg_color)
    canvas = FigureCanvasTkAgg(figure, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def create_plot(plot_func):
    if ev_data is None:
        messagebox.showwarning("Warning", "Load data first")
        return
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_func(ax)
    display_plot(fig)

def enable_buttons():
    for button in plot_buttons:
        button['state'] = 'normal'

def plot_ev_adoption(ax):
    adoption_by_year = ev_data['Model Year'].value_counts().sort_index()
    sns.barplot(x=adoption_by_year.index, y=adoption_by_year.values, palette="viridis", ax=ax)
    ax.set(title='EV Adoption Over Time', xlabel='Model Year', ylabel='Number of Vehicles Registered')
    ax.set_xticklabels(adoption_by_year.index, rotation=45)  

def plot_ev_types(ax):
    ev_type_distribution = ev_data['Electric Vehicle Type'].value_counts()
    sns.barplot(y=ev_type_distribution.index, x=ev_type_distribution.values, palette="rocket", ax=ax)
    ax.set(title='Distribution of Electric Vehicle Types', xlabel='Number of Vehicles Registered', ylabel='Electric Vehicle Type')

def plot_ev_range_distribution(ax):
    sns.histplot(ev_data['Electric Range'], bins=30, kde=True, color='royalblue', ax=ax)
    ax.axvline(ev_data['Electric Range'].mean(), color='red', linestyle='--', label=f'Mean Range: {ev_data["Electric Range"].mean():.2f} miles')
    ax.set(title='Distribution of Electric Vehicle Ranges', xlabel='Electric Range (miles)', ylabel='Number of Vehicles')
    ax.legend()

def plot_ev_forecast(ax):

    ev_registration_counts = ev_data['Model Year'].value_counts().sort_index()
    
    filtered_years = ev_registration_counts[ev_registration_counts.index <= 2023]

    
    def exp_growth(x, a, b):
        return a * np.exp(b * x)

    
    x_data = filtered_years.index - filtered_years.index.min()
    y_data = filtered_years.values

    
    params, covariance = curve_fit(exp_growth, x_data, y_data)

   
    forecast_years = np.arange(2024, 2024 + 6) - filtered_years.index.min()
    forecasted_values = exp_growth(forecast_years, *params)

   
    ax.plot(filtered_years.index, filtered_years.values, 'bo-', label='Actual Registrations')
    ax.plot(forecast_years + filtered_years.index.min(), forecasted_values, 'ro--', label='Forecasted Registrations')

    ax.set(title='Current & Estimated EV Market', xlabel='Year', ylabel='Number of EV Registrations')
    ax.legend()
    ax.grid(True)

def show_all_plots():
    if ev_data is None:
        messagebox.showwarning("Warning", "Load data first")
        return
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    plot_ev_adoption(axs[0, 0])
    plot_ev_types(axs[0, 1])
    plot_ev_range_distribution(axs[1, 0])
    plot_ev_forecast(axs[1, 1])
    fig.tight_layout(pad=3.0)
    display_plot(fig)

frame_buttons = tk.Frame(window, bg=bg_color)
frame_buttons.pack(fill=tk.X)

load_button = tk.Button(frame_buttons, text="Load Data", command=load_data, bg=button_color, fg=text_color, font=font_spec)
load_button.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

plot_buttons = []
plot_adoption_button = tk.Button(frame_buttons, text="Show EV Adoption Over Time", command=lambda: create_plot(plot_ev_adoption), state='disabled', bg=button_color, fg=text_color, font=font_spec)
plot_buttons.append(plot_adoption_button)
plot_types_button = tk.Button(frame_buttons, text="Show EV Types Distribution", command=lambda: create_plot(plot_ev_types), state='disabled', bg=button_color, fg=text_color, font=font_spec)
plot_buttons.append(plot_types_button)
plot_range_button = tk.Button(frame_buttons, text="Show EV Range Distribution", command=lambda: create_plot(plot_ev_range_distribution), state='disabled', bg=button_color, fg=text_color, font=font_spec)
plot_buttons.append(plot_range_button)
plot_forecast_button = tk.Button(frame_buttons, text="Show EV Adoption Forecast", command=lambda: create_plot(plot_ev_forecast), state='disabled', bg=button_color, fg=text_color, font=font_spec)
plot_buttons.append(plot_forecast_button)
show_all_button = tk.Button(frame_buttons, text="Show All Plots", command=show_all_plots, state='disabled', bg=button_color, fg=text_color, font=font_spec)
plot_buttons.append(show_all_button)

for button in plot_buttons:
    button.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)

window.mainloop()
