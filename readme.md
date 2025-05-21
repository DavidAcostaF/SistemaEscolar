```markdown
# 🚀 Guía de instalación del Sistema Escolar (Django + PostgreSQL + Moodle Sync)

## 📦 Requisitos previos

- Python 3.10+
- PostgreSQL 12+
- Git
- pip
- Docker (opcional si vas a correr Moodle en contenedor)
- Moodle configurado y accesible (por API)

```

## 🧾 1. Clonar el repositorio

```bash
git clone https://github.com/DavidAcostaF/SistemaEscolar.git
cd SistemaEscolar
```

---

## ⚙️ 2. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita tu archivo `.env` para conectar correctamente a PostgreSQL y Moodle:

```env
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=usuario_postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# Moodle API
MOODLE_API_URL=http://localhost:8082/webservice/rest/server.php
MOODLE_TOKEN=tu_token_de_moodle
```

Crear base de datos en PostgreSQL:

```sql
CREATE DATABASE nombre_de_tu_base_de_datos;
```

---

## 🐍 3. Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

Incluye:

- Django
- requests
- psycopg2
- Pillow (para manejo de imágenes)

---

## 🛠️ 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧑‍💻 6. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

---

## 🔁 7. Ejecutar sincronización manual inicial (opcional)

Antes de programar tareas automáticas, puedes hacer una sincronización manual:

```bash
python manage.py sync_moodle
```

Esto sincroniza:
- Alumnos
- Materias (Cursos)
- Tareas
- Relación de tareas entregadas

---




## ▶️ 8. Iniciar servidor

```bash
python manage.py runserver
```

Abrir en navegador: [http://localhost:8000](http://localhost:8000)

---

## 📋 Notas adicionales

- Moodle debe permitir llamadas API REST (`webservice/rest/server.php`).
- El token debe tener permisos sobre funciones como:
  - `core_user_get_users`
  - `core_enrol_get_users_courses`
  - `gradereport_user_get_grade_items`
  - `mod_assign_get_assignments`
  - `mod_assign_get_grades`
  - `core_course_get_contents`
---

# 🎯 ¡Listo! Proyecto corriendo correctamente 🎯
