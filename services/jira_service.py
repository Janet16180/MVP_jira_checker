import os
from atlassian import Jira
import logging

class JiraService:
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_username = os.getenv('JIRA_USERNAME')
        self.jira_api_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.jira_url, self.jira_username, self.jira_api_token]):
            raise ValueError("Missing required Jira configuration")
            
        self.jira = Jira(
            url=self.jira_url,
            username=self.jira_username,
            password=self.jira_api_token
        )
    
    def get_issue(self, issue_key):
        """Get issue details from Jira"""
        try:
            issue = self.jira.issue(issue_key)
            return {
                'key': issue_key,
                'summary': issue['fields']['summary'],
                'description': issue['fields']['description'] or '',
                'issue_type': issue['fields']['issuetype']['name'],
                'reporter': issue['fields']['reporter']['emailAddress'],
                'assignee': issue['fields']['assignee']['emailAddress'] if issue['fields']['assignee'] else None,
                'project_key': issue['fields']['project']['key']
            }
        except Exception as e:
            logging.error(f"Error fetching issue {issue_key}: {str(e)}")
            raise
    
    def get_scrum_master_email(self, project_key):
        """Get Scrum Master email for the project"""
        # For MVP, we'll use environment variable
        # In production, this could query project roles or team configuration
        return os.getenv('SCRUM_MASTER_EMAIL', 'scrum.master@company.com')