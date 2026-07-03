from pymongo import MongoClient
from pymongo.errors import PyMongoError

def conectar():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        db = client['ArenaMatch']
        print("\n✓ Conexion exitosa a MongoDB - ArenaMatch")
        return db
    except PyMongoError as e:
        print(f"\n✗ Error de conexion: {e}")
        exit(1)

def pedir_float(mensaje):
    valor = input(mensaje)
    try:
        return float(valor)
    except ValueError:
        print(f"✗ Error: '{valor}' no es un numero valido")
        return None

def crear_documento(db):
    print("\n--- CREAR DOCUMENTO ---")
    print("1. Torneo")
    print("2. Usuario")
    print("3. Equipo")
    coleccion = input("Seleccione coleccion: ")
    if coleccion == "1":
        nombre = input("Nombre del torneo: ")
        videojuego = input("Videojuego: ")
        fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
        fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
        estado = input("Estado (Planificacion/Inscripciones Abiertas/En Curso/Finalizado): ")
        if not nombre.strip() or not videojuego.strip() or not fecha_inicio.strip() or not fecha_fin.strip() or not estado.strip():
            print("✗ Error: los campos no pueden estar vacios")
            return
        prize_pool = pedir_float("Prize pool ($): ")
        if prize_pool is None:
            return
        costo = pedir_float("Costo inscripcion ($): ")
        if costo is None:
            return
        doc = {
            "nombre": nombre,
            "videojuego": videojuego,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "prize_pool": prize_pool,
            "costo_inscripcion": costo,
            "estado": estado,
            "equipos_inscritos": []
        }
        resultado = db.torneos.insert_one(doc)
        print(f"✓ Torneo creado con ID: {resultado.inserted_id}")
    elif coleccion == "2":
        nombre = input("Nombre del usuario: ")
        email = input("Email: ")
        rol = input("Rol (Administrador/Jugador/Arbitro/Patrocinador): ")
        if not nombre.strip() or not email.strip() or not rol.strip():
            print("✗ Error: los campos no pueden estar vacios")
            return
        doc = {
            "nombre": nombre,
            "email": email,
            "rol": rol,
            "fecha_registro": "2026-06-01",
            "activo": True
        }
        resultado = db.usuarios.insert_one(doc)
        print(f"✓ Usuario creado con ID: {resultado.inserted_id}")
    elif coleccion == "3":
        nombre = input("Nombre del equipo: ")
        logo = input("Logo URL: ")
        if not nombre.strip():
            print("✗ Error: el nombre no puede estar vacio")
            return
        doc = {
            "nombre": nombre,
            "logo_url": logo,
            "fecha_creacion": "2026-06-01",
            "jugadores": [],
            "torneos_participados": []
        }
        resultado = db.equipos.insert_one(doc)
        print(f"✓ Equipo creado con ID: {resultado.inserted_id}")
    else:
        print("✗ Opcion no valida")

def consultar_documentos(db):
    print("\n--- CONSULTAR DOCUMENTOS ---")
    print("1. Todos los torneos")
    print("2. Torneos por estado")
    print("3. Todos los usuarios")
    print("4. Usuarios por rol")
    print("5. Todas las inscripciones")
    print("6. Todos los equipos")
    opcion = input("Seleccione opcion: ")
    if opcion == "1":
        docs = db.torneos.find()
        for d in docs:
            print(f"\n  Torneo: {d['nombre']} | Videojuego: {d['videojuego']} | Estado: {d['estado']} | Prize Pool: ${d['prize_pool']}")
    elif opcion == "2":
        estado = input("Estado a buscar: ")
        docs = db.torneos.find({"estado": estado})
        for d in docs:
            print(f"\n  Torneo: {d['nombre']} | Videojuego: {d['videojuego']} | Prize Pool: ${d['prize_pool']}")
    elif opcion == "3":
        docs = db.usuarios.find()
        for d in docs:
            print(f"\n  Usuario: {d['nombre']} | Email: {d['email']} | Rol: {d['rol']}")
    elif opcion == "4":
        rol = input("Rol a buscar: ")
        docs = db.usuarios.find({"rol": rol})
        for d in docs:
            print(f"\n  Usuario: {d['nombre']} | Email: {d['email']}")
    elif opcion == "5":
        docs = db.inscripciones.find()
        for d in docs:
            print(f"\n  Torneo: {d['torneo']} | Equipo: {d['equipo']} | Estado: {d['estado']} | Monto: ${d['monto_pagado']}")
    elif opcion == "6":
        docs = db.equipos.find()
        for d in docs:
            print(f"\n  Equipo: {d['nombre']} | Logo: {d['logo_url']}")
    else:
        print("✗ Opcion no valida")

