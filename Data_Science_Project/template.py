import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name = "DataScience"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",  # Corrected typo
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "Dockerfile",
    "setup.py",
    "research/research.ipynb",  # Corrected typo
    "templates/index.html",
]

for file in list_of_files:
    file_path = Path(file)
    if file_path.parent != Path("."):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Creating directory {file_path.parent} for the file: {file_path.name}")
    if not file_path.exists() or file_path.stat().st_size == 0:
        file_path.touch(exist_ok=True)
        logging.info(f"Creating empty file: {file_path}")
    else:
        logging.info(f"{file_path.name} already exists")
