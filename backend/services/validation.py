import re
import phonenumbers
from phonenumbers import NumberParseException
from email_validator import validate_email, EmailNotValidError
from typing import Tuple, Optional

class ValidationService:
    """Service for validating user input data"""
    
    @staticmethod
    def validate_email_format(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        try:
            # Validate and get normalized result
            valid = validate_email(email)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    @staticmethod
    def validate_phone_number(phone: str, country_code: str) -> Tuple[bool, str]:
        """Validate phone number format"""
        if not phone:
            return True, ""  # Phone is optional
        
        try:
            # Remove any non-digit characters except +
            cleaned_phone = re.sub(r'[^\d+]', '', phone)
            
            # If phone doesn't start with +, prepend country code
            if not cleaned_phone.startswith('+'):
                # Map common country codes
                country_mapping = {
                    'US': '+1', 'CA': '+1', 'GB': '+44', 'FR': '+33', 'DE': '+49',
                    'IT': '+39', 'ES': '+34', 'AU': '+61', 'JP': '+81', 'CN': '+86',
                    'IN': '+91', 'BR': '+55', 'MX': '+52', 'RU': '+7', 'KR': '+82'
                }
                
                prefix = country_mapping.get(country_code, '+1')
                cleaned_phone = prefix + cleaned_phone
            
            # Parse the phone number
            parsed_number = phonenumbers.parse(cleaned_phone, None)
            
            # Check if it's valid
            if phonenumbers.is_valid_number(parsed_number):
                # Format in international format
                formatted = phonenumbers.format_number(
                    parsed_number, 
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
                return True, formatted
            else:
                return False, "Invalid phone number format"
                
        except NumberParseException as e:
            return False, f"Phone number parsing error: {e}"
        except Exception as e:
            return False, f"Phone validation error: {e}"
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate full name"""
        if not name or not name.strip():
            return False, "Name is required"
        
        name = name.strip()
        
        # Check minimum length
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        
        # Check maximum length
        if len(name) > 100:
            return False, "Name must be less than 100 characters"
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-ZÀ-ÿ\s\-'\.]+$", name):
            return False, "Name contains invalid characters"
        
        # Check for reasonable format (at least one letter)
        if not re.search(r'[a-zA-ZÀ-ÿ]', name):
            return False, "Name must contain at least one letter"
        
        return True, name
    
    @staticmethod
    def validate_message(message: str) -> Tuple[bool, str]:
        """Validate message content"""
        if not message or not message.strip():
            return False, "Message is required"
        
        message = message.strip()
        
        # Check minimum length
        if len(message) < 10:
            return False, "Message must be at least 10 characters long"
        
        # Check maximum length
        if len(message) > 5000:
            return False, "Message must be less than 5000 characters"
        
        return True, message
    
    @staticmethod
    def validate_country_code(country_code: str) -> Tuple[bool, str]:
        """Validate country code"""
        if not country_code or not country_code.strip():
            return False, "Country code is required"
        
        country_code = country_code.strip().upper()
        
        # List of valid ISO 3166-1 alpha-2 country codes (subset)
        valid_codes = {
            'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT',
            'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI',
            'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY',
            'BZ', 'CA', 'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN',
            'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 'DJ', 'DK', 'DM',
            'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK',
            'FM', 'FO', 'FR', 'GA', 'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL',
            'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK', 'HM',
            'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT',
            'JE', 'JM', 'JO', 'JP', 'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR',
            'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT', 'LU',
            'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM',
            'MN', 'MO', 'MP', 'MQ', 'MR', 'MS', 'MT', 'MU', 'MV', 'MW', 'MX', 'MY',
            'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU',
            'NZ', 'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR',
            'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS', 'RU', 'RW', 'SA', 'SB',
            'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO',
            'SR', 'SS', 'ST', 'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH',
            'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW', 'TZ', 'UA',
            'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU',
            'WF', 'WS', 'YE', 'YT', 'ZA', 'ZM', 'ZW'
        }
        
        if country_code not in valid_codes:
            return False, "Invalid country code"
        
        return True, country_code
