import requests

# * Configuración de la API de Notion
database_url = "https://api.notion.com/v1/databases/{base_de_datos}/query"
headers = {
    "Authorization": "token_de_autorización",
    "Notion-Version": "2022-06-28",
}


def main():
    filtro = input("Ingrese el nombre, marca o ID del producto que busca: ")
    productos = obtener_productos(filtro)

    if productos:
        producto_seleccionado = mostrar_productos(productos)
        cambiar_cantidad_o_precio(producto_seleccionado)
    else:
        print("No se encontraron productos que coincidan con el filtro.")


# * Obtener productos filtrados por nombre, marca o ID
def obtener_productos(filtro):
    params = {
        "filter": {
            "property": "Nombre",
            "text": {"contains": filtro},
        }
    }

    response = requests.post(database_url, headers=headers, json=params)
    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error al obtener productos: {response.status_code} - {response.text}")
        return None


# * Mostrar productos al usuario y permitir selección
def mostrar_productos(productos):
    for idx, producto in enumerate(productos):
        print(f"Producto {idx + 1}:")
        print(f"Nombre: {producto['Nombre']}")
        print(f"Marca: {producto['Marca']}")
        print(f"Descripción: {producto['Descripción']}")
        print(f"ID: {producto['ID']}")
        print(f"Precio por unidad: {producto['Precio']} MXN")
        print(f"Disponibilidad: {producto['Disponibilidad']}")
        print()

    seleccion = (
        int(input("Seleccione el número de producto que desea (1, 2, ...): ")) - 1
    )
    return productos[seleccion]


# * Cambiar cantidad a precio y precio a cantidad
def cambiar_cantidad_o_precio(producto):
    opcion = input(
        "¿Desea convertir de cantidad a precio (C) o de precio a cantidad (P)? "
    ).upper()

    if opcion == "C":
        precio_unitario = producto["Precio"]
        cantidad_actual = float(input("Ingrese la cantidad deseada de unidades: "))
        nuevo_precio = cantidad_actual * precio_unitario
        print(f"El precio por {cantidad_actual} unidad es: {nuevo_precio} MXN")

    elif opcion == "P":
        precio_unitario = float(input("Ingrese el precio disponible a gastar: "))
        cantidad_actual = producto["Cantidad"]
        cantidad_nueva = producto["Cantidad"] * precio_unitario
        nuevo_cantidad = cantidad_actual * precio_unitario
        print(f"La cantidad de {cantidad_nueva} unidades cuesta: {nuevo_cantidad} MXN")

    else:
        print("Opción no válida. Inténtelo de nuevo.")
        cambiar_cantidad_o_precio(producto)


if __name__ == "__main__":
    main()
