# 🇻🇪 Datil Retail: Inteligencia Operativa y Financiera

**Autor:** Lic. Albert Guacaran  
*Inteligencia de Negocios para la Toma Rápida de Decisiones*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B) ![Status](https://img.shields.io/badge/Status-Active-success)

---

## 🚀 Visión del Proyecto

**Datil Retail Intelligence** es una solución de Business Intelligence diseñada para transformar datos operativos complejos en decisiones ejecutivas inmediatas. 

A diferencia de los tableros tradicionales, este sistema no solo "muestra datos", sino que **sugiere acciones concretas** para optimizar el inventario y proteger el flujo de caja.

## 🧠 Módulos Clave

### 1. 📊 Análisis Pareto 80/20 (Nivel Pro)
Identificación matemática de los activos vitales de la empresa.
*   **Curva de Lorenz Dual:** Visualización del valor acumulado.
*   **Segmentación ABC:** Detecta el 20% de SKUs que generan el 80% del valor.

### 2. 📦 Gestión de Compras Inteligente
Motor de reabastecimiento que automatiza la decisión de compra.
*   **Detección de Quiebres:** Alertas automáticas cuando `Stock Actual < Stock Mínimo`.
*   **Planificación Financiera:** Desglose de inversión requerida en **Moneda Nacional 🇻🇪** vs **Divisas (Importado) 🌎**.
*   **Agrupación por Proveedor:** Genera órdenes de compra listas para enviar.

### 3. 📍 Mapa Operativo
Geolocalización en tiempo real del rendimiento de ventas por sede a nivel nacional.

### 4. 🛡️ Modo Offline "Zero-Downtime"
Arquitectura robusta que garantiza la disponibilidad del sistema. Si la conexión a la base de datos falla, el sistema genera automáticamente una simulación estadística en memoria para permitir la continuidad operativa y demostraciones sin interrupciones.

---

## 🛠️ Tecnologías Utilizadas

*   **Python**: Lógica de negocio y procesamiento de datos.
*   **Streamlit**: Framework para aplicaciones de datos interactivas.
*   **Pandas / NumPy**: Manipulación vectorial de grandes volúmenes de datos.
*   **Plotly**: Visualizaciones financieras interactivas.
*   **Firebase**: Backend de base de datos NoSQL (con fallback local).

## 💻 Instalación y Uso Local

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/albertguacaranguacaran-ops/ferre-analytics-pro.git
    cd ferre-analytics-pro
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la aplicación:**
    ```bash
    streamlit run app_datil.py
    ```

---
*Desarrollado con pasión por la eficiencia por albertguacaranguacaran-ops.*
