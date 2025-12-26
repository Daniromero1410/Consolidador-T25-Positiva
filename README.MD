# Guía de Implementación - Consolidador T25

## Objetivo

Esta guía te ayudará a configurar y ejecutar el Consolidador T25 desde cero, ya sea en Google Colab o en un entorno local.

---

## OPCIÓN 1: Ejecución en Google Colab (Recomendado)

### Paso 1: Preparar Archivos

1. Descargar los siguientes archivos del repositorio:
   - `consolidador_t25.ipynb` (o `ETL_consolidador_ml.ipynb` para versión ML)
   - `config.example.py`

2. Crear archivo `config.py` basado en `config.example.py`:
   ```python
   # config.py
   @dataclass
   class Config:
       HOST: str = 'mft.positiva.gov.co'
       PORT: int = 2243
       USERNAME: str = 'tu_usuario_real'
       PASSWORD: str = 'tu_contraseña_real'
       # ... resto de configuración
   ```

### Paso 2: Subir a Google Colab

1. Ir a [Google Colab](https://colab.research.google.com/)
2. Archivo → Subir notebook
3. Seleccionar `consolidador_t25.ipynb`

### Paso 3: Configurar Credenciales

Una vez en Colab, ejecutar la primera celda y luego:

```python
# Subir archivo config.py cuando se solicite
from google.colab import files
uploaded = files.upload()

# El sistema cargará automáticamente las credenciales
```

### Paso 4: Subir Maestra de Contratos

Cuando el notebook lo solicite, subir el archivo Excel con la maestra de contratos vigentes.

### Paso 5: Ejecutar Celdas Secuencialmente

Ejecutar cada celda en orden:
1. Instalación de dependencias
2. Carga de configuración
3. Carga de maestra
4. Selección de contratos
5. Procesamiento
6. Generación de archivos
7. Descarga de resultados

### Paso 6: Descargar Resultados

Los archivos generados se descargarán automáticamente:
- `CONSOLIDADO_[fecha].xlsx` - Datos consolidados
- `ALERTAS_[fecha].xlsx` - Alertas categorizadas por hojas
- `RESUMEN_[fecha].xlsx` - Resumen de ejecución

---

## OPCIÓN 2: Ejecución Local

### Paso 1: Clonar Repositorio

```bash
git clone https://github.com/Daniromero1410/consolidador-t25-positiva.git
cd consolidador-t25-positiva
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno
python -m venv venv

# Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar Credenciales

```bash
# Copiar plantilla
cp config.example.py config.py

# Editar config.py con tus credenciales
# Usar editor de texto o IDE
```

### Paso 5: Ejecutar Jupyter Notebook

```bash
# Instalar Jupyter si no lo tienes
pip install jupyter

# Iniciar Jupyter
jupyter notebook

# Abrir consolidador_t25.ipynb en el navegador
```

### Paso 6: Seguir Proceso de Colab

Ejecutar celdas secuencialmente como en la Opción 1.

---

## Configuración Avanzada

### Ajustar Timeouts

Si procesas contratos con archivos muy grandes:

```python
# En config.py
TIMEOUT_ARCHIVO: int = 120  # Aumentar a 2 minutos
TIMEOUT_CONTRATOS_PROBLEMATICOS: int = 180  # 3 minutos para problemáticos
```

### Configurar Contratos Problemáticos

Si un contrato específico requiere más tiempo:

```python
# En config.py
CONTRATOS_PROBLEMATICOS: set = field(default_factory=lambda: {
    '572-2023',
    '234-2024',  # Agregar más contratos aquí
})
```

### Ajustar Máximo de Sedes

Si un prestador tiene muchas sedes:

```python
# En config.py
MAX_SEDES: int = 100  # Aumentar límite
```

---

## Solución de Problemas

### Error: "Socket is closed"

**Causa:** Pérdida de conexión SFTP durante procesamiento largo.

**Solución:**
- El sistema reconecta automáticamente cada 10 contratos
- Si persiste, reducir el tamaño del lote de contratos a procesar

### Error: "Timeout procesando archivo"

**Causa:** Archivo muy grande o formato complejo.

**Solución:**
1. Agregar contrato a `CONTRATOS_PROBLEMATICOS`
2. Aumentar `TIMEOUT_CONTRATOS_PROBLEMATICOS`

### Error: "No se encontró hoja de servicios"

**Causa:** Archivo con formato no estándar o solo contiene ambulancias/traslados.

**Solución:**
- Revisar el archivo en `ALERTAS.xlsx` hoja `HOJAS_SIN_SERVICIOS`
- Si es formato propio del prestador, procesar manualmente

### Error: "Contrato no se encuentra en GoAnywhere"

**Causa:** Número de contrato no existe en servidor SFTP.

**Solución:**
1. Verificar número y año en la maestra
2. El sistema busca con cero inicial automáticamente (901 → 0901)
3. Si el contrato es muy nuevo, puede no estar sincronizado aún

### Warning: "Contratos sin fecha en maestra"

**Causa:** Registro de contrato sin fecha de inicio en Excel de maestra.

**Solución:**
- El sistema usa la fecha de modificación del archivo SFTP como fallback
- Para mayor precisión, actualizar la maestra con las fechas correctas

---

## Interpretación de Resultados

### Archivo CONSOLIDADO

**Columnas principales:**
- `codigo_cups` - Código del procedimiento médico
- `descripcion_del_cups` - Descripción del servicio
- `tarifa_unitaria_en_pesos` - Valor en pesos colombianos
- `manual_tarifario` - ISS, SOAT, o PROPIO
- `porcentaje_manual_tarifario` - Porcentaje de incremento/decremento
- `codigo_de_habilitacion` - Código de habilitación con sede
- `contrato` - Número de contrato (formato: NNN-AAAA)
- `origen_tarifa` - Inicial, Otrosí N, o Acta N
- `fecha_de_acuerdo` - Fecha de vigencia

### Archivo ALERTAS

**Hojas categorizadas:**

1. **CONTRATOS_NO_ENCONTRADOS** (Prioridad: CRÍTICA)
   - Contratos que no existen
   - Carpetas TARIFAS faltantes

2. **HOJAS_SIN_SERVICIOS** (Prioridad: ALTA)
   - Archivos sin hoja de servicios identificable
   - Problemas de detección de columnas

3. **FECHAS_FALTANTES** (Prioridad: MEDIA)
   - Contratos sin fecha en maestra
   - Sistema usó fecha de archivo como fallback

4. **AMBULANCIAS_TRASLADOS** (Prioridad: BAJA)
   - Contratos identificados como ambulancias
   - Archivos que solo contienen traslados
   - Informativo, no requiere acción

5. **ANEXOS_FALTANTES** (Prioridad: CRÍTICA)
   - Archivos ANEXO 1 no encontrados
   - Actas de negociación faltantes en secuencia

6. **FORMATO_PROPIO** (Prioridad: MEDIA)
   - Archivos con estructura diferente al estándar POSITIVA
   - Pueden requerir procesamiento manual

7. **ERRORES_PROCESAMIENTO** (Prioridad: ALTA)
   - Errores técnicos durante procesamiento
   - Timeouts, errores de lectura

### Archivo RESUMEN

**Información por contrato:**
- Éxito (SI/NO)
- Cantidad de registros procesados
- Tiempo de procesamiento
- Mensaje de error (si aplica)
- Indicador de ambulancia (si aplica)

---

## Mejores Prácticas

### Planificación de Ejecución

1. **Contratos individuales:** Para pruebas o correcciones urgentes
2. **Por año:** Para consolidación mensual o trimestral
3. **Completo:** Para cierre anual o auditorías

### Gestión de Alertas

**Priorizar por criticidad:**

```
CRÍTICA → Atender inmediatamente
  ├── Contratos no encontrados
  └── Anexos faltantes

ALTA → Atender en 24 horas
  ├── Hojas sin servicios
  └── Errores de procesamiento

MEDIA → Revisar en ciclo semanal
  ├── Fechas faltantes
  └── Formatos propios

BAJA → Informativo
  └── Ambulancias/Traslados
```

### Validación de Resultados

Antes de cargar a base de datos:

1. **Verificar totales:** Comparar cantidad de registros vs esperado
2. **Revisar alertas críticas:** Asegurar que no hay contratos sin procesar
3. **Validar fechas:** Confirmar que las fechas son coherentes
4. **Spot check:** Revisar manualmente 5-10 contratos aleatorios

### Mantenimiento

**Semanal:**
- Revisar alertas de formatos propios
- Actualizar maestra con contratos nuevos

**Mensual:**
- Verificar lista de ciudades colombianas (si hay nuevos municipios)
- Revisar contratos problemáticos y ajustar timeouts

**Trimestral:**
- Actualizar dependencias: `pip install --upgrade -r requirements.txt`
- Revisar logs de reconexiones SFTP

---

## Contacto y Soporte

**Desarrollador:** Daniel Romero  
**Email:** danielromero.software@gmail.com  
**Organización:** GESTAR INNOVACIÓN / POSITIVA Compañía de Seguros

**Para reportar problemas:**
1. Revisar primero esta guía y la sección de solución de problemas
2. Revisar el archivo ALERTAS generado
3. Si el problema persiste, contactar con:
   - Descripción del error
   - Archivos CONSOLIDADO y ALERTAS
   - Captura de pantalla del error (si aplica)

---

## Glosario

**ANEXO 1:** Archivo Excel con tarifas de servicios médicos  
**CUPS:** Clasificación Única de Procedimientos en Salud  
**OTROSÍ:** Modificación o adición a un contrato existente  
**Acta de Negociación:** Documento que modifica condiciones tarifarias  
**Código de Habilitación:** Identificador único de sede prestadora  
**Manual Tarifario:** ISS 2001, SOAT, o Tarifas Propias del prestador  
**Sede:** Ubicación física donde el prestador ofrece servicios  
**Prestador:** Institución Prestadora de Servicios de Salud (IPS)

---

Esta guía cubre los casos de uso más comunes. Para situaciones específicas o consultas técnicas avanzadas, contactar al equipo de desarrollo.
