---
description: Reglas y contexto global para los agentes que trabajen en el Sistema Bibliotecario PCA.
---

# Proyecto: Sistema Bibliotecario PCA

## Contexto
Este es un sistema web modular para gestionar la biblioteca del Politécnico de la Costa Atlántica (PCA). Permite la gestión de autores, estudiantes, libros y el historial de préstamos (activos y pendientes).

## Stack Tecnológico
- **Backend**: Python 3.13, FastAPI, SQLAlchemy 2.0, Pydantic v2.
- **Base de Datos**: MySQL 8.0 (desplegado vía Docker con el nombre `biblioteca_pca`).
- **Frontend**: React (Vite), React Router DOM, Bootstrap 5 (Sass, usando color institucional rojo `#D20B12`), Axios.
- **Despliegue**: Docker Compose (`docker-compose.yml`) orquestando `database`, `backend` y `frontend`.

## Reglas de Arquitectura y Desarrollo
1. **Backend**:
   - Mantener siempre la Arquitectura de 3 Capas: `routers` -> `services` -> `repositories`.
   - Utilizar "Soft Deletes" (bajas lógicas usando el campo `estado`) en lugar de `DELETE` físicos.
   - Las claves primarias (PK) son siempre `UUID`.
   - Los servicios contienen toda la lógica de negocio (ej. validación de stock al prestar o devolver).
2. **Frontend**:
   - Arquitectura modular basada en funcionalidades (Feature-Driven).
   - Componentes transversales (`Pagination`, `ConfirmDialog`, `LoadingSpinner`, `ToastContainer`) deben reutilizarse.
   - Usar `Suspense` y `lazy()` para el enrutamiento.
   - **Prohibido usar TailwindCSS**. Se debe emplear Bootstrap y sobrescribir variables en `src/assets/scss/custom.scss`.
3. **Base de Datos**:
   - Control estricto de restricciones relacionales (no eliminar autores con libros prestados, no inhabilitar estudiantes con préstamos pendientes).

## Instrucciones de Comportamiento del Agente
- Verifica siempre el archivo `walkthrough.md` y `implementation_plan.md` si necesitas conocer el progreso o las decisiones previas.
- Cuando agregues nuevas librerías, asegúrate de actualizar `requirements.txt` o `package.json` y ten en cuenta la reconstrucción de los contenedores Docker si es necesario.
