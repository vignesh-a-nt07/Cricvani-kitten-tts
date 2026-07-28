import os
from utils.logger import logger

def delete_temp_file(file_path: str):
    """Deletes a temporary file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Successfully deleted temporary file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to delete temporary file {file_path}: {str(e)}")
