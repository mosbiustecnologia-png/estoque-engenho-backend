"""
Estoque Engenho - Configurações
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "estoque_engenho"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_DEBUG: bool = True
    API_TITLE: str = "Estoque Engenho API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API de Controle de Estoque com Código de Barras"
    
    # Segurança
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:19006"
    
    @property
    def database_url(self) -> str:
        """URL de conexão com o banco de dados"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def cors_origins(self) -> List[str]:
        """Lista de origens permitidas para CORS"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global das configurações
settings = Settings()
