#  Arena-Match — Plataforma de Torneos de E-Sports

Proyecto Integrador - Base de Datos II (ITIZ2201)  
Universidad de Las Américas, Quito - Ecuador  
**Autores:** Jose Jauregui, Estéfano López, Inti Matute

---

##  Descripción

Arena-Match es una plataforma web para la gestión de torneos de deportes electrónicos (E-Sports) a nivel latinoamericano. Permite gestionar usuarios, equipos, torneos e inscripciones mediante una interfaz web conectada a SQL Server.

##  Tecnologías

- **Backend:** Python 3.14 + Flask 3.1.3
- **Base de Datos:** Microsoft SQL Server
- **Conexión BD:** pyodbc 5.3.0
- **Frontend:** HTML5 + CSS3 + Jinja2

##  Estructura del Proyecto
ArenaMatch/
├── app.py                  # Backend principal (Flask)
├── README.md               # Documentación del proyecto
├── templates/              # Plantillas HTML (Jinja2)
│   ├── base.html           # Plantilla base con navegación
│   ├── index.html          # Dashboard principal
│   ├── usuarios.html       # Gestión de usuarios
│   ├── equipos.html        # Gestión de equipos
│   ├── torneos.html        # Gestión de torneos
│   └── inscripciones.html  # Gestión de inscripciones
└── static/
└── css/
└── style.css       # Estilos CSS personalizados
##  Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/intimatute06/ArenaMatch.git
cd ArenaMatch
```

### 2. Instalar dependencias
```bash
pip install flask pyodbc
```

### 3. Configurar la base de datos
- Abrir SQL Server Management Studio
- Ejecutar el script SQL de creación de la base de datos ArenaMatch

### 4. Ejecutar la aplicación
```bash
python app.py
```

### 5. Abrir en el navegador
http://127.0.0.1:5000

## Funcionalidades

-  Gestión de Usuarios (Administrador, Jugador, Árbitro, Patrocinador)
-  Gestión de Equipos
-  Gestión de Torneos (League of Legends, Valorant, EA Sports FC)
-  Gestión de Inscripciones
-  Operaciones CRUD completas
-  Interfaz dark mode temática E-Sports

##  Base de Datos

El sistema utiliza Microsoft SQL Server con las siguientes tablas:
- **Usuario** — Perfiles y roles de los participantes
- **Equipo** — Equipos registrados en la plataforma
- **Jugador** — Jugadores asociados a equipos
- **Torneo** — Torneos con sus configuraciones
- **Inscripcion** — Registro de equipos en torneos
- **Partida** — Enfrentamientos programados