from flask import Blueprint, jsonify, send_file, make_response, request
from services.history_service import load_history
from utils.auth import require_token
from utils.csv_export import export_to_csv
from io import StringIO
import os

history_bp = Blueprint('history', __name__, url_prefix='/history')

@history_bp.route('/', methods=['GET'])
@require_token
def get_history():
    """Get processing history in JSON format"""
    try:
        return jsonify(load_history()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_bp.route('/export', methods=['GET'])
@require_token
def export_history():
    """Export processing history to CSV or JSON"""
    try:
        history = load_history()
        if not history:
            return jsonify({"error": "No history to export"}), 404
            
        # Check if format parameter is provided
        format = request.args.get('format', 'csv')
        
        if format.lower() == 'json':
            # Return JSON response
            return jsonify(history)
        else:
            # Generate CSV content in memory
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=export_to_csv(history, write_to_file=False))
            writer.writeheader()
            
            # Write data to CSV
            for item in history:
                base_row = {
                    'filename': item.get('filename'),
                    'processed_at': item.get('processed_at'),
                    'file_type': item.get('file_type'),
                    'page_count': item.get('page_count'),
                    'text_length': item.get('text_length'),
                    **item.get('extracted_fields', {})
                }
                
                for page in item.get('pages', []):
                    row = base_row.copy()
                    row.update({
                        'page': page.get('page'),
                        'text': page.get('text', '')[:1000],
                        **page.get('fields', {})
                    })
                    writer.writerow(row)
            
            # Get the CSV content
            csv_content = output.getvalue()
            
            # Create response with CSV content
            response = make_response(csv_content)
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename=extracted_data.csv'
            return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
