"""
Archivo de configuración de ejemplo para Consolidador T25
IMPORTANTE: Copiar este archivo como config.py y completar con credenciales reales
"""

from dataclasses import dataclass, field


@dataclass
class Config:
    """
    Configuración centralizada del sistema ETL Consolidador T25.
    
    Este archivo contiene todos los parámetros de configuración necesarios
    para la conexión SFTP, timeouts, rutas y límites de procesamiento.
    
    USO:
        1. Copiar este archivo: cp config.example.py config.py
        2. Editar config.py con credenciales reales
        3. Verificar que config.py está en .gitignore
    """
    
    # Configuración de servidor SFTP
    HOST: str = 'tu-sftp-host.com'  # Ejemplo: 'mft.example.com'
    PORT: int = 22                    # Puerto estándar SFTP (22) o personalizado
    USERNAME: str = 'tu_username'   # Usuario SFTP
    PASSWORD: str = 'tu_password'   # Contraseña SFTP
    
    # Timeouts y reintentos
    TIMEOUT_CONEXION: int = 30        # Timeout para conexión inicial (segundos)
    TIMEOUT_OPERACION: int = 20       # Timeout para operaciones SFTP (segundos)
    TIMEOUT_ARCHIVO: int = 60         # Timeout por archivo procesado (segundos)
    MAX_REINTENTOS_CONEXION: int = 5  # Máximo de intentos de conexión
    MAX_REINTENTOS_OPERACION: int = 3 # Máximo de reintentos por operación
    BACKOFF_BASE: float = 2.0         # Base para backoff exponencial
    KEEPALIVE_INTERVAL: int = 5       # Intervalo de keepalive (segundos)
    
    # Rutas y carpetas
    CARPETA_PRINCIPAL: str = 'CARPETA RAIZ'  # Carpeta raíz en SFTP
    CARPETA_TRABAJO: str = './trabajo_temp'                         # Carpeta temporal local
    
    # Configuración de procesamiento
    CONTRATOS_PROBLEMATICOS: set = field(default_factory=lambda: {'572-2023'})
    TIMEOUT_CONTRATOS_PROBLEMATICOS: int = 30
    MAX_SEDES: int = 50  # Máximo de sedes a procesar por archivo


# Instancia global de configuración
# Esta instancia será importada por los módulos del sistema
CONFIG = Config()
