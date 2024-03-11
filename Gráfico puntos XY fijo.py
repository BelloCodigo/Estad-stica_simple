import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import Tk, filedialog, Label, Entry, Button, messagebox

# Variables globales
data = None
ruta_archivo = None
column_names = None
nombre_archivo = None 

# Función para cargar el archivo CSV
def load_csv():
    global data, ruta_archivo, column_names, nombre_archivo
    
    ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    if ruta_archivo:
        nombre_archivo = os.path.splitext(os.path.basename(ruta_archivo))[0]

        csv_data = pd.read_csv(ruta_archivo)
        
        data = csv_data.iloc[:, [3, 4]] 
        column_names = csv_data.columns[[3, 4]]
        
        messagebox.showinfo("Info", "Datos cargados exitosamente.")

# Función para generar el gráfico de puntos con ejes intercambiados, grilla, configurables xticks y yticks, líneas verticales y horizontales
def generate_points_graph():
    global data, column_names, nombre_archivo

    series_name = entry_series_name.get()

    fig, ax = plt.subplots()

    points = ax.scatter(data.iloc[:, 1], data.iloc[:, 0], label=series_name)

    ax.set_xlabel(column_names[1]) 
    ax.set_ylabel(column_names[0]) 

    ax.grid(True, axis='both')

    try:
        xticks_interval = float(entry_xticks.get())
        yticks_interval = float(entry_yticks.get())
        xtick_min = float(entry_xtick_min.get())
        xtick_max = float(entry_xtick_max.get())
        ytick_min = float(entry_ytick_min.get())
        ytick_max = float(entry_ytick_max.get())

        ax.set_xticks(np.arange(xtick_min, xtick_max, xticks_interval))
        ax.set_yticks(np.arange(ytick_min, ytick_max, yticks_interval))

        ax.set_xticklabels([f'{tick:.0f}' for tick in ax.get_xticks()])
        ax.set_yticklabels([f'{tick:.0f}' for tick in ax.get_yticks()])

        # Ajuste del rango del eje x
        ax.set_xlim(xtick_min, xtick_max)

        # Ajuste del rango del eje y
        ax.set_ylim(ytick_min, ytick_max)
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos para xticks y yticks.")
        return

    ax.legend()

    annotations = []
    for x, y in zip(data.iloc[:, 1], data.iloc[:, 0]):
        annotation = ax.annotate(f'x: {x:.0f}, y: {y:.0f}', (x, y), textcoords="offset points", xytext=(10,10), ha='left', fontsize=8, visible=False)
        annotations.append(annotation)

    def show_annotations(event):
        x, y = event.xdata, event.ydata
        if x is not None and y is not None:
            for ann in annotations:
                ann.set_visible(False)
            for x, y in zip(data.iloc[:, 1], data.iloc[:, 0]):
                if abs(x - event.xdata) < 0.05 and abs(y - event.ydata) < 0.05:
                    ann = next(ann for ann in annotations if ann.xy == (x, y))
                    ann.set_visible(True)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', show_annotations)

    try:
        vertical_line_value = float(entry_vertical_line_value.get())
        ax.axvline(x=vertical_line_value, color='r', linestyle='--')
        
        vertical_label_position = float(entry_vertical_label_position.get())
        ax.text(vertical_line_value, vertical_label_position, f' {vertical_line_value:.0f}°', rotation=0, verticalalignment='bottom',color='red', fontweight='bold')
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un valor numérico válido para la línea vertical y la posición del label.")
        return

    try:
        horizontal_line_value = float(entry_horizontal_line_value.get())
        ax.axhline(y=horizontal_line_value, color='b', linestyle='--')
        
        horizontal_label_position = float(entry_horizontal_label_position.get())
        ax.text(horizontal_label_position, horizontal_line_value, f' {horizontal_line_value:.1f}m', rotation=0, verticalalignment='bottom',color='blue', fontweight='bold')
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un valor numérico válido para la línea horizontal y la posición del label.")
        return

    plt.title(nombre_archivo) 
    
    plt.show()

root = Tk()
root.title("Configuración del Gráfico de Puntos")

Label(root, text="Nombre de la Serie:").grid(row=0, column=0)
entry_series_name = Entry(root)
entry_series_name.grid(row=0, column=1)
entry_series_name.insert(0, "Perfil validado")

Label(root, text="Intervalo de xticks:").grid(row=1, column=0)
entry_xticks = Entry(root)
entry_xticks.grid(row=1, column=1)
entry_xticks.insert(0, "5")

Label(root, text="Intervalo de yticks:").grid(row=2, column=0)
entry_yticks = Entry(root)
entry_yticks.grid(row=2, column=1)
entry_yticks.insert(0, "2")

Label(root, text="Valor mínimo de xtick:").grid(row=3, column=0)
entry_xtick_min = Entry(root)
entry_xtick_min.grid(row=3, column=1)
entry_xtick_min.insert(0, "45")

Label(root, text="Valor máximo de xtick:").grid(row=4, column=0)
entry_xtick_max = Entry(root)
entry_xtick_max.grid(row=4, column=1)
entry_xtick_max.insert(0, "90")

Label(root, text="Valor mínimo de ytick:").grid(row=5, column=0)
entry_ytick_min = Entry(root)
entry_ytick_min.grid(row=5, column=1)
entry_ytick_min.insert(0, "0")

Label(root, text="Valor máximo de ytick:").grid(row=6, column=0)
entry_ytick_max = Entry(root)
entry_ytick_max.grid(row=6, column=1)
entry_ytick_max.insert(0, "20")

Label(root, text="Valor de la línea vertical:").grid(row=7, column=0)
entry_vertical_line_value = Entry(root)
entry_vertical_line_value.grid(row=7, column=1)
entry_vertical_line_value.insert(0, "80")

Label(root, text="Posición del label de la línea vertical:").grid(row=8, column=0)
entry_vertical_label_position = Entry(root)
entry_vertical_label_position.grid(row=8, column=1)
entry_vertical_label_position.insert(0, "18")

Label(root, text="Valor de la línea horizontal:").grid(row=9, column=0)
entry_horizontal_line_value = Entry(root)
entry_horizontal_line_value.grid(row=9, column=1)
entry_horizontal_line_value.insert(0, "10")

Label(root, text="Posición del label de la línea horizontal:").grid(row=10, column=0)
entry_horizontal_label_position = Entry(root)
entry_horizontal_label_position.grid(row=10, column=1)
entry_horizontal_label_position.insert(0, "90")

Button(root, text="Cargar CSV", command=load_csv).grid(row=11, column=0, columnspan=2)
Button(root, text="Generar Gráfico de Puntos", command=generate_points_graph).grid(row=12, column=0, columnspan=2)

root.mainloop()
