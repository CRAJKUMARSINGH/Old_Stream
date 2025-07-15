from typing import Any, Union
import locale
from datetime import datetime

# Set locale for Indian numbering (if available)
try:
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    except:
        pass

def format_number(value: Any, decimals: int = 2) -> str:
    """Format number with specified decimal places"""
    try:
        if value is None:
            return "0.00" if decimals > 0 else "0"
        
        if isinstance(value, (int, float)):
            if decimals == 0:
                return f"{int(round(value))}"
            else:
                return f"{value:.{decimals}f}"
        elif isinstance(value, str):
            if decimals == 0:
                return f"{int(round(float(value)))}"
            else:
                return f"{float(value):.{decimals}f}"
    except:
        pass
    
    return "0.00" if decimals > 0 else "0"

def format_currency(value: Any, symbol: str = "₹") -> str:
    """Format currency with Indian numbering system"""
    try:
        if value is None:
            return f"{symbol}0.00"
        
        if isinstance(value, (int, float)):
            # Use Indian numbering system
            return f"{symbol}{value:,.2f}"
        elif isinstance(value, str):
            return f"{symbol}{float(value):,.2f}"
    except:
        pass
    
    return f"{symbol}0.00"

def format_date(date_input: Union[str, datetime], output_format: str = '%d/%m/%Y') -> str:
    """Format date to specified format (default: dd/mm/yyyy)"""
    try:
        if date_input is None or date_input == '':
            return 'N/A'
        
        if isinstance(date_input, datetime):
            return date_input.strftime(output_format)
        
        if isinstance(date_input, str):
            if date_input.lower() in ['n/a', 'na', 'not applicable', '']:
                return 'N/A'
            
            # Try to parse different date formats
            input_formats = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%d-%m-%Y',
                '%Y/%m/%d',
                '%m/%d/%Y',
                '%d.%m.%Y',
                '%Y.%m.%d'
            ]
            
            for fmt in input_formats:
                try:
                    parsed_date = datetime.strptime(date_input.strip(), fmt)
                    return parsed_date.strftime(output_format)
                except:
                    continue
    except:
        pass
    
    return str(date_input) if date_input else 'N/A'

def format_percentage(value: Any, decimals: int = 2) -> str:
    """Format percentage with specified decimal places"""
    try:
        if value is None:
            return "0.00%"
        
        if isinstance(value, (int, float)):
            return f"{value:.{decimals}f}%"
        elif isinstance(value, str):
            return f"{float(value):.{decimals}f}%"
    except:
        pass
    
    return "0.00%"

def format_indian_number(value: Any) -> str:
    """Format number according to Indian numbering system (lakhs, crores)"""
    try:
        if value is None:
            return "0"
        
        num = float(value)
        
        if num >= 10000000:  # 1 crore
            return f"{num/10000000:.2f} Cr"
        elif num >= 100000:  # 1 lakh
            return f"{num/100000:.2f} L"
        elif num >= 1000:    # 1 thousand
            return f"{num/1000:.2f} K"
        else:
            return f"{num:.2f}"
    except:
        pass
    
    return "0"

def number_to_words(value: Any) -> str:
    """Convert number to words (Indian format)"""
    try:
        if value is None:
            return "Zero"
        
        num = int(float(value))
        
        if num == 0:
            return "Zero"
        
        # Basic implementation for small numbers
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        
        def convert_hundreds(n):
            result = ""
            if n >= 100:
                result += ones[n // 100] + " Hundred "
                n %= 100
            
            if n >= 20:
                result += tens[n // 10] + " "
                n %= 10
            elif n >= 10:
                result += teens[n - 10] + " "
                n = 0
            
            if n > 0:
                result += ones[n] + " "
            
            return result
        
        if num < 1000:
            return convert_hundreds(num).strip()
        elif num < 100000:
            thousands = num // 1000
            remainder = num % 1000
            result = convert_hundreds(thousands) + "Thousand "
            if remainder > 0:
                result += convert_hundreds(remainder)
            return result.strip()
        elif num < 10000000:
            lakhs = num // 100000
            remainder = num % 100000
            result = convert_hundreds(lakhs) + "Lakh "
            if remainder > 0:
                if remainder >= 1000:
                    result += convert_hundreds(remainder // 1000) + "Thousand "
                    remainder %= 1000
                if remainder > 0:
                    result += convert_hundreds(remainder)
            return result.strip()
        else:
            crores = num // 10000000
            remainder = num % 10000000
            result = convert_hundreds(crores) + "Crore "
            if remainder > 0:
                if remainder >= 100000:
                    result += convert_hundreds(remainder // 100000) + "Lakh "
                    remainder %= 100000
                if remainder >= 1000:
                    result += convert_hundreds(remainder // 1000) + "Thousand "
                    remainder %= 1000
                if remainder > 0:
                    result += convert_hundreds(remainder)
            return result.strip()
    
    except:
        pass
    
    return "Zero"

def round_to_even(value: Any) -> int:
    """Round to nearest even number (used for GST)"""
    try:
        num = float(value)
        rounded = round(num)
        if rounded % 2 != 0:
            rounded += 1
        return rounded
    except:
        pass
    
    return 0

def safe_divide(numerator: Any, denominator: Any, default: float = 0.0) -> float:
    """Safely divide two numbers with default fallback"""
    try:
        num = float(numerator)
        den = float(denominator)
        if den != 0:
            return num / den
    except:
        pass
    
    return default

def calculate_percentage(part: Any, total: Any, decimals: int = 2) -> float:
    """Calculate percentage with safe division"""
    try:
        part_val = float(part)
        total_val = float(total)
        if total_val != 0:
            return round((part_val / total_val) * 100, decimals)
    except:
        pass
    
    return 0.0
