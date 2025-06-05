import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Base de datos simulada de productos y cantidades esperadas
expected_products = {
    "product_001": 24,
    "product_002": 50,
    "product_003": 75
}

# Conectar a la base de datos MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto con tu nombre de usuario
        password="W7301@jqir#@",  # Cambia esto con tu contraseña
        database="vendor"
    )

# Función para guardar en MySQL
def save_to_database(product_id, provided_quantity, label_confirmed, box_fit):
    estado = "Correcto" if label_confirmed == 1 and box_fit == "Yes" else "Incorrecto"
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO registros_envios (product_id, cantidad, etiqueta_confirmada, tamano_caja_adecuado, estado)
        VALUES (%s, %s, %s, %s, %s)
    """, (product_id, provided_quantity, label_confirmed, box_fit == "Yes", estado))
    
    conn.commit()
    cursor.close()
    conn.close()

# Función para confirmar el envío
def confirm_shipment():
    product_id = entry_product_id.get()
    total_quantity = entry_total_quantity.get()
    package_quantity = entry_package_quantity.get()
    label_confirmed = label_check_var.get()
    box_fit = box_fit_var.get()
    
    # Validar que el producto exista en la "base de datos"
    if product_id not in expected_products:
        messagebox.showerror("Error", "Product not found in the system.")
        return

    # Verificar y calcular cantidad total y paquetes/unidades por paquete
    try:
        provided_quantity_total = int(total_quantity)
    except ValueError:
        messagebox.showerror("Error", "Total amount entered is not valid.")
        return

    try:
        packages, units_per_package = map(int, package_quantity.split('/'))
        calculated_quantity = packages * units_per_package
    except ValueError:
        messagebox.showerror("Error", "Invalid package/unit format. Use 'packages/units' format' (e.g., 8/3).")
        return
    
    # Verificar si ambas cantidades coinciden y cumplen la cantidad esperada
    expected_quantity = expected_products[product_id]
    if provided_quantity_total == calculated_quantity == expected_quantity and label_confirmed == 1 and box_fit == "Yes":
        save_to_database(product_id, provided_quantity_total, label_confirmed, box_fit)
        messagebox.showinfo("Confirmation successful", "The order has been verified and is ready for shipping.")
        # Mensaje de agradecimiento
        messagebox.showinfo("Thank you", "Thank you for the review and confirming the process.")
    else:
        errors = []
        if provided_quantity_total != expected_quantity or calculated_quantity != expected_quantity:
            errors.append(f" -The amounts entered do not match the expected amount ({expected_quantity} units).")
        if label_confirmed != 1:
            errors.append(" - The labeling process has not been confirmed.")
        if box_fit != "Yes":
            errors.append(" - The quantities do not fit the box size.")
        
        messagebox.showerror("Error en la confirmación", "\n".join(errors))
        save_to_database(product_id, provided_quantity_total, 0, box_fit)

# Configuración de la ventana principal
window = tk.Tk()
window.title("Shipping Confirmation")
window.geometry("450x400")
window.configure(bg="#f0f0f0")

# Estilos de fuente
label_font = ("Arial", 12)
entry_font = ("Arial", 11)
button_font = ("Arial", 12, "bold")

# Etiqueta e ingreso de ID del producto
tk.Label(window, text="Product ID:", font=label_font, bg="#f0f0f0").pack(pady=(15, 5))
entry_product_id = tk.Entry(window, font=entry_font, width=30, bd=2)
entry_product_id.pack(pady=5)

# Etiqueta e ingreso de cantidad total
tk.Label(window, text="Total number of units:", font=label_font, bg="#f0f0f0").pack(pady=(15, 5))
entry_total_quantity = tk.Entry(window, font=entry_font, width=30, bd=2)
entry_total_quantity.pack(pady=5)

# Etiqueta e ingreso de cantidad en formato "paquetes/unidades por paquete"
tk.Label(window, text="Enter in packages/units per package format (e.g., 8/3):", font=label_font, bg="#f0f0f0").pack(pady=(15, 5))
entry_package_quantity = tk.Entry(window, font=entry_font, width=30, bd=2)
entry_package_quantity.pack(pady=5)

# Checkbox para confirmar etiquetado
label_check_var = tk.IntVar()
label_checkbox = tk.Checkbutton(window, text="The labeling process is verified", font=label_font, variable=label_check_var, bg="#f0f0f0")
label_checkbox.pack(pady=15)

# Pregunta sobre el ajuste al tamaño de la caja
tk.Label(window, text="Do the items fit the box size?", font=label_font, bg="#f0f0f0").pack(pady=(10, 5))
box_fit_var = tk.StringVar()
box_fit_var.set("No")  # Valor predeterminado
box_fit_yes = tk.Radiobutton(window, text="Yes", variable=box_fit_var, value="Yes", font=label_font, bg="#f0f0f0")
box_fit_no = tk.Radiobutton(window, text="No", variable=box_fit_var, value="No", font=label_font, bg="#f0f0f0")
box_fit_yes.pack()
box_fit_no.pack()

# Botón de confirmación
confirm_button = tk.Button(window, text="Confirm Shipping", font=button_font, bg="#4CAF50", fg="white", command=confirm_shipment, width=15)
confirm_button.pack(pady=(10, 20))

# Ejecutar la ventana principal
window.mainloop()

