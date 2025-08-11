import re
from typing import Dict, List
import json
from pathlib import Path

class FieldGuesser:
    """Class to guess field types using pattern matching"""
    
    def __init__(self):
        """Initialize with default patterns"""
        self.patterns = {
            'invoice_number': [
                r'invoice\s*#?\s*(\d+)',
                r'inv\.?\s*#?\s*(\d+)',
                r'bill\s*#?\s*(\d+)',
                r'\b\d{4,}\b'  # Generic number pattern
            ],
            'date': [
                r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
                r'\b\d{1,2}-\d{1,2}-\d{2,4}\b',
                r'\b\d{4}-\d{1,2}-\d{1,2}\b',
                r'\b\d{1,2}\s+[a-z]{3}\s+\d{4}\b',  # e.g., 15 Aug 2025
                r'\b[a-z]{3}\s+\d{1,2},\s+\d{4}\b'  # e.g., Aug 15, 2025
            ],
            'amount': [
                r'\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'PKR\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
                r'\b\d+(?:\.\d{2})?\b'  # Generic number pattern
            ],
            'email': [
                r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            ],
            'phone': [
                r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                r'\d{10}'  # Generic 10-digit phone number
            ]
        }
        
        # Load custom patterns from file if available
        self.load_custom_patterns()
        
    def load_custom_patterns(self):
        """Load custom patterns from JSON file"""
        try:
            pattern_file = Path('patterns.json')
            if pattern_file.exists():
                with open(pattern_file, 'r') as f:
                    custom_patterns = json.load(f)
                    self.patterns.update(custom_patterns)
        except Exception as e:
            print(f"Warning: Failed to load custom patterns: {str(e)}")
            
    def save_custom_patterns(self):
        """Save custom patterns to JSON file"""
        try:
            with open('patterns.json', 'w') as f:
                json.dump(self.patterns, f, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save patterns: {str(e)}")
            
    def add_custom_pattern(self, field_name: str, pattern: str):
        """Add a custom pattern for a field"""
        if field_name not in self.patterns:
            self.patterns[field_name] = []
        self.patterns[field_name].append(pattern)
        self.save_custom_patterns()
        
    def guess_fields(self, text: str) -> Dict[str, List[str]]:
        """
        Guess fields from text using pattern matching
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary of field names and their possible values
        """
        results = {}
        
        # Try each pattern for each field
        for field_name, patterns in self.patterns.items():
            matches = []
            for pattern in patterns:
                # Find all matches in text
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    value = match.group(0).strip()
                    # Clean up the value
                    value = re.sub(r'[\s,]+', '', value)  # Remove spaces and commas
                    if value not in matches:
                        matches.append(value)
            
            if matches:
                results[field_name] = matches
                
        return results

def get_field_guesser():
    """Singleton pattern to get FieldGuesser instance"""
    if not hasattr(get_field_guesser, "instance"):
        get_field_guesser.instance = FieldGuesser()
    return get_field_guesser.instance
