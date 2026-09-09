# Sistema Bibliotecario PCA

Sistema web modular para la gestión de la biblioteca del **Politécnico de la Costa Atlántica (PCA)**. Permite administrar autores, estudiantes, libros y el ciclo de vida completo de los préstamos.

---

## Stack Tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| **Backend** | Python | 3.13 |
| | FastAPI | 0.141.1 |
| | SQLAlchemy | 2.0.52 |
| | Pydantic v2 | 2.13.5 |
| | Uvicorn | 0.52.4 |
| | PyMySQL | 1.2.0 |
| **Frontend** | React | 19.2.8 |
| | Vite | 8.2.2 |
| | Bootstrap | 5.3.8 |
| | Sass | 1.104.0 |
| | Axios | 1.20.0 |
| | React Router DOM | 7.18.3 |
| **Base de Datos** | MySQL | 8.0 |
| **Infraestructura** | Docker / Docker Compose | — |

---

## Arquitectura

```
┌─────────────────┐        ┌─────────────────────────────────┐
│   Frontend      │        │           Backend               │
│  React + Vite   │◄──────►│         FastAPI                 │
│  Feature-Driven │  HTTP  │   Arquitectura 3 Capas          │
│  Lazy Loading   │        │  Routers → Services → Repos     │
└─────────────────┘        └──────────────┬──────────────────┘
                                          │ SQLAlchemy ORM
                                          ▼
                                  ┌───────────────┐
                                  │   MySQL 8.0   │
                                  │  biblioteca   │
                                  │     _pca      │
                                  └───────────────┘
```

### Backend — 3 Capas

- **Routers** (`/api/v1/`): Reciben peticiones HTTP, validan con Pydantic, retornan respuestas. Sin lógica de negocio.
- **Services**: Concentran toda la lógica de negocio (validación de stock, restricciones de baja, unicidad de datos).
- **Repositories**: Única capa autorizada para interactuar con la base de datos vía SQLAlchemy.

### Frontend — Feature-Driven

Módulos autónomos por funcionalidad. Componentes transversales compartidos (`Pagination`, `ConfirmDialog`, `LoadingSpinner`, `ToastContainer`). Enrutamiento con `React Router DOM` y carga diferida (`lazy` + `Suspense`).

### Lógica de Negocio Clave

- **Soft Deletes**: Todos los registros se deshabilitan lógicamente (`estado = false`), nunca se eliminan físicamente.
- **Control de stock**: Al crear un préstamo, `cantidad_disponible` del libro se decrementa en 1. Al registrar la devolución, se incrementa.
- **Restricciones de integridad**:
  - Un autor no puede eliminarse si tiene libros con préstamos activos.
  - Un estudiante no puede inhabilitarse si tiene préstamos pendientes.
  - Un libro no puede eliminarse si tiene préstamos activos.
- **PKs como UUID**: Todas las claves primarias son `CHAR(36)` generados desde el backend.

---

## Módulos del Sistema

| Módulo | Ruta Frontend | Endpoints Backend |
|--------|--------------|------------------|
| Dashboard | `/dashboard` | `GET /api/v1/dashboard/metrics` |
| Autores | `/authors` | `GET/POST /api/v1/autores`, `GET/PUT/DELETE /api/v1/autores/{id}` |
| Estudiantes | `/students` | `GET/POST /api/v1/estudiantes`, `GET/PUT/DELETE /api/v1/estudiantes/{id}` |
| Libros | `/books` | `GET/POST /api/v1/libros`, `GET/PUT/DELETE /api/v1/libros/{id}` |
| Préstamos | `/loans` | `GET /api/v1/prestamos/activos`, `GET /api/v1/prestamos/pendientes`, `POST /api/v1/prestamos`, `POST /api/v1/prestamos/{id}/devolucion` |

---

## Ejecutar el Proyecto

### Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y en ejecución.
- Git.

### 1. Clonar el repositorio

```bash
git clone https://github.com/AlssyLop/Sistema-Bibliotecario.git
cd Sistema-Bibliotecario
```

### 2. Levantar todos los servicios con Docker Compose

```bash
docker compose up -d
```

Esto construye y levanta automáticamente:
- `biblioteca_pca` — MySQL 8.0 en el puerto `3306` (inicializado con `database.sql`)
- `biblioteca_backend` — FastAPI en el puerto `8000`
- `biblioteca_frontend` — React (Nginx) en el puerto `80`

> La base de datos incluye **30 registros de prueba por entidad** insertados al iniciar.

### 3. Verificar que los servicios estén corriendo

```bash
docker compose ps
```

### 4. Acceder al sistema

| Servicio | URL |
|---------|-----|
| **Aplicación web** | http://localhost |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |

---

## Desarrollo Local (sin Docker)

### Backend

```bash
# Crear entorno virtual e instalar dependencias
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt

# Configurar variables de entorno
cp backend/.env.example backend/.env
# Editar backend/.env con los datos de tu MySQL local

# Iniciar el servidor
uvicorn backend.app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Disponible en http://localhost:5173
```

> **Nota**: Para desarrollo local, el frontend apunta a `http://localhost:8000/api/v1`. Asegúrate de que el backend esté corriendo antes de iniciar el frontend.

---

## Estructura del Repositorio

```
.
├── backend/
│   ├── app/
│   │   ├── core/           # Configuración y conexión a BD
│   │   ├── models/         # Entidades ORM (SQLAlchemy)
│   │   ├── schemas/        # DTOs y validación (Pydantic v2)
│   │   ├── repositories/   # Capa de acceso a datos
│   │   ├── services/       # Lógica de negocio
│   │   ├── routers/        # Controladores HTTP
│   │   └── main.py         # Entrada principal FastAPI
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── assets/scss/    # Estilos institucionales (Bootstrap + Sass)
│   │   ├── components/     # Componentes transversales compartidos
│   │   ├── layout/         # AppShell, Sidebar, Navbar
│   │   ├── modules/        # Módulos por funcionalidad
│   │   ├── routes/         # Enrutamiento con Lazy Loading
│   │   └── services/       # Interceptor Axios global
│   └── Dockerfile
├── database.sql            # Schema + 30 registros de prueba por entidad
├── docker-compose.yml      # Orquestación de servicios
├── requirements.txt        # Dependencias Python
└── AGENTS.md               # Contexto y reglas para agentes de IA
```
