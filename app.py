from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from services.jira_service import JiraService
from services.ai_service import AIService
from services.email_service import EmailService
from services.ticket_validator import TicketValidator
import logging

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize services
jira_service = JiraService()
ai_service = AIService()
email_service = EmailService()
ticket_validator = TicketValidator(ai_service, email_service)

@app.route('/webhook', methods=['POST'])
def jira_webhook():
    """Handle Jira webhook events for ticket creation/updates"""
    try:
        data = request.json
        
        # Check if it's a ticket creation or update event
        if data.get('webhookEvent') in ['jira:issue_created', 'jira:issue_updated']:
            issue_key = data['issue']['key']
            
            # Validate the ticket
            ticket_validator.validate_ticket(issue_key)
            
            return jsonify({"status": "success", "message": "Ticket processed"}), 200
        
        return jsonify({"status": "ignored", "message": "Event not relevant"}), 200
    
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/validate/<issue_key>', methods=['POST'])
def validate_ticket_manual(issue_key):
    """Manual ticket validation endpoint for testing"""
    try:
        result = ticket_validator.validate_ticket(issue_key)
        return jsonify(result), 200
    except Exception as e:
        logging.error(f"Error validating ticket {issue_key}: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)