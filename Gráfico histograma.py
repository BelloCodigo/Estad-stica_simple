import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Label, Entry, Button, messagebox
import os

# Variables globales
data = None
ruta_archivo = None
selected_column = None
nombre_archivo = None  # Variable para almacenar el nombre del archivo sin la extensión

# Función para cargar el archivo CSV
def load_csv():
    global data, ruta_archivo, selected_column, nombre_archivo

    # Seleccionar archivo CSV
    ruta_archivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    # Verificar si el usuario seleccionó un archivo
    if ruta_archivo:
        # Extraer el nombre del archivo sin la extensión
        nombre_archivo = os.path.splitext(os.path.basename(ruta_archivo))[0]

        # Cargar los datos desde el archivo CSV
        csv_data = pd.read_csv(ruta_archivo)

        # Verificar si alguna de las columnas posibles está presente en los datos cargados
        possible_columns = ['Ancho Berma(R)', 'Angulo Cara-Banco(R)', 'Línea del Programa(R)']
        for col in possible_columns:
            if col in csv_data.columns:
                selected_column = col
                data = csv_data[selected_column]
                break

        if selected_column:
            messagebox.showinfo("Info", f"Datos cargados exitosamente desde la columna: {selected_column}.")
        else:
            messagebox.showerror("Error", "Ninguna de las columnas necesarias está presente en el archivo CSV.")

