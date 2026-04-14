# 🏫 Sistema Escolar — Backend API REST

> API REST desarrollada con **Django + Django REST Framework** que sirve como backend del Sistema Escolar. Gestiona autenticación, usuarios (alumnos, maestros, administradores) y eventos escolares.

🔗 **Frontend:** [https://sistema-escolar-iota.vercel.app](https://sistema-escolar-iota.vercel.app/registro-usuarios)

---

## 📋 Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación y Configuración](#instalación-y-configuración)
- [Configuración de Base de Datos](#configuración-de-base-de-datos)
- [Variables de Entorno](#variables-de-entorno)
- [Endpoints Principales](#endpoints-principales)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Despliegue](#despliegue)

---

## 📖 Descripción General

Este backend expone una API REST que alimenta la plataforma de gestión escolar. Sus responsabilidades principales son:

- Registro y autenticación de usuarios por rol (Alumno, Maestro, Administrador).
- CRUD de alumnos y maestros.
- CRUD de eventos escolares.
- Utilidades de cifrado para protección de datos sensibles.
- Conexión con base de datos **MySQL**.

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|------------|-----|
| [Python 3](https://www.python.org/) | Lenguaje principal |
| [Django](https://www.djangoproject.com/) | Framework web |
| [Django REST Framework](https://www.django-rest-framework.org/) | Construcción de la API REST |
| [MySQL](https://www.mysql.com/) | Base de datos relacional |
| [Google App Engine](https://cloud.google.com/appengine) | Plataforma de despliegue |

---

## ✅ Requisitos Previos

- Python `>=3.9`
- pip
- MySQL `>=8.0`
- Cuenta en Google Cloud (para despliegue)

---

## 🚀 Instalación y Configuración

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu-usuario/sistema-escolar-backend.git
cd sistema-escolar-backend
```

2. **Crea y activa un entorno virtual:**

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Configura la base de datos** (ver sección siguiente).

5. **Aplica las migraciones:**

```bash
python manage.py migrate
```

6. **Inicia el servidor de desarrollo:**

```bash
python manage.py runserver
```

La API estará disponible en: [http://localhost:8000/](http://localhost:8000/)

---

## 🗄️ Configuración de Base de Datos

El proyecto usa **MySQL**. Configura tu conexión en el archivo `my.cnf`:

```ini
[client]
database = nombre_de_tu_base_de_datos
host     = localhost
user     = tu_usuario
password = tu_contraseña
port     = 3306
```

Asegúrate de que la base de datos exista antes de correr las migraciones:

```sql
CREATE DATABASE sistema_escolar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## 🔐 Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables (o configúralas directamente en `settings.py` para desarrollo local):

```env
SECRET_KEY=tu_clave_secreta_de_django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=sistema_escolar
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

> ⚠️ **Nunca subas** el archivo `.env` ni `my.cnf` con credenciales reales al repositorio.

---

## 📡 Endpoints Principales

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/registro/` | Registro de nuevo usuario |
| `POST` | `/api/login/` | Inicio de sesión |
| `GET` | `/api/alumnos/` | Listar todos los alumnos |
| `POST` | `/api/alumnos/` | Crear alumno |
| `PUT` | `/api/alumnos/<id>/` | Editar alumno |
| `DELETE` | `/api/alumnos/<id>/` | Eliminar alumno |
| `GET` | `/api/maestros/` | Listar todos los maestros |
| `POST` | `/api/maestros/` | Crear maestro |
| `PUT` | `/api/maestros/<id>/` | Editar maestro |
| `DELETE` | `/api/maestros/<id>/` | Eliminar maestro |
| `GET` | `/api/admins/` | Listar administradores |

### Eventos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/eventos/` | Listar todos los eventos |
| `POST` | `/api/eventos/` | Crear evento |
| `PUT` | `/api/eventos/<id>/` | Editar evento |
| `DELETE` | `/api/eventos/<id>/` | Eliminar evento |
| `GET` | `/api/eventos/total/` | Total de eventos registrados |

---

## 📁 Estructura del Proyecto

```
sistema-escolar-backend/
├── migrations/          # Migraciones de la base de datos
├── puentes/             # Módulo de conexión entre alumnos y maestros
├── views/               # Vistas y lógica de cada endpoint
├── static/              # Archivos estáticos
├── admin.py             # Configuración del panel de administración de Django
├── cypher_utils.py      # Utilidades de cifrado de datos sensibles
├── data_utils.py        # Utilidades de manipulación de datos
├── models.py            # Modelos de la base de datos (Alumno, Maestro, Evento, etc.)
├── serializers.py       # Serializers de Django REST Framework
├── settings.py          # Configuración general de Django
├── urls.py              # Definición de rutas de la API
├── utils.py             # Funciones de utilidad generales
├── wsgi.py              # Punto de entrada WSGI
├── main.py              # Punto de entrada principal
├── manage.py            # CLI de Django
├── app.yaml             # Configuración para Google App Engine
├── deploy.sh            # Script de despliegue automatizado
├── my.cnf               # Configuración de conexión a MySQL 
├── requirements.txt     # Dependencias del proyecto
└── .gitignore
```

---

## ☁️ Despliegue

El proyecto está configurado para desplegarse en **Google App Engine**.

### Despliegue manual

1. Asegúrate de tener instalado y configurado el [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
2. Autentica tu cuenta:

```bash
gcloud auth login
gcloud config set project TU_PROJECT_ID
```

3. Ejecuta el script de despliegue:

```bash
bash deploy.sh
```

O directamente con el CLI de GCP:

```bash
gcloud app deploy app.yaml
```

---

## 📦 Dependencias

Las dependencias del proyecto se encuentran en `requirements.txt`. Para generarlas o actualizarlas:

```bash
pip freeze > requirements.txt
```

---

> Desarrollado con 🐍 Python + Django REST Framework · Desplegado en Google App Engine
