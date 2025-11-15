"""
Excel search utility for searching records by name or ID.
"""

import os
import pandas as pd
from typing import Optional, List, Dict, Any
from pathlib import Path


class ExcelSearch:
    """Search utility for Excel files."""
    
    def __init__(self, excel_file_path: Optional[str] = None):
        """
        Initialize the Excel search utility.
        
        Args:
            excel_file_path: Path to the Excel file. If None, looks for 'data/contratos_icetex.xlsx' in project root.
        """
        if excel_file_path is None:
            # Default to 'data/contratos_icetex.xlsx' in project root
            project_root = Path(__file__).parent.parent
            excel_file_path = project_root / "data" / "contratos_icetex.xlsx"
        
        self.excel_file_path = Path(excel_file_path)
        self.df = None
        self._load_excel()
    
    def _load_excel(self):
        """Load the Excel file into a DataFrame."""
        if not self.excel_file_path.exists():
            # Use relative path for error message if possible, otherwise use full path
            try:
                relative_path = self.excel_file_path.relative_to(Path.cwd())
                path_display = str(relative_path)
            except ValueError:
                # Path is not relative to current directory, use full path
                path_display = str(self.excel_file_path)
            
            raise FileNotFoundError(
                f"Excel file not found at: {path_display}\n"
                f"Please place your Excel file at: data/contratos_icetex.xlsx "
                f"(relative to the project root) or set EXCEL_FILE_PATH environment variable."
            )
        
        try:
            # Try reading as .xlsx first
            if self.excel_file_path.suffix.lower() in ['.xlsx', '.xls']:
                self.df = pd.read_excel(self.excel_file_path, engine='openpyxl')
            else:
                # Try CSV as fallback
                self.df = pd.read_csv(self.excel_file_path)
            
            # Store original dtypes for reference
            self.original_dtypes = self.df.dtypes.to_dict()
            
            print(f"✅ Excel file loaded successfully: {len(self.df)} rows, {len(self.df.columns)} columns")
            
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")
    
    def reload(self):
        """Reload the Excel file from disk."""
        self._load_excel()
    
    def search_by_name_or_id(
        self, 
        search_term: str, 
        name_columns: Optional[List[str]] = None,
        id_columns: Optional[List[str]] = None,
        case_sensitive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search for records by name or ID.
        
        Args:
            search_term: The search term (name or ID)
            name_columns: List of column names to search in for names
            id_columns: List of column names to search in for IDs
            case_sensitive: Whether the search should be case-sensitive
            
        Returns:
            List of matching records as dictionaries
        """
        if self.df is None or self.df.empty:
            return []
        
        # Auto-detect columns if not provided
        if name_columns is None:
            name_columns = self._detect_name_columns()
        
        if id_columns is None:
            id_columns = self._detect_id_columns()
        
        # Convert search term based on case sensitivity
        search_term_lower = search_term.lower() if not case_sensitive else search_term
        
        # Search in all relevant columns
        mask = pd.Series([False] * len(self.df))
        
        # Search in name columns
        for col in name_columns:
            if col in self.df.columns:
                if case_sensitive:
                    mask = mask | self.df[col].astype(str).str.contains(search_term, na=False, regex=False)
                else:
                    mask = mask | self.df[col].astype(str).str.lower().str.contains(search_term_lower, na=False, regex=False)
        
        # Search in ID columns (exact match preferred)
        for col in id_columns:
            if col in self.df.columns:
                # Try exact match first, then partial match
                if case_sensitive:
                    exact_match = self.df[col].astype(str) == search_term
                    partial_match = self.df[col].astype(str).str.contains(search_term, na=False, regex=False)
                else:
                    exact_match = self.df[col].astype(str).str.lower() == search_term_lower
                    partial_match = self.df[col].astype(str).str.lower().str.contains(search_term_lower, na=False, regex=False)
                
                mask = mask | exact_match | partial_match
        
        # Filter results
        results_df = self.df[mask]
        
        # Convert to list of dictionaries
        results = results_df.to_dict('records')
        
        # Convert numpy types to Python native types for JSON serialization
        for record in results:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif pd.api.types.is_integer_dtype(type(value)):
                    record[key] = int(value) if not pd.isna(value) else None
                elif pd.api.types.is_float_dtype(type(value)):
                    record[key] = float(value) if not pd.isna(value) else None
        
        return results
    
    def _detect_name_columns(self) -> List[str]:
        """Auto-detect columns that might contain names."""
        # Based on the user's Excel structure
        common_name_keywords = [
            'nombre', 'name', 'apellido', 'surname', 'completo', 'full',
            'primer', 'segundo', 'primer_nombre', 'segundo_nombre',
            'razon social', 'razón social', 'representante legal'
        ]
        
        detected = []
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in common_name_keywords):
                detected.append(col)
        
        # If no matches, return first few text columns
        if not detected:
            text_cols = self.df.select_dtypes(include=['object']).columns.tolist()
            detected = text_cols[:3] if len(text_cols) >= 3 else text_cols
        
        return detected if detected else [self.df.columns[0]]
    
    def _detect_id_columns(self) -> List[str]:
        """Auto-detect columns that might contain IDs."""
        # Based on the user's Excel structure
        common_id_keywords = [
            'id', 'cedula', 'cedula_ciudadania', 'cédula', 'documento', 'document', 
            'numero', 'número', 'numero_documento', 'identificacion', 'identificación',
            'dni', 'pasaporte', 'nit'
        ]
        
        detected = []
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(keyword in col_lower for keyword in common_id_keywords):
                detected.append(col)
        
        return detected if detected else []
    
    def get_all_columns(self) -> List[str]:
        """Get list of all column names in the Excel file."""
        if self.df is None:
            return []
        return self.df.columns.tolist()
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the loaded Excel file."""
        if self.df is None:
            return {
                "file_exists": False,
                "rows": 0,
                "columns": []
            }
        
        return {
            "file_exists": True,
            "file_path": str(self.excel_file_path),
            "rows": len(self.df),
            "columns": self.get_all_columns(),
            "name_columns": self._detect_name_columns(),
            "id_columns": self._detect_id_columns()
        }

