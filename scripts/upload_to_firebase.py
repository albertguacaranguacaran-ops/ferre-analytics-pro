import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from faker import Faker
import os


path_to_json = os.path.join(os.path.dirname(__file__), '..', 'firebase_credentials.json')

if not firebase_admin._apps:
    cred = credentials.Certificate(path_to_json)
    firebase_admin.initialize_app(cred)

db = firestore.client()
fake = Faker()

def seed_datil_retail():
    print("🚀 Iniciando carga masiva para Ferre-Analytics-Datil...")

    print("📍 Creando 24 sedes a nivel nacional...")
    regiones = ['Central', 'Capital', 'Occidente', 'Oriente', 'Andes', 'Guayana']
    for i in range(1, 25):
        sede_id = f"DATIL-SEDE-{i:02d}"
        db.collection('sedes').document(sede_id).set({
            'nombre': f"Ferretería Datil - Sede {i:02d}",
            'region': np.random.choice(regiones),
            'capacidad_almacen': np.random.randint(5000, 20000),
            'estatus': 'Activa'
        })


    print("📦 Generando 10,000 SKUs de ferretería...")
    categorias = ['Herramientas Eléctricas', 'Construcción', 'Pinturas', 'Plomería', 'Electricidad']
    
    batch = db.batch()
    for i in range(1, 10001):
        sku = f"DAT-FERR-{10000 + i}"
        origen = np.random.choice(['Importado', 'Nacional'], p=[0.4, 0.6])
   
        if origen == 'Importado':
            costo = round(np.random.uniform(25, 600), 2)
            lead_time = np.random.randint(45, 120) 
        else:
            costo = round(np.random.uniform(5, 150), 2)
            lead_time = np.random.randint(2, 15)
            
        doc_ref = db.collection('productos').document(sku)
        batch.set(doc_ref, {
            'sku': sku,
            'descripcion': f"{fake.word().upper()} {fake.word().upper()} PROFESIONAL",
            'categoria': np.random.choice(categorias),
            'origen': origen,
            'costo_usd': costo,
            'precio_venta': round(costo * 1.35, 2), # Margen del 35%
            'stock_minimo': np.random.randint(10, 100),
            'lead_time_days': lead_time
        })

        if i % 500 == 0:
            batch.commit()
            batch = db.batch()
            print(f"✅ {i} productos cargados exitosamente...")

    print("\n¡PROCESO COMPLETADO! 🎊")
    print("La base de datos de Ferre-Analytics-Datil está lista en la nube.")

if __name__ == "__main__":
    seed_datil_retail()
