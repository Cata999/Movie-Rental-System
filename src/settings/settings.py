# File: src/settings/settings.py (FINAL FIX)

import configparser
import os
from src.exceptions.exceptions import MovieRentalException


class Settings:
    def __init__(self, config_file='settings.properties'):
        """Initializes the Settings class by robustly locating the configuration file."""

        # 1. Calculate the PROJECT ROOT (a9-Cata999S/) relative to the settings.py file
        current_file_path = os.path.abspath(__file__)
        settings_dir = os.path.dirname(current_file_path)
        self.project_root = os.path.abspath(os.path.join(settings_dir, os.pardir, os.pardir))

        # 2. Form the absolute path to the settings file
        absolute_config_path = os.path.join(self.project_root, config_file)

        self.config = configparser.ConfigParser()

        if not os.path.exists(absolute_config_path):
            raise MovieRentalException(
                f"Configuration file not found at: {absolute_config_path}. "
                "Ensure settings.properties is directly in the project root folder."
            )

        self.config.read(absolute_config_path)

        if 'RepositorySettings' not in self.config:
            raise MovieRentalException("Configuration file must contain a [RepositorySettings] section.")

    def get_repo_type(self):
        """Returns the chosen repository type (e.g., 'textfiles')."""
        try:
            repo_type = self.config.get('RepositorySettings', 'repository').lower()
            if repo_type not in ["inmemory", "textfiles", "binaryfiles"]:
                raise MovieRentalException(f"Invalid repository type: {repo_type}.")
            return repo_type
        except configparser.NoOptionError:
            raise MovieRentalException("Missing 'repository' option in [RepositorySettings] section.")

    def get_file_path(self, entity_name):
        """
        Returns the ABSOLUTE file path for a specific entity.
        The path is constructed from the project root and the relative path in the config file.
        """
        try:
            # Get the path from the config file (e.g., 'src/ui/clients.txt')
            relative_path = self.config.get('RepositorySettings', entity_name)

            # Combine the project root with the relative path to get an absolute path
            return os.path.join(self.project_root, relative_path)

        except configparser.NoOptionError:
            raise MovieRentalException(f"Missing file path option for '{entity_name}' in [RepositorySettings] section.")