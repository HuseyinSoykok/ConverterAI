"""
Advanced Table Detection using OpenCV
Detects table structures, rows, columns, and cells in images
"""
import cv2
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path
from utils.logger import logger


class TableDetector:
    """
    Detect and extract table structures from images using computer vision
    
    Features:
    - Horizontal/vertical line detection
    - Cell boundary identification
    - Row and column structure recognition
    - Pre-processing for better OCR results
    """
    
    def __init__(self):
        """Initialize table detector"""
        self.min_line_length = 30  # Minimum line length to consider
        self.max_line_gap = 10     # Maximum gap between line segments
        
    def detect_tables(self, image_path: str) -> List[Dict[str, Any]]:
        """
        Detect tables in an image
        
        Args:
            image_path: Path to image file
        
        Returns:
            List of detected table regions with coordinates
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                logger.error(f"Failed to read image: {image_path}")
                return []
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply preprocessing
            processed = self._preprocess_for_tables(gray)
            
            # Detect horizontal and vertical lines
            horizontal_lines = self._detect_horizontal_lines(processed)
            vertical_lines = self._detect_vertical_lines(processed)
            
            # Find table regions (intersections of h/v lines)
            tables = self._find_table_regions(horizontal_lines, vertical_lines, image.shape)
            
            logger.info(f"Detected {len(tables)} potential tables in image")
            return tables
            
        except Exception as e:
            logger.error(f"Table detection failed: {e}")
            return []
    
    def _preprocess_for_tables(self, gray_image: np.ndarray) -> np.ndarray:
        """
        Preprocess image for better table detection
        
        Args:
            gray_image: Grayscale input image
        
        Returns:
            Preprocessed binary image
        """
        # Apply adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray_image, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )
        
        # Noise removal
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        return binary
    
    def _detect_horizontal_lines(self, binary_image: np.ndarray) -> np.ndarray:
        """
        Detect horizontal lines in image
        
        Args:
            binary_image: Binary input image
        
        Returns:
            Image with only horizontal lines
        """
        # Create horizontal kernel (wide and short)
        horizontal_size = binary_image.shape[1] // 30
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
        
        # Apply morphological operations
        horizontal_lines = cv2.erode(binary_image, horizontal_kernel, iterations=1)
        horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=1)
        
        return horizontal_lines
    
    def _detect_vertical_lines(self, binary_image: np.ndarray) -> np.ndarray:
        """
        Detect vertical lines in image
        
        Args:
            binary_image: Binary input image
        
        Returns:
            Image with only vertical lines
        """
        # Create vertical kernel (tall and narrow)
        vertical_size = binary_image.shape[0] // 30
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))
        
        # Apply morphological operations
        vertical_lines = cv2.erode(binary_image, vertical_kernel, iterations=1)
        vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=1)
        
        return vertical_lines
    
    def _find_table_regions(
        self,
        h_lines: np.ndarray,
        v_lines: np.ndarray,
        image_shape: Tuple[int, ...]
    ) -> List[Dict[str, Any]]:
        """
        Find table regions from horizontal and vertical lines
        
        Args:
            h_lines: Horizontal lines image
            v_lines: Vertical lines image
            image_shape: Original image shape
        
        Returns:
            List of table region dictionaries
        """
        # Combine horizontal and vertical lines
        table_mask = cv2.add(h_lines, v_lines)
        
        # Find contours (potential table boundaries)
        contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        tables = []
        min_table_area = 10000  # Minimum area to consider as table
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            if area > min_table_area:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Calculate aspect ratio
                aspect_ratio = float(w) / h if h > 0 else 0
                
                # Tables are typically wider than tall, but not extremely so
                if 0.3 < aspect_ratio < 5.0:
                    tables.append({
                        'x': int(x),
                        'y': int(y),
                        'width': int(w),
                        'height': int(h),
                        'area': int(area),
                        'aspect_ratio': float(aspect_ratio)
                    })
        
        # Sort tables by y-coordinate (top to bottom)
        tables.sort(key=lambda t: t['y'])
        
        return tables
    
    def extract_table_structure(
        self,
        image_path: str,
        table_region: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract detailed structure (rows, columns, cells) from a table region
        
        Args:
            image_path: Path to image file
            table_region: Table region dictionary with coordinates
        
        Returns:
            Dictionary with table structure details
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                return {'rows': 0, 'columns': 0, 'cells': []}
            
            # Extract table region
            x, y, w, h = table_region['x'], table_region['y'], table_region['width'], table_region['height']
            table_img = image[y:y+h, x:x+w]
            
            # Convert to grayscale
            gray = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
            
            # Preprocess
            binary = self._preprocess_for_tables(gray)
            
            # Detect lines
            h_lines = self._detect_horizontal_lines(binary)
            v_lines = self._detect_vertical_lines(binary)
            
            # Find row and column boundaries
            rows = self._find_rows(h_lines)
            columns = self._find_columns(v_lines)
            
            # Extract cell coordinates
            cells = self._extract_cells(rows, columns, table_region)
            
            logger.info(f"Extracted table structure: {len(rows)} rows, {len(columns)} columns")
            
            return {
                'rows': len(rows),
                'columns': len(columns),
                'cells': cells,
                'row_boundaries': rows,
                'column_boundaries': columns
            }
            
        except Exception as e:
            logger.error(f"Table structure extraction failed: {e}")
            return {'rows': 0, 'columns': 0, 'cells': []}
    
    def _find_rows(self, h_lines: np.ndarray) -> List[int]:
        """
        Find row boundaries from horizontal lines
        
        Args:
            h_lines: Horizontal lines image
        
        Returns:
            List of y-coordinates for row boundaries
        """
        # Sum pixels horizontally to find strong horizontal lines
        h_projection = np.sum(h_lines, axis=1)
        
        # Find peaks (row boundaries)
        threshold = np.max(h_projection) * 0.5
        rows = []
        
        for i, value in enumerate(h_projection):
            if value > threshold:
                # Add if not too close to previous row
                if not rows or i - rows[-1] > 10:
                    rows.append(i)
        
        return rows
    
    def _find_columns(self, v_lines: np.ndarray) -> List[int]:
        """
        Find column boundaries from vertical lines
        
        Args:
            v_lines: Vertical lines image
        
        Returns:
            List of x-coordinates for column boundaries
        """
        # Sum pixels vertically to find strong vertical lines
        v_projection = np.sum(v_lines, axis=0)
        
        # Find peaks (column boundaries)
        threshold = np.max(v_projection) * 0.5
        columns = []
        
        for i, value in enumerate(v_projection):
            if value > threshold:
                # Add if not too close to previous column
                if not columns or i - columns[-1] > 10:
                    columns.append(i)
        
        return columns
    
    def _extract_cells(
        self,
        rows: List[int],
        columns: List[int],
        table_region: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Extract individual cell coordinates from row/column boundaries
        
        Args:
            rows: List of row y-coordinates
            columns: List of column x-coordinates
            table_region: Table region info
        
        Returns:
            List of cell dictionaries with coordinates
        """
        cells = []
        offset_x = table_region['x']
        offset_y = table_region['y']
        
        for i in range(len(rows) - 1):
            for j in range(len(columns) - 1):
                cell = {
                    'row': i,
                    'column': j,
                    'x': offset_x + columns[j],
                    'y': offset_y + rows[i],
                    'width': columns[j + 1] - columns[j],
                    'height': rows[i + 1] - rows[i]
                }
                cells.append(cell)
        
        return cells
    
    def enhance_table_image(self, image_path: str, output_path: Optional[str] = None) -> str:
        """
        Enhance image for better table OCR
        
        Applies:
        - Contrast enhancement
        - Noise reduction
        - Rotation correction (deskew)
        - Border removal
        
        Args:
            image_path: Input image path
            output_path: Output path (if None, uses temp file)
        
        Returns:
            Path to enhanced image
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                logger.error(f"Failed to read image: {image_path}")
                return image_path
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 1. Deskew (rotation correction)
            deskewed = self._deskew_image(gray)
            
            # 2. Enhance contrast
            enhanced = cv2.equalizeHist(deskewed)
            
            # 3. Denoise
            denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
            
            # 4. Sharpen
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            # Save enhanced image
            if output_path is None:
                output_path = str(Path(image_path).stem) + '_enhanced.png'
            
            cv2.imwrite(output_path, sharpened)
            logger.info(f"Enhanced table image saved: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Image enhancement failed: {e}")
            return image_path
    
    def _deskew_image(self, gray_image: np.ndarray) -> np.ndarray:
        """
        Correct image rotation (deskew)
        
        Args:
            gray_image: Grayscale input image
        
        Returns:
            Deskewed image
        """
        # Apply threshold
        thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Find coordinates of all non-zero points
        coords = np.column_stack(np.where(thresh > 0))
        
        if len(coords) < 100:
            # Not enough points to determine angle
            return gray_image
        
        # Find minimum area rectangle
        angle = cv2.minAreaRect(coords)[-1]
        
        # Adjust angle (fix: only apply small corrections)
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        # Only rotate if angle is small (0.5 to 5 degrees)
        # Ignore large angles as they're likely false positives
        if 0.5 < abs(angle) < 5:
            (h, w) = gray_image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(gray_image, M, (w, h), 
                                     flags=cv2.INTER_CUBIC, 
                                     borderMode=cv2.BORDER_REPLICATE)
            logger.info(f"Image deskewed by {angle:.2f} degrees")
            return rotated
        elif abs(angle) >= 5:
            logger.info(f"Skipping deskew: angle too large ({angle:.2f} degrees, likely false positive)")
        
        return gray_image
