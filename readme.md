```markdown
# 🚀 Guía de instalación del proyecto Django

## 📦 Requisitos previos

- Python 3.8+
- PostgreSQL 12+
- Git
- pip

---

## 🧾 1. Clonar el repositorio

```bash
git clone https://github.com/DavidAcostaF/SistemaEscolar.git
cd tu-repo
```

---

## ⚙️ 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env`:

```env
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=usuario_postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
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

## ▶️ 7. Iniciar servidor

```bash
python manage.py runserver
```

Abrir en navegador: `http://localhost:8000`

---
```