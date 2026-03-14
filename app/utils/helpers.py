"""Helper utilities"""

import os
import uuid
from typing import Optional
from datetime import datetime

def generate_id(prefix: str = "") -> str:
    """
    Generate a unique ID
    
    Args:
        prefix: Optional prefix for the ID
    
    Returns:
        Generated unique ID
    """
    unique_id = str(uuid.uuid4()).replace("-", "")
    if prefix:
        return f"{prefix}_{unique_id[:8]}"
    return unique_id

def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes
    
    Args:
        file_path: Path to file
    
    Returns:
        File size in bytes
    """
    return os.path.getsize(file_path)

def get_file_extension(filename: str) -> str:
    """
    Get file extension
    
    Args:
        filename: Name of file
    
    Returns:
        File extension
    """
    _, ext = os.path.splitext(filename)
    return ext.lower()

def ensure_directory(directory: str) -> None:
    """
    Ensure directory exists, create if not
    
    Args:
        directory: Directory path
    """
    os.makedirs(directory, exist_ok=True)

def safe_filename(filename: str) -> str:
    """
    Make filename safe for filesystem
    
    Args:
        filename: Original filename
    
    Returns:
        Safe filename
    """
    import re
    
    # Remove special characters
    safe_name = re.sub(r'[^\w\s\-.]', '', filename)
    # Replace multiple spaces with single space
    safe_name = re.sub(r'\s+', ' ', safe_name)
    # Replace spaces with underscores
    safe_name = safe_name.replace(' ', '_')
    
    return safe_name

def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to HH:MM:SS
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def get_timestamp() -> str:
    """
    Get current timestamp
    
    Returns:
        Current timestamp as ISO string
    """
    return datetime.now().isoformat()
