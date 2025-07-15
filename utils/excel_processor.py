import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExcelProcessor:
    """Processes Excel files to extract bill generation data"""
    
    def __init__(self):
        self.file_format = None
        self.title_data = {}
        self.work_order_items = []
        self.bill_quantity_items = []
        self.extra_items = []
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Main method to process Excel file"""
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            
            logger.info(f"Processing file with sheets: {sheet_names}")
            
            # Detect file format
            self.file_format = self._detect_file_format(sheet_names)
            logger.info(f"Detected file format: {self.file_format}")
            
            # Process based on format
            if self.file_format == "New Pattern":
                self._process_new_pattern(excel_file)
            else:
                self._process_old_pattern(excel_file)
            
            # Extract work order and bill quantity data
            self._extract_work_order_data(excel_file)
            self._extract_bill_quantity_data(excel_file)
            
            # Extract extra items if available
            self._extract_extra_items(excel_file)
            
            # Calculate totals
            totals = self._calculate_totals()
            
            return {
                'file_format': self.file_format,
                'title_info': self.title_data,
                'work_order_items': self.work_order_items,
                'bill_quantity_items': self.bill_quantity_items,
                'extra_items': self.extra_items,
                'total_amount': totals['total_amount'],
                'work_order_amount': totals['work_order_amount'],
                'deviation_data': self._calculate_deviation_data(),
                'deductions': self._calculate_deductions(totals['total_amount']),
                'net_payable': self._calculate_net_payable(totals['total_amount'])
            }
            
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            raise
    
    def _detect_file_format(self, sheet_names: List[str]) -> str:
        """Detect if file is Old Pattern or New Pattern with Title sheet"""
        # Check if Title sheet exists (New Pattern)
        if 'Title' in sheet_names:
            return "New Pattern"
        else:
            return "Old Pattern"
    
    def _process_new_pattern(self, excel_file: pd.ExcelFile):
        """Process New Pattern files with Title sheet"""
        try:
            # Read Title sheet
            title_df = excel_file.parse('Title', header=None)
            
            # Extract key information from Title sheet
            self.title_data = self._extract_title_data(title_df)
            
        except Exception as e:
            logger.error(f"Error processing Title sheet: {str(e)}")
            raise
    
    def _process_old_pattern(self, excel_file: pd.ExcelFile):
        """Process Old Pattern files without Title sheet"""
        # For old pattern, we need to extract basic info from other sheets
        # This is a fallback method
        self.title_data = {
            'agreement_no': 'N/A',
            'contractor_name': 'N/A',
            'work_name': 'N/A',
            'work_order_amount': 0,
            'date_of_commencement': 'N/A',
            'date_of_completion': 'N/A',
            'measurement_book_no': 'N/A'
        }
    
    def _extract_title_data(self, title_df: pd.DataFrame) -> Dict[str, Any]:
        """Extract data from Title sheet"""
        title_info = {}
        
        try:
            # Convert DataFrame to dictionary for easier processing
            data_dict = {}
            for index, row in title_df.iterrows():
                if pd.notna(row.iloc[0]) and len(row) > 1 and pd.notna(row.iloc[1]):
                    key = str(row.iloc[0]).strip()
                    value = str(row.iloc[1]).strip()
                    data_dict[key] = value
            
            # Extract specific fields
            title_info['agreement_no'] = data_dict.get('Agreement No.', 'N/A')
            title_info['contractor_name'] = data_dict.get('Name of Contractor', 'N/A')
            title_info['work_name'] = data_dict.get('Name of Work', 'N/A')
            title_info['work_order_amount'] = self._parse_amount(data_dict.get('Work Order Amount', '0'))
            title_info['date_of_commencement'] = data_dict.get('Date of Commencement', 'N/A')
            title_info['date_of_completion'] = data_dict.get('Date of Completion', 'N/A')
            title_info['measurement_book_no'] = data_dict.get('M.B No.', 'N/A')
            title_info['chargeable_head'] = data_dict.get('Chargeable Head', 'N/A')
            title_info['administrative_section'] = data_dict.get('Administrative Section', 'N/A')
            title_info['technical_section'] = data_dict.get('Technical Section', 'N/A')
            title_info['subdivision_name'] = data_dict.get('Name of Sub Division', 'N/A')
            
        except Exception as e:
            logger.error(f"Error extracting title data: {str(e)}")
            # Set default values
            title_info = {
                'agreement_no': 'N/A',
                'contractor_name': 'N/A',
                'work_name': 'N/A',
                'work_order_amount': 0,
                'date_of_commencement': 'N/A',
                'date_of_completion': 'N/A',
                'measurement_book_no': 'N/A'
            }
        
        return title_info
    
    def _extract_work_order_data(self, excel_file: pd.ExcelFile):
        """Extract data from Work Order sheet"""
        try:
            if 'Work Order' in excel_file.sheet_names:
                work_order_df = excel_file.parse('Work Order', header=1)  # Header in row 2
                
                # Process each row
                for index, row in work_order_df.iterrows():
                    # Skip empty rows
                    if row.isna().all():
                        continue
                    
                    # Extract item data (include items with any non-zero quantity)
                    item_data = self._extract_item_data(row, 'work_order')
                    if item_data and item_data['quantity'] > 0:
                        self.work_order_items.append(item_data)
                            
        except Exception as e:
            logger.error(f"Error extracting work order data: {str(e)}")
    
    def _extract_bill_quantity_data(self, excel_file: pd.ExcelFile):
        """Extract data from Bill Quantity sheet"""
        try:
            if 'Bill Quantity' in excel_file.sheet_names:
                bill_quantity_df = excel_file.parse('Bill Quantity', header=1)  # Header in row 2
                
                # Process each row
                for index, row in bill_quantity_df.iterrows():
                    # Skip empty rows
                    if row.isna().all():
                        continue
                    
                    # Extract item data (include items with any non-zero quantity)
                    item_data = self._extract_item_data(row, 'bill_quantity')
                    if item_data and item_data['quantity'] > 0:
                        self.bill_quantity_items.append(item_data)
                            
        except Exception as e:
            logger.error(f"Error extracting bill quantity data: {str(e)}")
    
    def _extract_extra_items(self, excel_file: pd.ExcelFile):
        """Extract extra items data if available"""
        try:
            if 'Extra Items' in excel_file.sheet_names:
                extra_items_df = excel_file.parse('Extra Items', header=1)
                
                # Process each row
                for index, row in extra_items_df.iterrows():
                    # Skip empty rows
                    if row.isna().all():
                        continue
                    
                    # Extract item data (include items with any non-zero quantity)
                    item_data = self._extract_item_data(row, 'extra_items')
                    if item_data and item_data['quantity'] > 0:
                        self.extra_items.append(item_data)
                            
        except Exception as e:
            logger.error(f"Error extracting extra items data: {str(e)}")
    
    def _extract_item_data(self, row: pd.Series, sheet_type: str) -> Optional[Dict[str, Any]]:
        """Extract item data from a row"""
        try:
            # Common structure for all sheet types
            item_data = {
                'item_no': self._safe_get_value(row, 0),
                'description': self._safe_get_value(row, 1),
                'unit': self._safe_get_value(row, 2),
                'quantity': self._safe_get_numeric_value(row, 3),
                'rate': self._safe_get_numeric_value(row, 4),
                'amount': self._safe_get_numeric_value(row, 5)
            }
            
            # Calculate amount if not provided
            if item_data['amount'] == 0 and item_data['quantity'] > 0 and item_data['rate'] > 0:
                item_data['amount'] = item_data['quantity'] * item_data['rate']
            
            # Only include items with non-zero quantities or amounts
            if item_data['quantity'] > 0 or item_data['amount'] > 0:
                return item_data
            
        except Exception as e:
            logger.error(f"Error extracting item data: {str(e)}")
        
        return None
    
    def _safe_get_value(self, row: pd.Series, index: int) -> str:
        """Safely get value from row"""
        try:
            if index < len(row) and pd.notna(row.iloc[index]):
                return str(row.iloc[index]).strip()
        except:
            pass
        return ""
    
    def _safe_get_numeric_value(self, row: pd.Series, index: int) -> float:
        """Safely get numeric value from row"""
        try:
            if index < len(row) and pd.notna(row.iloc[index]):
                value = row.iloc[index]
                if isinstance(value, (int, float)):
                    return float(value)
                elif isinstance(value, str):
                    # Remove commas and convert to float
                    cleaned_value = value.replace(',', '').strip()
                    if cleaned_value:
                        return float(cleaned_value)
        except:
            pass
        return 0.0
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parse amount string to float"""
        try:
            if isinstance(amount_str, (int, float)):
                return float(amount_str)
            elif isinstance(amount_str, str):
                # Remove currency symbols, commas, and convert to float
                cleaned = amount_str.replace('₹', '').replace(',', '').strip()
                if cleaned:
                    return float(cleaned)
        except:
            pass
        return 0.0
    
    def _calculate_totals(self) -> Dict[str, float]:
        """Calculate totals from all items"""
        total_amount = 0.0
        work_order_amount = 0.0
        
        # Sum from bill quantity items
        for item in self.bill_quantity_items:
            total_amount += item.get('amount', 0)
        
        # Sum from extra items
        for item in self.extra_items:
            total_amount += item.get('amount', 0)
        
        # Work order amount from title or work order items
        work_order_amount = self.title_data.get('work_order_amount', 0)
        if work_order_amount == 0:
            for item in self.work_order_items:
                work_order_amount += item.get('amount', 0)
        
        return {
            'total_amount': total_amount,
            'work_order_amount': work_order_amount
        }
    
    def _calculate_deviation_data(self) -> List[Dict[str, Any]]:
        """Calculate deviation data comparing work order vs executed quantities"""
        deviation_data = []
        
        # Create lookup for bill quantities
        bill_lookup = {item.get('item_no', ''): item for item in self.bill_quantity_items}
        
        # Process work order items
        for wo_item in self.work_order_items:
            item_no = wo_item.get('item_no', '')
            bill_item = bill_lookup.get(item_no, {})
            
            wo_qty = wo_item.get('quantity', 0)
            wo_rate = wo_item.get('rate', 0)
            wo_amount = wo_qty * wo_rate
            
            exec_qty = bill_item.get('quantity', 0)
            exec_rate = bill_item.get('rate', wo_rate)
            exec_amount = exec_qty * exec_rate
            
            # Calculate excess/saving
            excess_qty = max(0, exec_qty - wo_qty)
            excess_amount = excess_qty * exec_rate
            
            saving_qty = max(0, wo_qty - exec_qty)
            saving_amount = saving_qty * exec_rate
            
            deviation_data.append({
                'item_no': item_no,
                'description': wo_item.get('description', ''),
                'unit': wo_item.get('unit', ''),
                'wo_quantity': wo_qty,
                'wo_rate': wo_rate,
                'wo_amount': wo_amount,
                'exec_quantity': exec_qty,
                'exec_rate': exec_rate,
                'exec_amount': exec_amount,
                'excess_quantity': excess_qty,
                'excess_amount': excess_amount,
                'saving_quantity': saving_qty,
                'saving_amount': saving_amount
            })
        
        return deviation_data
    
    def _calculate_deductions(self, total_amount: float) -> Dict[str, float]:
        """Calculate statutory deductions"""
        deductions = {
            'sd_rate': 10.0,  # Security Deposit
            'it_rate': 2.0,   # Income Tax
            'gst_rate': 2.0,  # GST
            'lc_rate': 1.0    # Labour Cess
        }
        
        deductions['sd_amount'] = round(total_amount * deductions['sd_rate'] / 100)
        deductions['it_amount'] = round(total_amount * deductions['it_rate'] / 100)
        deductions['gst_amount'] = round(total_amount * deductions['gst_rate'] / 100)
        # Round GST to next even number
        if deductions['gst_amount'] % 2 != 0:
            deductions['gst_amount'] += 1
        deductions['lc_amount'] = round(total_amount * deductions['lc_rate'] / 100)
        
        deductions['total_deductions'] = (
            deductions['sd_amount'] + 
            deductions['it_amount'] + 
            deductions['gst_amount'] + 
            deductions['lc_amount']
        )
        
        return deductions
    
    def _calculate_net_payable(self, total_amount: float) -> float:
        """Calculate net payable amount after deductions"""
        deductions = self._calculate_deductions(total_amount)
        return total_amount - deductions['total_deductions']