def actualizar_documento(db):
    print("\n--- ACTUALIZAR DOCUMENTO ---")
    print("1. Actualizar estado de torneo")
    print("2. Actualizar estado de inscripcion")
    print("3. Actualizar prize pool de torneo")
    opcion = input("Seleccione opcion: ")
    if opcion == "1":
        nombre = input("Nombre del torneo: ")
        nuevo_estado = input("Nuevo estado: ")
        resultado = db.torneos.update_one(
            {"nombre": nombre},
            {"$set": {"estado": nuevo_estado}}
        )
        if resultado.modified_count > 0:
            print(f"✓ Torneo actualizado correctamente")
        else:
            print("✗ No se encontro el torneo")
    elif opcion == "2":
        equipo = input("Nombre del equipo: ")
        nuevo_estado = input("Nuevo estado (Pagado/Pendiente/Rechazado): ")
        resultado = db.inscripciones.update_one(
            {"equipo": equipo},
            {"$set": {"estado": nuevo_estado}}
        )
        if resultado.modified_count > 0:
            print(f"✓ Inscripcion actualizada correctamente")
        else:
            print("✗ No se encontro la inscripcion")
    elif opcion == "3":
        nombre = input("Nombre del torneo: ")
        if not nombre.strip():
            print("✗ Error: el nombre no puede estar vacio")
            return
        nuevo_prize = pedir_float("Nuevo prize pool ($): ")
        if nuevo_prize is None:
            return
        resultado = db.torneos.update_one(
            {"nombre": nombre},
            {"$set": {"prize_pool": nuevo_prize}}
        )
        if resultado.modified_count > 0:
            print(f"✓ Prize pool actualizado correctamente")
        else:
            print("✗ No se encontro el torneo")
    else:
        print("✗ Opcion no valida")

def eliminar_documento(db):
    print("\n--- ELIMINAR DOCUMENTO ---")
    print("1. Eliminar torneo")
    print("2. Eliminar usuario")
    print("3. Eliminar equipo")
    opcion = input("Seleccione opcion: ")
    if opcion == "1":
        nombre = input("Nombre del torneo a eliminar: ")
        resultado = db.torneos.delete_one({"nombre": nombre})
        if resultado.deleted_count > 0:
            print(f"✓ Torneo eliminado correctamente")
        else:
            print("✗ No se encontro el torneo")
    elif opcion == "2":
        email = input("Email del usuario a eliminar: ")
        resultado = db.usuarios.delete_one({"email": email})
        if resultado.deleted_count > 0:
            print(f"✓ Usuario eliminado correctamente")
        else:
            print("✗ No se encontro el usuario")
    elif opcion == "3":
        nombre = input("Nombre del equipo a eliminar: ")
        resultado = db.equipos.delete_one({"nombre": nombre})
        if resultado.deleted_count > 0:
            print(f"✓ Equipo eliminado correctamente")
        else:
            print("✗ No se encontro el equipo")
    else:
        print("✗ Opcion no valida")

def agregacion_estadisticas(db):
    print("\n--- AGREGACION: ESTADISTICAS ---")
    resultado = db.torneos.aggregate([
        {"$group": {
            "_id": "$videojuego",
            "total_torneos": {"$sum": 1},
            "prize_pool_promedio": {"$avg": "$prize_pool"},
            "prize_pool_total": {"$sum": "$prize_pool"}
        }},
        {"$sort": {"prize_pool_total": -1}}
    ])
    print("\n  Estadisticas por videojuego:")
    for r in resultado:
        print(f"\n  Videojuego: {r['_id']}")
        print(f"  Total torneos: {r['total_torneos']}")
        print(f"  Prize pool promedio: ${r['prize_pool_promedio']:.2f}")
        print(f"  Prize pool total: ${r['prize_pool_total']:.2f}")

def agregacion_conteo(db):
    print("\n--- AGREGACION: CONTEO Y TOTALES ---")
    print("1. Inscripciones por estado")
    print("2. Usuarios por rol")
    print("3. Torneos por videojuego")
    opcion = input("Seleccione opcion: ")
    if opcion == "1":
        resultado = db.inscripciones.aggregate([
            {"$group": {"_id": "$estado", "total": {"$sum": 1}}}
        ])
        print("\n  Inscripciones por estado:")
        for r in resultado:
            print(f"  {r['_id']}: {r['total']}")
    elif opcion == "2":
        resultado = db.usuarios.aggregate([
            {"$group": {"_id": "$rol", "total": {"$sum": 1}}}
        ])
        print("\n  Usuarios por rol:")
        for r in resultado:
            print(f"  {r['_id']}: {r['total']}")
    elif opcion == "3":
        resultado = db.torneos.aggregate([
            {"$group": {"_id": "$videojuego", "total": {"$sum": 1}}}
        ])
        print("\n  Torneos por videojuego:")
        for r in resultado:
            print(f"  {r['_id']}: {r['total']}")
    else:
        print("✗ Opcion no valida")

def menu():
    print("\n╔══════════════════════════════════════╗")
    print("║       ARENA-MATCH - CLI MongoDB      ║")
    print("╠══════════════════════════════════════╣")
    print("║  1. Crear documento                  ║")
    print("║  2. Consultar documentos             ║")
    print("║  3. Actualizar documento             ║")
    print("║  4. Eliminar documento               ║")
    print("║  5. Agregacion: estadisticas         ║")
    print("║  6. Agregacion: conteo y totales     ║")
    print("║  0. Salir                            ║")
    print("╚══════════════════════════════════════╝")

def main():
    db = conectar()
    while True:
        menu()
        opcion = input("\nSeleccione una opcion: ")
        if opcion == "1":
            crear_documento(db)
        elif opcion == "2":
            consultar_documentos(db)
        elif opcion == "3":
            actualizar_documento(db)
        elif opcion == "4":
            eliminar_documento(db)
        elif opcion == "5":
            agregacion_estadisticas(db)
        elif opcion == "6":
            agregacion_conteo(db)
        elif opcion == "0":
            print("\n✓ Saliendo de Arena-Match CLI. Hasta luego!")
            break
        else:
            print("\n✗ Opcion no valida, intente de nuevo")

if __name__ == "__main__":
    main()