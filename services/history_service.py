import json
import os
from datetime import datetime

HISTORY_FILE = os.path.join('storage', 'history.json')

def save_history(filename, result):
    """
    Save file processing history with additional metadata
    """
    if not os.path.exists('storage'):
        os.makedirs('storage')

    try:
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []

        # Create history entry with metadata
        entry = {
            'filename': filename,
            'processed_at': datetime.now().isoformat(),
            'result': result,
            'pages': result.get('pages', []),
            'extracted_fields': {
                'invoice_number': result.get('pages', [{}])[0].get('fields', {}).get('invoice_number'),
                'date': result.get('pages', [{}])[0].get('fields', {}).get('date'),
                'total': result.get('pages', [{}])[0].get('fields', {}).get('total'),
                'amount': result.get('pages', [{}])[0].get('fields', {}).get('amount'),
                'vendor': result.get('pages', [{}])[0].get('fields', {}).get('vendor'),
                'description': result.get('pages', [{}])[0].get('fields', {}).get('description')
            },
            'file_type': filename.split('.')[-1].lower(),
            'page_count': len(result.get('pages', [])),
            'text_length': sum(len(page.get('text', '')) for page in result.get('pages', []))
        }

        history.append(entry)

        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)

    except Exception as e:
        raise Exception(f"Failed to save history: {str(e)}")

def load_history():
    """
    Load file processing history with additional filtering capabilities
    """
    try:
        if not os.path.exists(HISTORY_FILE):
            return []

        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
            
        # Validate the history structure
        if not isinstance(history, list):
            raise ValueError("Invalid history file format")
            
        # Clean up any invalid entries
        cleaned_history = []
        for entry in history:
            try:
                # Validate required fields
                if not isinstance(entry, dict):
                    continue
                
                # Add default values for missing fields
                entry.setdefault('file_type', 'unknown')
                entry.setdefault('page_count', 0)
                entry.setdefault('text_length', 0)
                entry.setdefault('extracted_fields', {})
                entry.setdefault('pages', [])
                
                cleaned_history.append(entry)
            except Exception as e:
                print(f"Warning: Skipping invalid history entry: {str(e)}")
                continue
                
        # Sort by processed_at in descending order
        cleaned_history.sort(key=lambda x: x['processed_at'], reverse=True)
        return cleaned_history
    except Exception as e:
        print(f"Error loading history: {str(e)}")
        return []
