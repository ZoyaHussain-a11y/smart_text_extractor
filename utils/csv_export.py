import csv
from datetime import datetime
import os
from typing import List, Dict, Union

def export_to_csv(data: List[Dict], filename: str = None, write_to_file: bool = True) -> Union[str, List[str]]:
    """
    Export extracted data to CSV format
    
    Args:
        data: List of dictionaries containing extracted data
        filename: Optional output filename
    
    Returns:
        Path to the created CSV file
    """
    # Get all unique field names from the data
    field_names = set()
    # Add all possible fields
    field_names.update([
        'filename', 'processed_at', 'file_type', 'page_count', 'text_length',
        'invoice_number', 'date', 'total', 'amount', 'vendor', 'description',
        'page', 'text'
    ])
    
    # Add any additional field names from the data
    for item in data:
        field_names.update(item.get('extracted_fields', {}).keys())
        for page in item.get('pages', []):
            field_names.update(page.get('fields', {}).keys())
    
    # Sort field names
    field_names = sorted(list(field_names))
    
    if write_to_file:
        if not filename:
            filename = f"extracted_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Create CSV file
        csv_path = os.path.join('exports', filename)
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            
            for item in data:
                # Create base row with file-level information
                base_row = {
                    'filename': item.get('filename'),
                    'processed_at': item.get('processed_at'),
                    'file_type': item.get('file_type'),
                    'page_count': item.get('page_count'),
                    'text_length': item.get('text_length'),
                    **item.get('extracted_fields', {})
                }
                
                # Write a row for each page
                for page in item.get('pages', []):
                    row = base_row.copy()
                    row.update({
                        'page': page.get('page'),
                        'text': page.get('text', '')[:1000],  # Limit text length to 1000 chars
                        **page.get('fields', {})
                    })
                    writer.writerow(row)
        
        return csv_path
    else:
        output = []
        for item in data:
            # Create base row with file-level information
            base_row = {
                'filename': item.get('filename'),
                'processed_at': item.get('processed_at'),
                'file_type': item.get('file_type'),
                'page_count': item.get('page_count'),
                'text_length': item.get('text_length'),
                **item.get('extracted_fields', {})
            }
            
            # Write a row for each page
            for page in item.get('pages', []):
                row = base_row.copy()
                row.update({
                    'page': page.get('page'),
                    'text': page.get('text', '')[:1000],  # Limit text length to 1000 chars
                    **page.get('fields', {})
                })
                writer.writerow(row)
    
    return csv_path
