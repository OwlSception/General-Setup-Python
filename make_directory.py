import os
import subprocess
import logging

def get_python_boilerplate(file_path):
    """Return boilerplate content for a Python file."""
    return f"""
    \"\"\"{file_path} Module description.

    This is an auto-generated module part of the project.
    
    \"\"\"
    # {file_path}
    filename = "{file_path}"
    
    # Standard Library
    import os
    
    # Third Party Library
    from dotenv import load_dotenv
    
    # Local Library
    from logger.setup_logger import setup_logger
    
    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    # Setup Logger
    log_file_name = os.path.join(os.path.dirname(__file__), "logs", "project_log.log")
    
    logger = setup_logger(
        name=f"{file_path}",
        log_file_name=log_file_name,
        level=logging.DEBUG,
    )
    """

def create_project_directory(project_name):
    """Create a project directory structure and necessary files."""
    # Define the directory structure
    directories = [
        os.path.join(project_name, ''),
        os.path.join(project_name, 'config'),
        os.path.join(project_name, 'data', 'final_data'),
        os.path.join(project_name, 'data', 'interim_data'),
        os.path.join(project_name, 'data', 'processed_data'),
        os.path.join(project_name, 'data', 'raw_data'),
        os.path.join(project_name, 'docs'),
        os.path.join(project_name, 'logs'),
        os.path.join(project_name, 'logger'),
        os.path.join(project_name, 'models'),
        os.path.join(project_name, 'notebooks'),
        os.path.join(project_name, 'reports'),
        os.path.join(project_name, 'resources'),
        os.path.join(project_name, 'results'),
        os.path.join(project_name, 'src'),
        os.path.join(project_name, 'src', 'data_acquisition'),
        os.path.join(project_name, 'src', 'data_acquisition', 'helpers'),
        os.path.join(project_name, 'src', 'cleaning'),
        os.path.join(project_name, 'src', 'visualization'),
        os.path.join(project_name, 'src', 'features'),
        os.path.join(project_name, 'src', 'models'),
        os.path.join(project_name, 'src', 'storage'),
        os.path.join(project_name, 'src', 'styling'),
        os.path.join(project_name, 'tests'),
        os.path.join(project_name, 'utils'),
    ]

    # Create the directories
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f'Created directory: {directory}')
        except Exception as e:
            print(f'Error creating directory {directory}: {e}')

    # Create the initial files and write the boilerplate
    init_files = {
        os.path.join(project_name, "config", "__init__.py"): "",
        os.path.join(project_name, "config", "config.py"): "",
        os.path.join(project_name, "config", "load_config.py"): "",
        os.path.join(project_name, "data", "__init__.py"): "",
        os.path.join(project_name, "docs", "README.md"): f"# {project_name.title()} Read Me",
        os.path.join(project_name, "docs", "LICENSE"): "License",
        os.path.join(project_name, "logs", "citations.json"): "",
        os.path.join(project_name, "logs", f'{project_name}.log'): "",
        os.path.join(project_name, "logger", "citation_logger.py"): "",
        os.path.join(project_name, "logger", "setup_logger.py"): "",
        os.path.join(project_name, "logger", "__init__.py"): "",
        os.path.join(project_name, "src", "dataset.py"): "",
        os.path.join(project_name, "src", "data_acquisition", "data_acquisition.py"): "",
        os.path.join(project_name, "src", "data_acquisition", "helpers", "helpers.py"): "",
        os.path.join(project_name, "src", "data_acquisition", "read_files.py"): "",
        os.path.join(project_name, "src", "cleaning", "skewed_data.py"): "",
        os.path.join(project_name, "src", "features", "build_features.py"): "",
        os.path.join(project_name, "src", "visualization", "plots.py"): "",
        os.path.join(project_name, "src", "__init__.py"): "",
        os.path.join(project_name, "tests", "__init__.py"): "",
        os.path.join(project_name, "utils", "utils.py"): "",
        os.path.join(project_name, "main.py"): "",
        os.path.join(project_name, "docs", "requirements.txt"): "",  # We'll fill this later
        os.path.join(project_name, "docs", "index.md"): f"# {project_name.title()} Index \n",
    }

    # Create the files and write the boilerplate
    for file_path, content in init_files.items():
        try:
            # Create the file if it does not exist
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    # Write boilerplate content if it's not empty
                    if "logger" in file_path or "config" in file_path or "data_acquisition" in file_path or "run_project.py" in file_path:
                        f.write(get_python_boilerplate(file_path))
                    elif "index.md" in file_path:
                        f.write(print_directory_structure(project_name))
                    else:
                        f.write(content)
                print(f'Created file: {file_path} with boilerplate content')
            else:
                print(f'File already exists: {file_path}')
        except Exception as e:
            print(f'Error creating file {file_path}: {e}')

def update_requirements(project_directory):
    """Updates the requirements.txt file with the current packages."""
    try:
        req_path = os.path.join(project_directory, "docs", "requirements.txt")
        with open(req_path, "w") as req_file:
            subprocess.run(["pip", "freeze"], stdout=req_file)
        print(f'Updated requirements in {req_path}')
    except Exception as e:
        print(f'Error updating requirements: {e}')
