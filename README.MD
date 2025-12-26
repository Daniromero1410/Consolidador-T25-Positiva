 Consolidador T25

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()
[![Status](https://img.shields.io/badge/Status-Production-success.svg)]()

Sistema ETL para consolidación y validación de datos de tarificación médica desarrollado para POSITIVA Compañía de Seguros.

## Descripción

Plataforma de procesamiento de datos que automatiza la consolidación de tarifas médicas de proveedores de salud en Colombia. El sistema descarga archivos Excel vía SFTP, valida datos mediante reglas semánticas y genera reportes de alertas categorizado por tipo de error.

Procesa diariamente más de 50 archivos con información contractual de servicios médicos, aplicando validaciones específicas del sector salud colombiano incluyendo códigos CUPS, tarifarios ISS/SOAT, y estructura organizacional de prestadores.

## Problemática y Solución

### Situación Anterior
- Procesamiento manual de archivos: 8+ horas diarias
- Tasa de error en validación: aproximadamente 50 errores por día
- Municipios colombianos confundidos con códigos de servicios médicos
- Pérdida de información de sedes por mapeo incorrecto
- Inconsistencias en formatos de proveedores

### Resultados Actuales
- Procesamiento automatizado: menos de 30 minutos
- Reducción de errores: 95%
- Validación semántica que diferencia ubicaciones geográficas de servicios médicos
- 50+ archivos procesados diariamente
- Cero errores críticos en producción desde implementación
- Trazabilidad completa mediante sistema de logging

## Características Técnicas

### Procesamiento Multi-formato
- Detección automática de formatos: ANEXO 1, ANEXO 2, ANEXO 3
- Compatibilidad con formatos Excel: `.xlsx`, `.xlsb`, `.xls`
- Procesamiento de documentos OTROSÍ y actas de negociación
- Manejo de nomenclatura estandarizada: `NNN-TARIFAS-PROVEEDOR-NIT.ext`

### Validación Semántica Inteligente
Diferenciación automática entre:
- **SEDES**: Ubicaciones físicas de prestadores de salud
- **SERVICIOS**: Procedimientos médicos identificados por códigos CUPS

Detección de anomalías:
- Municipios y departamentos colombianos malinterpretados como códigos CUPS
- Números telefónicos confundidos con valores tarifarios
- Códigos de habilitación con formato incorrecto
- Validación contra base de datos de 142 ciudades y 33 departamentos de Colombia

### Sistema de Alertas Categorizado

Alertas organizadas en 15 categorías con prioridad asignada:

```
├── CONTRATOS_NO_ENCONTRADOS (Prioridad: CRÍTICA)
├── HOJAS_SIN_SERVICIOS (Prioridad: ALTA)
├── FECHAS_FALTANTES (Prioridad: MEDIA)
├── AMBULANCIAS_TRASLADOS (Prioridad: BAJA)
├── ANEXOS_FALTANTES (Prioridad: CRÍTICA)
├── FORMATO_PROPIO (Prioridad: MEDIA)
└── ERRORES_PROCESAMIENTO (Prioridad: ALTA)
```

### Conexión SFTP Robusta
- Reconexión automática programada cada 10 contratos
- Sistema de timeouts configurables por operación
- Reintentos con backoff exponencial
- Keepalive para sesiones de larga duración
- Manejo de desconexiones de red

### ETL con Machine Learning (Versión Avanzada)
- Clasificación automática de tipos de archivo mediante algoritmos supervisados
- Predicción de anomalías basada en patrones históricos
- Detección de outliers en datos de tarificación

## Stack Tecnológico

```
Python 3.9+
├── pandas              # Manipulación y análisis de datos
├── openpyxl           # Lectura/escritura de archivos .xlsx
├── pyxlsb             # Procesamiento de archivos .xlsb
├── paramiko           # Cliente SFTP
├── numpy              # Operaciones numéricas
├── scikit-learn       # Machine Learning (versión ETL-ML)
└── xlsxwriter         # Generación de reportes Excel
```

## Arquitectura del Sistema

```
┌──────────────────────────────┐
│  SFTP Server (POSITIVA)      │
│  mft.positiva.gov.co:2243    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  1. Descarga de Archivos     │
│     - Conexión SFTP          │
│     - Reconexión automática  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  2. Detección de Formato     │
│     - ANEXO 1/2/3            │
│     - OTROSÍ                 │
│     - Formato propio         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  3. Validación Semántica     │
│     - Sedes vs Servicios     │
│     - Códigos CUPS           │
│     - Geografía colombiana   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  4. Extracción de Datos      │
│     - Servicios médicos      │
│     - Valores tarifarios     │
│     - Códigos habilitación   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  5. Sistema de Alertas       │
│     - Categorización         │
│     - Priorización           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  6. Consolidación y Export   │
│     - Archivos Excel         │
│     - Sistema de logs        │
│     - Reportes ejecutivos    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  Base de Datos SQL           │
│  (Consolidado Final)         │
└──────────────────────────────┘
```

## Instalación

### Requisitos Previos
- Python 3.9 o superior
- Acceso a servidor SFTP de POSITIVA
- Credenciales de autenticación

### Configuración del Entorno

```bash
# Clonar repositorio
git clone https://github.com/Daniromero1410/consolidador-t25-positiva.git
cd consolidador-t25-positiva

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Configuración de Credenciales

```bash
# Copiar plantilla de configuración
cp config.example.py config.py

# Editar config.py con credenciales reales
# IMPORTANTE: config.py está en .gitignore y nunca debe subirse a control de versiones
```

Estructura del archivo `config.py`:

```python
@dataclass
class Config:
    HOST: str = 'mft.positiva.gov.co'
    PORT: int = 2243
    USERNAME: str = 'your_username'
    PASSWORD: str = 'your_password'
    TIMEOUT_ARCHIVO: int = 60
    MAX_SEDES: int = 50
    # ... otras configuraciones
```

## Uso

### Versión Estándar (Google Colab)

El sistema está diseñado para ejecutarse en Google Colab. Abrir el notebook `consolidador_t25.ipynb` y seguir las instrucciones.

### Versión con Machine Learning

Para procesamiento avanzado con detección de anomalías:

```python
# Abrir ETL_consolidador_ml.ipynb en Google Colab
# Ejecutar celdas secuencialmente
```

## Métricas de Rendimiento

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| Tiempo de procesamiento | 8+ horas | menos de 30 min | 96% |
| Errores de validación | aproximadamente 50 por día | aproximadamente 2 por día | 95% |
| Archivos procesados por día | Manual | 50+ | Automatizado |
| Precisión de datos | 85% | 99.5% | +14.5 puntos |
| Costo operativo mensual | Alto | Bajo | 80% |

## Casos de Uso

### Consolidación Contractual
Procesamiento de anexos contractuales:
- ANEXO 1: Servicios médicos
- ANEXO 2: Medicamentos
- ANEXO 3: Material médico-quirúrgico
- OTROSÍ: Modificaciones y actualizaciones

### Validación Tarifaria
Verificación de precios según manuales autorizados:
- Manual SOAT
- Manual ISS 2001
- Tarifas propias del prestador

### Gestión Multi-sede
Procesamiento de prestadores con múltiples ubicaciones:
- Hospitales con sedes regionales
- IPS con consultorios satélite
- Servicios domiciliarios

### Auditoría de Calidad
Generación de reportes para auditoría:
- Códigos CUPS no válidos
- Valores tarifarios fuera de rango estadístico
- Información contractual incompleta
- Inconsistencias en datos de habilitación

## Validaciones Implementadas

### Validación de Códigos CUPS

```python
# Códigos válidos
Ejemplos aceptados: '890201', '015201', '602E01', '786001'

# Rechazos automáticos
- Nombres de ciudades: 'ARMENIA', 'CALI', 'BOGOTÁ', 'MEDELLÍN'
- Números telefónicos: '3214567890', '3001234567'
- Valores monetarios grandes: mayor o igual a 7 dígitos
- Códigos de habilitación: 8-12 dígitos sin validación CUPS
```

### Validación de Números Telefónicos

```python
# Detección de celulares colombianos
Prefijos válidos: 300-305, 310-318, 320-324, 350-351, 330-333
Longitud: 10 dígitos
Formato: Con o sin guiones

Ejemplos: '3214567890', '321-456-7890', '3001234567'
```

### Validación Semántica de Secciones

```python
# Diferenciación automática
SEDES:    Contienen códigos de habilitación, direcciones, municipios
SERVICIOS: Contienen códigos CUPS, descripciones médicas, tarifas

# Detección de encabezados
TRASLADOS: ORIGEN/DESTINO, ciudades en columnas, valores de transporte
AMBULANCIAS: TAM, TAB, Servicio de ambulancia, Transporte asistencial
```

## Sistema de Alertas

### Niveles de Prioridad

```python
CRITICA = Requiere acción inmediata
ALTA    = Requiere atención en 24 horas
MEDIA   = Revisar en siguiente ciclo
BAJA    = Informativo
```

### Alertas Más Frecuentes

**SIN_ANEXO1 (CRÍTICA)**
```
Descripción: Archivo ANEXO 1 no encontrado en carpeta TARIFAS
Acción: Verificar carga del archivo en servidor SFTP
Impacto: Contrato no procesable
```

**FECHA_FALTANTE_MAESTRA (MEDIA)**
```
Descripción: Contrato sin fecha de inicio en base de datos maestra
Acción: Actualizar registro en tabla de contratos
Impacto: Imposibilidad de validar vigencia
```

**FORMATO_PROPIO (MEDIA)**
```
Descripción: Estructura del archivo no coincide con estándar POSITIVA
Acción: Solicitar corrección a proveedor o procesar manualmente
Impacto: Posible extracción incompleta de datos
```

**CONTRATO_AMBULANCIA_MAESTRA (BAJA)**
```
Descripción: Contrato identificado como servicio exclusivo de ambulancias
Acción: Verificar si requiere procesamiento de ANEXO 1
Impacto: Ninguno si es correcta la clasificación
```

## Historial de Versiones

### v15.1 (Producción actual)
- Exclusión de archivos con patrón "ANÁLISIS DE TARIFAS"
- Corrección en detección de archivos con palabra "TARIFAS" o "TARIFA" aislada
- Mejoras en clasificación de tipos de archivo

### v15.0
- Detección mejorada de patrón `NNN-TARIFAS-PROVEEDOR-NIT`
- Expansión de detección de OTROSÍ: `OTROSI_N`, `OTROSI#N`, `OT_N`, `ADICION_N`
- Nueva función `clasificar_tipo_archivo()` para análisis detallado
- Alerta `FORMATO_PROPIO` para archivos con estructura no estándar

### v14.1
- Alerta de PAQUETES únicamente cuando no existe hoja de servicios válida
- Detección de números telefónicos sin formato (10 dígitos continuos)
- Validación CUPS estricta que rechaza nombres de ciudades colombianas
- Detección de secciones de traslados médicos
- Reconexión SFTP forzada cada 10 contratos procesados

## Seguridad y Cumplimiento

### Protección de Datos Sensibles
- Credenciales almacenadas únicamente en archivo local `config.py`
- `config.py` incluido en `.gitignore` para prevenir exposición
- Sanitización de información personal en logs del sistema
- Conexión SFTP mediante cifrado SSH

### Validación de Integridad
- Verificación de formato de archivos antes de procesamiento
- Validación de permisos de acceso SFTP
- Checksums para archivos descargados

### Cumplimiento Normativo
- Procesamiento de códigos CUPS según Resolución 5269 de 2017
- Validación de tarifas según Manual ISS 2001
- Compatibilidad con normativa de contratos públicos (Ley 80 de 1993)

## Estructura del Proyecto

```
consolidador-t25-positiva/
├── README.md                       # Este archivo
├── .gitignore                      # Archivos excluidos de Git
├── config.example.py               # Plantilla de configuración
├── requirements.txt                # Dependencias del proyecto
├── consolidador_t25.ipynb          # Notebook principal (Colab)
├── ETL_consolidador_ml.ipynb       # Versión con Machine Learning
└── docs/
    └── GUIA_IMPLEMENTACION.md      # Guía paso a paso
```

## Contribución

Este proyecto es de uso interno de POSITIVA Compañía de Seguros a través del área de GESTAR INNOVACIÓN.

Para reportar problemas o sugerir mejoras, contactar al equipo de desarrollo.

## Desarrollo

**Desarrollador Principal:** Daniel Romero  
**Rol:** Software Engineer - Big Data & AI  
**Organización:** GESTAR INNOVACIÓN / POSITIVA Compañía de Seguros  
**Contacto:** danielromero.software@gmail.com

## Licencia

Uso interno - POSITIVA Compañía de Seguros S.A.

Código propietario. Prohibida su distribución o uso fuera del ámbito de POSITIVA sin autorización expresa.

## Enlaces

- [POSITIVA Compañía de Seguros](https://www.positiva.gov.co/)
- [Guía de Implementación](./docs/GUIA_IMPLEMENTACION.md)

---

**Sistema desarrollado para POSITIVA Compañía de Seguros**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Daniel_Romero-0077B5?logo=linkedin)](https://www.linkedin.com/in/daniromerosoftware)
[![GitHub](https://img.shields.io/badge/GitHub-Daniromero1410-181717?logo=github)](https://github.com/Daniromero1410)
