# Jira Ticket Quality Checker MVP

An intelligent system that automatically validates Jira ticket quality using AI and sends improvement suggestions to team members.

## Features

- **Automatic Validation**: Analyzes tickets when created/updated via Jira webhooks
- **AI-Powered Analysis**: Uses GPT-4 to evaluate ticket quality, clarity, and completeness
- **Smart Notifications**: Sends improvement suggestions to ticket creators and Scrum Masters
- **Manual Validation**: API endpoint for testing specific tickets
- **Configurable Quality Thresholds**: Adjustable quality standards

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Set up Jira Webhook**
   - Go to Jira → System → Webhooks
   - Create webhook pointing to: `http://your-server:5000/webhook`
   - Select events: Issue Created, Issue Updated

## API Endpoints

- `POST /webhook` - Jira webhook endpoint
- `POST /validate/<issue-key>` - Manual ticket validation
- `GET /health` - Health check

## Configuration

Required environment variables:
- `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`
- `OPENAI_API_KEY`
- `SCRUM_MASTER_EMAIL`

Optional (for email notifications):
- `SMTP_SERVER`, `SMTP_PORT`, `EMAIL_USERNAME`, `EMAIL_PASSWORD`

## Quality Criteria

The AI evaluates tickets based on:
- **Clarity**: Clear and understandable requirements
- **Completeness**: Sufficient detail for implementation  
- **Acceptance Criteria**: Clear definition of done
- **Context**: Adequate background information
- **Actionability**: Ready for development work

Tickets scoring below 6/10 trigger improvement notifications.

## Testing

Test with a specific ticket:
```bash
curl -X POST http://localhost:5000/validate/PROJ-123
```