import logging
from .jira_service import JiraService

class TicketValidator:
    def __init__(self, ai_service, email_service):
        self.ai_service = ai_service
        self.email_service = email_service
        self.jira_service = JiraService()
        
        # Quality threshold for MVP (can be configurable later)
        self.quality_threshold = 6
    
    def validate_ticket(self, issue_key):
        """Main validation logic for a ticket"""
        try:
            # Get ticket data from Jira
            ticket_data = self.jira_service.get_issue(issue_key)
            logging.info(f"Validating ticket: {issue_key}")
            
            # Analyze ticket quality with AI
            analysis_result = self.ai_service.analyze_ticket_quality(ticket_data)
            
            # Check if ticket needs improvement
            if not analysis_result['is_acceptable'] or analysis_result['quality_score'] < self.quality_threshold:
                # Send feedback emails
                self._send_improvement_notifications(ticket_data, analysis_result)
                
                return {
                    "status": "needs_improvement",
                    "ticket_key": issue_key,
                    "quality_score": analysis_result['quality_score'],
                    "analysis": analysis_result,
                    "notifications_sent": True
                }
            else:
                logging.info(f"Ticket {issue_key} meets quality standards")
                return {
                    "status": "acceptable",
                    "ticket_key": issue_key,
                    "quality_score": analysis_result['quality_score'],
                    "analysis": analysis_result,
                    "notifications_sent": False
                }
                
        except Exception as e:
            logging.error(f"Error validating ticket {issue_key}: {str(e)}")
            raise
    
    def _send_improvement_notifications(self, ticket_data, analysis_result):
        """Send notification emails to relevant parties"""
        try:
            # Build recipient list
            recipients = [ticket_data['reporter']]
            
            # Add Scrum Master
            scrum_master_email = self.jira_service.get_scrum_master_email(ticket_data['project_key'])
            if scrum_master_email:
                recipients.append(scrum_master_email)
            
            # Send email
            success = self.email_service.send_ticket_feedback(
                ticket_data, 
                analysis_result, 
                recipients
            )
            
            if success:
                logging.info(f"Improvement notifications sent for ticket {ticket_data['key']}")
            else:
                logging.warning(f"Failed to send notifications for ticket {ticket_data['key']}")
                
        except Exception as e:
            logging.error(f"Error sending improvement notifications: {str(e)}")
            # Don't raise - notification failure shouldn't break validation