# Función para generar el histograma
def generate_histogram():
    global data, selected_column, nombre_archivo

    # Obtener los valores de entrada para bins, xticks, xmin, xmax, text_size, text_y_offset y xdata
    try:
        num_bins = int(entry_bins.get())
        xticks_interval = float(entry_xticks.get())
        x_min = float(entry_xmin.get())
        x_max = float(entry_xmax.get())
        text_size = float(entry_text_size.get())
        text_y_offset = float(entry_text_y_offset.get())
        xdata = float(entry_xdata.get())
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos para bins, xticks, xmin, xmax, text_size, text_y_offset y xdata.")
        return

    # Verificar si los valores de x_min y x_max son válidos
    if x_min >= x_max:
        messagebox.showerror("Error", "El valor mínimo de x debe ser menor que el valor máximo de x.")
        return

    # Calcular el histograma
    hist, bin_edges = np.histogram(data, bins=num_bins)

    # Calcular la frecuencia acumulada inversa en porcentaje del total de datos
    hist_inverse = np.cumsum(hist[::-1])[::-1]
    total_datos = len(data)
    hist_inverse_percent = (hist_inverse / total_datos) * 100

    # Calcular el percentil 20
    percentil_20 = np.percentile(data, 20)

    # Configurar la figura y los ejes
    fig, ax1 = plt.subplots()

    # Trazar el histograma con frecuencia acumulada inversa en el eje secundario
    points, = ax1.plot(bin_edges[:-1], hist_inverse_percent, color='orange', marker='o', label='Frecuencia acumulada inversa (%)')

    # Configurar etiquetas y título para el primer eje y
    ax1.set_xlabel(selected_column)
    ax1.set_ylabel('Frecuencia acumulada inversa (%)', color='orange')

    # Configurar límites del eje x
    ax1.set_xlim(x_min, x_max)

    # Configurar límites del eje y principal y secundario
    ax1.set_ylim(bottom=0)
    ax1.set_yticks(np.arange(0, 101, 10))

    # Configurar ticks del eje x
    ax1.set_xticks(np.arange(x_min, x_max, xticks_interval))

    # Agregar un segundo conjunto de barras para la frecuencia absoluta
    ax2 = ax1.twinx()
    bars = ax2.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor='black', alpha=0.5, color='blue', label='Frecuencia absoluta')

    # Configurar etiquetas para el segundo eje y
    ax2.set_ylabel('Frecuencia absoluta', color='blue')

    # Agregar leyendas
    ax1.legend(loc='lower left', fontsize='7', bbox_to_anchor=(0.5, -0.2))
    ax2.legend(loc='lower right', fontsize='7', bbox_to_anchor=(0.5, -0.2))


    # Agregar tooltips con annotate
    annotations = []
    for i, txt in enumerate(hist_inverse_percent):
        annotation = ax1.annotate(f'{bin_edges[:-1][i]:.1f}, {txt:.1f}%', (bin_edges[:-1][i], hist_inverse_percent[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=10, visible=False)
        annotations.append(annotation)

    # Función para mostrar las etiquetas cercanas al cursor
    def show_labels(event):
        x, _ = event.xdata, event.ydata
        if x is not None:
            for ann in annotations:
                ann.set_visible(abs(ann.xy[0] - x) < 0.05)
            fig.canvas.draw_idle()

    # Conectar la función de mostrar etiquetas al evento de mover el cursor
    fig.canvas.mpl_connect('motion_notify_event', show_labels)

    # Mostrar el valor del percentil 20 en el gráfico como una etiqueta de la línea
    ax1.axvline(x=percentil_20, color='green', linestyle='--')
    ax1.annotate(f'P80: {percentil_20:.0f}°', (percentil_20, text_y_offset), textcoords="offset points", xytext=(0,10), ha='left', fontsize=text_size, color='green')

    # Calcular el índice del bin al que pertenece xdata
    bin_index = np.digitize(xdata, bin_edges) - 1
    # Calcular el porcentaje de FACI para xdata
    fac_percentage = hist_inverse_percent[bin_index]

    # Mostrar el valor de xdata y su porcentaje de FACI en el gráfico
    ax1.axvline(x=xdata, color='red', linestyle='--')
    ax1.annotate(f'Diseño: {xdata:.0f}°, {fac_percentage:.0f}%', (xdata, text_y_offset), textcoords="offset points", xytext=(0,10), ha='left', fontsize=text_size, color='red')

    # Establecer el título del gráfico usando el nombre del archivo
    plt.title(nombre_archivo) # Añadir esta línea para establecer el título del gráfico

    # Configurar el bottom después de crear la figura
    fig.subplots_adjust(bottom=0.15)

    # Mostrar la gráfica
    plt.show()


# Crear una instancia de Tkinter
root = Tk()
root.title("Configuración del Histograma")

# Etiqueta y entrada para la cantidad de bins
Label(root, text="Cantidad de Bins:").grid(row=0, column=0)
entry_bins = Entry(root)
entry_bins.grid(row=0, column=1)
entry_bins.insert(0, "20")

# Etiqueta y entrada para los xticks
Label(root, text="Intervalo de xticks:").grid(row=1, column=0)
entry_xticks = Entry(root)
entry_xticks.grid(row=1, column=1)
entry_xticks.insert(0, "5")

# Etiqueta y entrada para el valor mínimo de x
Label(root, text="Valor mínimo de x:").grid(row=2, column=0)
entry_xmin = Entry(root)
entry_xmin.grid(row=2, column=1)
entry_xmin.insert(0, "45")

# Etiqueta y entrada para el valor máximo de x
Label(root, text="Valor máximo de x:").grid(row=3, column=0)
entry_xmax = Entry(root)
entry_xmax.grid(row=3, column=1)
entry_xmax.insert(0, "90")

# Etiqueta y entrada para el tamaño del texto de la etiqueta del percentil 20
Label(root, text="Tamaño del texto de la etiqueta del percentil 20:").grid(row=4, column=0)
entry_text_size = Entry(root)
entry_text_size.grid(row=4, column=1)
entry_text_size.insert(0, "10")

# Etiqueta y entrada para el desplazamiento vertical del texto de la etiqueta del percentil 20
Label(root, text="Desplazamiento vertical del texto de la etiqueta del percentil 20:").grid(row=5, column=0)
entry_text_y_offset = Entry(root)
entry_text_y_offset.grid(row=5, column=1)
entry_text_y_offset.insert(0, "85")

# Etiqueta y entrada para el valor de xdata
Label(root, text="Valor de xdata:").grid(row=6, column=0)
entry_xdata = Entry(root)
entry_xdata.grid(row=6, column=1)
entry_xdata.insert(0, "80")

# Botón para cargar el archivo CSV
Button(root, text="Cargar CSV", command=load_csv).grid(row=9, column=0, columnspan=2)

# Botón para generar el histograma
Button(root, text="Generar Histograma", command=generate_histogram).grid(row=10, column=0, columnspan=2)

root.mainloop()
