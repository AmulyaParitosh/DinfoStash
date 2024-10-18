from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    apiKey: str
    authDomain: str
    projectId: str
    storageBucket: str
    messagingSenderId: str
    appId: str
    measurementId: str
    serviceAccountCertificatePath: str

load_dotenv(
    override=True, verbose=True
)  # Load the .env file in the root directory of the project

SETTINGS = Settings()  # type: ignore
