#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Formulario de escritorio con Tkinter que muestra una grilla con los datos
de un archivo CSV (ejemplo.csv) y un botón para salir.
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Ruta del archivo CSV (mismo directorio que este script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "ejemplo.csv")


def leer_csv(ruta):
    """Lee el archivo CSV y devuelve (encabezados, filas)."""
    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, delimiter=",")
        datos = [fila for fila in lector if fila]  # ignora líneas vacías
    if not datos:
        return [], []
    encabezados = datos[0]
    filas = datos[1:]
    return encabezados, filas


class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Formulario Grilla de Ejemplo.")

        # Iniciar maximizado (Windows). Fallback para otros sistemas.
        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-zoomed", True)

        self._crear_widgets()
        self._cargar_datos()

    def _configurar_estilo(self):
        """Configura la grilla con una paleta de tonos azules."""
        # Paleta de azules
        AZUL_CELDA = "#eaf2fb"        # fondo de las celdas (azul muy claro)
        AZUL_CELDA_ALT = "#d4e4f7"    # fondo de filas alternas (azul claro)
        AZUL_TEXTO = "#0d2f5c"        # texto (azul oscuro) -> buen contraste
        AZUL_ENCABEZADO = "#1e5aa8"   # fondo del encabezado (azul medio)
        AZUL_ENCABEZADO_ACT = "#17457f"  # encabezado al pasar el mouse
        AZUL_SELECCION = "#2f6fbf"    # fondo de la fila seleccionada
        BLANCO = "#ffffff"

        estilo = ttk.Style(self)
        # 'clam' permite personalizar colores de forma consistente
        estilo.theme_use("clam")

        # Cuerpo de la grilla (celdas)
        estilo.configure(
            "Azul.Treeview",
            background=AZUL_CELDA,
            fieldbackground=AZUL_CELDA,
            foreground=AZUL_TEXTO,
            rowheight=26,
            bordercolor=AZUL_ENCABEZADO,
            borderwidth=1,
        )
        # Fila seleccionada: fondo azul fuerte + texto blanco (alto contraste)
        estilo.map(
            "Azul.Treeview",
            background=[("selected", AZUL_SELECCION)],
            foreground=[("selected", BLANCO)],
        )

        # Encabezados
        estilo.configure(
            "Azul.Treeview.Heading",
            background=AZUL_ENCABEZADO,
            foreground=BLANCO,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        estilo.map(
            "Azul.Treeview.Heading",
            background=[("active", AZUL_ENCABEZADO_ACT)],
        )

        # Guardamos colores para las filas alternas
        self._color_par = AZUL_CELDA
        self._color_impar = AZUL_CELDA_ALT

    def _crear_widgets(self):
        self._configurar_estilo()

        # Contenedor principal
        contenedor = ttk.Frame(self, padding=10)
        contenedor.pack(fill=tk.BOTH, expand=True)

        # Marco para la grilla + scrollbars
        marco_grilla = ttk.Frame(contenedor)
        marco_grilla.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(
            marco_grilla, show="headings", style="Azul.Treeview"
        )

        scroll_y = ttk.Scrollbar(
            marco_grilla, orient=tk.VERTICAL, command=self.tree.yview
        )
        scroll_x = ttk.Scrollbar(
            marco_grilla, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        marco_grilla.rowconfigure(0, weight=1)
        marco_grilla.columnconfigure(0, weight=1)

        # Marco para los botones
        marco_botones = ttk.Frame(contenedor)
        marco_botones.pack(fill=tk.X, pady=(10, 0))

        boton_salir = ttk.Button(
            marco_botones, text="Salir", command=self.destroy
        )
        boton_salir.pack(side=tk.RIGHT)

    def _cargar_datos(self):
        if not os.path.exists(CSV_PATH):
            messagebox.showerror(
                "Error",
                f"No se encontró el archivo:\n{CSV_PATH}",
            )
            return

        try:
            encabezados, filas = leer_csv(CSV_PATH)
        except Exception as error:  # noqa: BLE001
            messagebox.showerror(
                "Error", f"No se pudo leer el archivo CSV:\n{error}"
            )
            return

        if not encabezados:
            messagebox.showwarning(
                "Aviso", "El archivo CSV no contiene datos."
            )
            return

        # Configurar columnas de la grilla
        self.tree["columns"] = encabezados
        for col in encabezados:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150, anchor=tk.W, stretch=True)

        # Etiquetas para filas alternas (efecto cebra en tonos azules)
        self.tree.tag_configure("par", background=self._color_par)
        self.tree.tag_configure("impar", background=self._color_impar)

        # Insertar filas
        for indice, fila in enumerate(filas):
            etiqueta = "par" if indice % 2 == 0 else "impar"
            self.tree.insert("", tk.END, values=fila, tags=(etiqueta,))


def main():
    app = Aplicacion()
    app.mainloop()


if __name__ == "__main__":
    main()
