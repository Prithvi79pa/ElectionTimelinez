# Election Assistant

An interactive web application that helps users understand the election process, timelines, and steps in an easy-to-follow way.

## Features

- **Personalized Timeline**: View election dates and deadlines customized for your state
- **Step-by-Step Guide**: Clear instructions for voter registration and voting
- **State-Specific Information**: Rules, requirements, and resources for all 50 states
- **Interactive Progress Tracking**: Keep track of completed steps
- **FAQ Section**: Answers to common questions about voting
- **Accessibility**: WCAG 2.1 AA compliant, mobile-responsive design

## Quick Start

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
election-assistant/
├── app/
│   ├── services/          # Business logic
│   ├── static/           # CSS, JavaScript, images
│   ├── templates/        # HTML templates
│   └── routes.py         # Flask routes
├── data/
│   ├── elections/        # Election data
│   ├── states/          # State-specific rules
│   ├── content/         # Educational content
│   └── quizzes/         # Quiz questions
├── app.py               # Application entry point
├── config.py            # Configuration
└── requirements.txt     # Dependencies
```

## Usage

### Select Your State
1. On the homepage, select your state from the dropdown
2. View personalized timeline and requirements

### View Timeline
- See all key election dates
- Get countdown to important deadlines
- View your next recommended action

### Learn How to Vote
- Follow step-by-step registration process
- Understand voting methods (in-person, early, mail-in)
- Find your polling place

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Storage**: JSON files
- **Design**: Mobile-first, responsive, accessible

## Important Notice

This is an educational tool. Election rules and dates can vary by jurisdiction and may change. Always verify information with your local election office or official state website before taking action.

## License

For educational purposes only.
