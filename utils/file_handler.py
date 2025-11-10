"""
File handling utilities
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
from utils.logger import logger


class FileHandler:
    """Handle file operations like copy, move, delete, cleanup"""
    
    @staticmethod
    def safe_copy(src: str, dst: str) -> bool:
        """
        Safely copy file with error handling
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            Success status
        """
        try:
            # Create destination directory if needed
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            logger.info(f"File copied: {src} -> {dst}")
            return True
        except Exception as e:
            logger.error(f"Failed to copy file: {e}")
            return False
    
    @staticmethod
    def safe_move(src: str, dst: str) -> bool:
        """
        Safely move file with error handling
        
        Args:
            src: Source file path
            dst: Destination file path
            
        Returns:
            Success status
        """
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            logger.info(f"File moved: {src} -> {dst}")
            return True
        except Exception as e:
            logger.error(f"Failed to move file: {e}")
            return False
    
    @staticmethod
    def safe_delete(file_path: str) -> bool:
        """
        Safely delete file with error handling
        
        Args:
            file_path: Path to file
            
        Returns:
            Success status
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False
    
    @staticmethod
    def cleanup_directory(directory: str, older_than_hours: int = 24) -> int:
        """
        Clean up old files from directory
        
        Args:
            directory: Directory path
            older_than_hours: Delete files older than this many hours
            
        Returns:
            Number of files deleted
        """
        deleted_count = 0
        cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
        
        try:
            for file_path in Path(directory).glob('*'):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_time:
                        if FileHandler.safe_delete(str(file_path)):
                            deleted_count += 1
        except Exception as e:
            logger.error(f"Cleanup error in {directory}: {e}")
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old files from {directory}")
        
        return deleted_count
    
    @staticmethod
    def get_unique_filename(directory: str, filename: str) -> str:
        """
        Generate unique filename if file already exists
        
        Args:
            directory: Target directory
            filename: Desired filename
            
        Returns:
            Unique filename
        """
        path = Path(directory) / filename
        
        if not path.exists():
            return filename
        
        # Add counter to filename
        name = path.stem
        ext = path.suffix
        counter = 1
        
        while path.exists():
            new_name = f"{name}_{counter}{ext}"
            path = Path(directory) / new_name
            counter += 1
        
        return path.name
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[dict]:
        """
        Get file information
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary with file info or None
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            
            stat = path.stat()
            return {
                'name': path.name,
                'size': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'extension': path.suffix,
                'absolute_path': str(path.absolute())
            }
        except Exception as e:
            logger.error(f"Failed to get file info: {e}")
            return None
    
    @staticmethod
    def list_files(directory: str, pattern: str = '*') -> List[str]:
        """
        List files in directory matching pattern
        
        Args:
            directory: Directory path
            pattern: Glob pattern
            
        Returns:
            List of file paths
        """
        try:
            return [str(f) for f in Path(directory).glob(pattern) if f.is_file()]
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
