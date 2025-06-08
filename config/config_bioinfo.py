# Standard Library

# Third Party Library

# Local Library
from utils.setup_logger import setup_logger


class DiseaseConfig(BaseConfig):
    diseases: Dict[str, Any] = Field(
        Dict[str, Any], description="Dictionary of diseases and their variants."
    )

    def __init__(self, config_file: str):
        super().__init__(config_file)
        self.diseases = self.config.get("disease_info", {})
        self.logger = setup_logger(name="BioInfo Config")

    def add_disease(self, disease_name: str, variants: Dict[str, Any]):
        self.diseases[disease_name] = {"variants": variants}
        self.save_config()
        self.logger.info(f"Disease '{disease_name}' added with variants: {variants}")

    def list_diseases(self) -> list:
        return list(self.diseases.keys())

    def get_variants(self, disease_name: str) -> Optional[Dict[str, Any]]:
        return self.diseases.get(disease_name, {}).get("variants", {})

    def insert_disease(self, db_path, disease_name):
        """Insert a new disease into the database."""
        import sqlite3

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("INSERT INTO diseases (name) VALUES (?)", (disease_name,))
            self.logger.info(f"Disease '{disease_name}' added to database.")

        except Exception as e:
            self.logger.error(f"Error inserting disease: {e}")
        finally:
            conn.commit()
            conn.close()

    def init_db(self, db_path):
        """Initialize the SQLite database."""
        import sqlite3

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS genes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                disease_id INTEGER,
                FOREIGN KEY (disease_id) REFERENCES diseases (id)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                identifier TEXT NOT NULL,
                gene_id INTEGER,
                FOREIGN KEY (gene_id) REFERENCES genes (id)
            )
            """)
            self.logger.info("Database initialized successfully.")
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
        finally:
            conn.commit()
            conn.close()

    class Config:
        extra = "allow"
