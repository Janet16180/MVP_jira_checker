import os
import openai
import logging
import json

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("Missing OPENAI_API_KEY environment variable")
    
    def analyze_ticket_quality(self, ticket_data):
        """Analyze ticket quality using GPT-4"""
        prompt = self._build_analysis_prompt(ticket_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert in agile development and ticket quality assessment. Analyze the given Jira ticket and provide structured feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            return self._parse_ai_response(response.choices[0].message.content)
            
        except Exception as e:
            logging.error(f"Error analyzing ticket with AI: {str(e)}")
            raise
    
    def _build_analysis_prompt(self, ticket_data):
        """Build the prompt for AI analysis"""
        return f"""
        Analyze this Jira ticket for quality and completeness:
        
        Title: {ticket_data['summary']}
        Description: {ticket_data['description']}
        Issue Type: {ticket_data['issue_type']}
        
        Please evaluate the ticket based on these criteria:
        1. Clarity: Is the requirement clear and understandable?
        2. Completeness: Does it include sufficient detail for implementation?
        3. Acceptance Criteria: Are there clear acceptance criteria or definition of done?
        4. Context: Is there enough context/background provided?
        5. Actionability: Can a developer start working on this immediately?
        
        Respond in JSON format with:
        {{
            "quality_score": (1-10),
            "is_acceptable": (true/false),
            "issues": ["list of specific issues found"],
            "suggestions": ["list of specific improvement suggestions"],
            "summary": "brief summary of the analysis"
        }}
        """
    
    def _parse_ai_response(self, response_text):
        """Parse AI response and extract structured data"""
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            json_str = response_text[start_idx:end_idx]
            
            return json.loads(json_str)
        except Exception as e:
            logging.error(f"Error parsing AI response: {str(e)}")
            # Return default response if parsing fails
            return {
                "quality_score": 5,
                "is_acceptable": False,
                "issues": ["Unable to analyze ticket properly"],
                "suggestions": ["Please review ticket description and add more details"],
                "summary": "Analysis failed - manual review required"
            }