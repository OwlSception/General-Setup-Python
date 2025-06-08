# Standard Library Imports
import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional
from unittest.mock import Base

# Third Party Library Imports
from pydantic import BaseModel, Field, ValidationError
from utils.data_manager import DataManager

# from template.logger.setup_logger import setup_logger
# Local Library Imports
from template.utils import setup_logger

# Setup logger
project_name = "template_project"
log_file_name = f"{project_name}_log.log"

logger = setup_logger.setup_logger("ProjectConfigLog")

# config_file = "config.json"


class BaseConfig(BaseModel):
    version: str = Field(str, description="Version of the configuration")
    description: str = Field(str, description="Description of the configuration")
    author: str = Field(str, description="Author of the configuration")
    email: str = Field(str, description="Email of the configuration")
    default_data_source_enabled: bool = Field(
        False, description="Default enabled status for data sources"
    )

    class Config:
        extra = "allow"

    def __init__(self):
        super().__init__()
        self.data_manger = DataManager()
        self.config_file = "config.jsonc"
        print(f"Config File: {self.config_file}")
        self.config = {}
        self.load_config()
        self.logger = setup_logger.setup_logger(name="Base Project Config Log")

    def load_config(self):
        try:
            self.data_manger.load_data(self.config_file, subfolder="config")
            logger.info("Configuration loaded and validated successfully.")
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            raise
        except json.JSONDecodeError as json_err:
            logger.error(f"Error decoding JSON from configuration file: {json_err}")
            raise

    def save_config(self):
        try:
            self.data_manger.save_data(self.config_file, subfolder="config")
            logger.info("Configuration saved successfully.")
        except Exception as e:
            print(f"Error: {e}")

    def update_config(self, key: str, value):
        try:
            setattr(self, key, value)
            self.save_config()
            logger.info(f"Configuration updated: {key} = {value}")
        except ValidationError as e:
            logger.error(f"Error updating configuration: {e}")
            raise

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        raise KeyError(f"{key} not found in the configuration.")

    def __setitem__(self, key, value):
        self.update_config(key, value)


class DataAcquisitionConfig(BaseConfig):
    api_keys: Dict[str, str] = Field(
        Dict[str, str], description="API keys for various data sources."
    )
    data_sources: Dict[str, Dict[str, Any]] = Field(
        Dict[str, Dict[str, Any]], description="Configuration for data sources."
    )
    retry_settings: Dict[str, int] = Field(
        Dict[str, int], description="Settings for retrying failed requests."
    )
    rate_limiting: Dict[str, Any] = Field(
        Dict[str, Any], description="Rate limiting settings."
    )

    def __init__(self: str):
        super().__init__()

        self.api_keys = os.getenv("API_KEYS")
        self.data_sources = self.config.get("data_sources", {})
        self.retry_attempts = self.config.get("retry_attempts", 1)
        self.retry_delay = self.config.get("retry_delay", 10)

    def set_data_source_enabled(self, source_name: str, enabled: bool):
        if source_name in self.data_sources:
            self.data_sources[source_name]["enabled"] = enabled
            self.save_config()
            print(f"Data source '{source_name}' enabled set to {enabled}.")
        else:
            print(f"Data source '{source_name}' not found in configuration.")

    def get_data_sources(self) -> Dict[str, Any]:
        return self.data_sources

    def set_all_data_sources_enabling(self, enabled: bool):
        for source_name in self.config.get("data_sources", {}).keys():
            self.config["data_sources"][source_name]["enabled"] = enabled
        self.save_config()
        print(f"All data sources enabled set to {enabled}.")

    class Config:
        extra = "allow"


class StorageConfig(BaseConfig):
    storage_format: Dict[str, str] = Field(
        Dict[str, str], description="Supported storage formats and their extensions."
    )
    save_filename: str = Field(str, description="Format for saving filenames.")
    file_paths: Dict[str, str] = Field(
        Dict[str, str], description="Paths for storing various types of data."
    )

    def __init__(self):
        super().__init__()
        self.storage_format = self.config.get("storage_format", {})
        self.save_filename = self.config.get(
            "save_filename", f"{project_name}_incorrect_save"
        )
        self.file_paths = self.config.get("file_paths", {})

    class Config:
        extra = "allow"


class DataLimiter(BaseConfig):
    def __init__(self):
        super().__init__()
        self.max_data_size = self.config.get("max_data_size", 1000)
        self.rate_limiting = self.config.get("rate_limiting", False)
        self.limit = self.rate_limiting.get("limit", 40) if self.rate_limiting else 40
        self.period = (
            self.config.get("rate_limiting", {}).get("period", 60)
            if self.rate_limiting
            else 60
        )
        self.interval = self.period / float(self.limit)
        self.last_time_called = 0.0

    def limit_data_retrieval(self, data: Any):
        limited_data = (
            data[: self.max_data_size] if len(data) > self.max_data_size else data
        )
        logger.debug(f"Limited data size from {len(data)} to {len(limited_data)}.")
        return limited_data

    def rate_limited(self, func):
        def wrapper(*args, **kwargs):
            elapsed = time.monotonic() - self.last_time_called
            if elapsed < self.interval:
                sleep_time = self.interval - elapsed
                logger.debug(
                    f"Rate limiting in effect. Sleeping for {sleep_time:.2f} seconds."
                )
                time.sleep(sleep_time)
            self.last_time_called = time.monotonic()
            return func(*args, **kwargs)

        return wrapper

    def init_limiter(self):
        self.last_time_called = time.monotonic()

    def reset_limiter(self):
        """Resets the rate limiter's last_time_called to the current time."""
        self.last_time_called = time.monotonic()


# class Config:
#     def __init__(self, config_file: str = "config.json"):
#         try:
#             self.base_config = BaseConfig(config_file=config_file)
#             self.data_sources = DataAcquisitionConfig(config_file=config_file)
#             self.storage = StorageConfig(config_file=config_file)
#             self.data_limiter = DataLimiter(self.base_config.config)
#             self.diseases = DiseaseConfig(config_file=config_file)
#         except FileNotFoundError as e:
#             logger.error(f"Error loading configuration: {e}")
#             raise
#         except ValidationError as e:
#             logger.error(f"Error validating configuration: {e}")
#             sys.exit(1)


# Example usage

# print(config.base_config.config)
# print(config.data_sources.api_keys)
