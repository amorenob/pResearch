# Scraping de MercadoLibre: Ítems Más Vendidos

Este proyecto utiliza el framework **Scrapy** para extraer información sobre los ítems "más vendidos" de categorías específicas en MercadoLibre Colombia. El objetivo principal es identificar productos con alta demanda y obtener datos relevantes para análisis de mercado, seguimiento de ventas, o investigación de productos.

---

## 🚀 Tecnologías Utilizadas

* **Python 3.x**
* **Scrapy**: El framework de código abierto y colaboración rápida para web scraping en Python.
* **Pipenv (recomendado)**: Para gestionar las dependencias del proyecto de forma aislada y reproducible.

---

## ✨ Características

* **Enfoque en "Más Vendidos"**: El spider está diseñado para navegar a URLs que contienen el identificador `_BestSellers_YES`, lo que sugiere un enfoque en la extracción de productos con altas ventas.
* **Extracción de Datos Clave**: Por cada ítem, se recolectan los siguientes datos:
    * **SKU**: Identificador único del producto.
    * **Nombre**: Título del producto.
    * **Precio**: Precio del producto.
    * **Cantidad Vendida**: Número de unidades vendidas (extraído del texto "X vendidos").
    * **Ubicación**: Información de la ubicación del vendedor (si disponible en el texto de venta).
    * **Enlace del Producto**: URL directa al detalle del producto.
    * **Categoría/Subcategoría (`sub`)**: Parte de la URL que indica la subcategoría del producto.
* **Paginación Automática**: El spider sigue automáticamente los enlaces de paginación (`Siguiente`) para raspar múltiples páginas de resultados.
* **Filtro Inicial de URLs**: Actualmente, el spider comienza con una URL específica de celulares Huawei, pero está estructurado para permitir la adición de otras categorías.

---
Descargo de Responsabilidad

Este proyecto tiene únicamente fines educativos. No está diseñado para su uso en producción y no debe emplearse para realizar scraping de sitios web sin el permiso correspondiente. Siempre revisa los términos de servicio de los sitios web de los que extraigas información.
