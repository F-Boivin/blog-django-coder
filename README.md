# Blog Coder — Proyecto final del curso de Python (Coderhouse)

Aplicación web tipo blog desarrollada con **Django**, proyecto integrador de los Módulos 11-13 del curso. Incluye publicaciones con búsqueda dinámica, registro y autenticación de usuarios, perfiles editables, sistema de permisos por grupos y panel de administración personalizado.

**Autor:** Felipe Boivin

## Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| 📝 **Publicaciones** | CRUD completo de posts con categorías, paginación y fechas |
| 🔍 **Búsqueda dinámica** | Filtro por texto (`icontains` en título y contenido, con `Q` objects) encadenado con filtro por categoría, vía GET |
| 👤 **Registro y autenticación** | Alta de usuarios con email, login y logout |
| 🪪 **Perfiles** | Cada usuario tiene un perfil (bio, ubicación, fecha de nacimiento) creado automáticamente por señal y editable desde "Mi perfil" |
| 🛡️ **Permisos por grupos** | Grupo **Moderadores** con permiso personalizado `puede_moderar`: pueden eliminar publicaciones de cualquier autor |
| ⚙️ **Admin personalizado** | `list_display`, `list_filter`, `search_fields`, `date_hierarchy`, acción masiva y perfil inline en el usuario |
| 📄 **Páginas estáticas** | "Acerca de" y "Contacto" (formulario con validación personalizada) |

## Stack

- Python 3.10+ · Django 5.x · SQLite · Bootstrap 5 (CDN)

## Instalación y configuración

```bash
# 1. Clonar el repositorio
git clone https://github.com/F-Boivin/blog-django-coder.git
cd blog-django-coder

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear las migraciones y aplicarlas
python manage.py makemigrations
python manage.py migrate

# 5. Crear el superusuario (será el autor de los datos de ejemplo)
python manage.py createsuperuser
#    Sugerido para evaluación: admin / Admin123!

# 6. Crear el grupo Moderadores con su permiso personalizado
python manage.py crear_grupos

# 7. Cargar datos de ejemplo (4 publicaciones)
python manage.py loaddata sample_data

# 8. Levantar el servidor
python manage.py runserver
# → http://127.0.0.1:8000/
```

> **Importante:** el paso 5 (superusuario) debe hacerse **antes** del paso 7, porque los posts de ejemplo referencian al usuario con id 1 como autor.

## Cómo probar cada funcionalidad

| Funcionalidad | Cómo probarla |
|---|---|
| Listado y búsqueda | En `/`, escribir "django" en el buscador → filtra por título/contenido. Combinar con una categoría → filtros encadenados |
| Registro | `/usuarios/registro/` → crear cuenta → redirige al login |
| Login / Logout | `/usuarios/login/` → al ingresar, el navbar muestra "Mi perfil" y "+ Nueva publicación" |
| Perfil editable | `/usuarios/perfil/` (requiere sesión) → editar bio/ubicación → "Perfil actualizado" |
| Crear post | "+ Nueva publicación" (requiere sesión). Validación: título de menos de 5 caracteres es rechazado |
| Editar post | Botón "Editar" — solo visible y permitido para el autor (403 para otros) |
| Moderación | En el admin, agregar un usuario al grupo **Moderadores** → ese usuario puede eliminar posts ajenos desde la web |
| Contacto | `/contacto/` → mensaje de menos de 10 caracteres es rechazado; uno válido muestra confirmación |
| Admin | `/admin/` con el superusuario → publicaciones con filtros/búsqueda/acción masiva; usuarios con perfil inline |

## Tests

```bash
python manage.py test
```

Cubren: validación de formularios (`PostForm`, `ContactForm`), listado público, búsqueda con `icontains` y filtros encadenados, control de acceso por login, permisos de moderación y la señal de creación de perfiles. **15 tests.**

## Arquitectura de permisos

| Nivel | Quién | Puede |
|---|---|---|
| Público | Cualquier visitante | Leer posts, buscar, ver "Acerca de", enviar contacto |
| Registrado | Usuario autenticado | Crear posts, editar/borrar los propios, editar su perfil |
| **Moderadores** | Grupo con permiso `posts.puede_moderar` | Además, eliminar publicaciones de **cualquier** autor |
| Staff | `is_staff` / superusuario | Panel de administración completo |

El grupo Moderadores se crea con `python manage.py crear_grupos` (idempotente) y se gestiona desde el admin (Usuarios → grupos). El permiso se define en `Post.Meta.permissions` y se aplica en `PostDeleteView.test_func()`.

## Estructura del proyecto

```
blog-django-coder/
├── manage.py / requirements.txt
├── blog_project/          # Configuración (settings con env-vars, urls, wsgi)
├── posts/                 # App principal
│   ├── models.py          # Post + permiso custom puede_moderar
│   ├── views.py           # CBV: listado con búsqueda GET, CRUD con mixins
│   ├── forms.py           # PostForm, BusquedaForm, ContactForm
│   ├── admin.py           # PostAdmin personalizado + acción masiva
│   ├── context_processors.py  # site_name y menú global
│   ├── templatetags/      # filtro 'resumen' + inclusion tag 'tarjeta_post'
│   ├── management/commands/crear_grupos.py
│   ├── fixtures/sample_data.json
│   └── tests.py
├── usuarios/              # Registro, login, Profile (señal) + inline en admin
└── templates/             # base.html (bloques title/content/scripts) + páginas
```

## Notas de despliegue

`settings.py` lee `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` y `DJANGO_ALLOWED_HOSTS` de variables de entorno (con defaults de desarrollo). Para producción:

```bash
export DJANGO_SECRET_KEY="<clave-segura-generada>"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="tudominio.pythonanywhere.com"
python manage.py collectstatic
```

El proyecto está pensado para desplegarse en PythonAnywhere (gratuito): clonar el repo, crear el venv, configurar la web app con el WSGI apuntando a `blog_project.settings` y mapear `/static/` a `staticfiles/`.
