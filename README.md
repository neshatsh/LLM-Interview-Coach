# LLM Interview Coach

An intelligent interview practice bot that helps data scientists and ML engineers prepare for technical interviews using GPT-4o.

## Features

-  5 interview categories: ML Theory, Statistics, Coding, System Design, Behavioral
-  Detailed AI-powered feedback on each answer
-  Save and review past interview sessions
-  Track your performance over time
- ️ Customizable number of questions per session

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install openai python-dotenv
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add: `OPENAI_API_KEY=your-api-key-here`


## Commands

- `/start <type> [num]` - Start interview (default 5 questions)
- `/types` - Show available interview types
- `/save` - Save current session
- `/quit` - Exit

## Interview Types

- `ml_theory` - Machine learning concepts
- `statistics` - Statistical methods
- `coding` - Programming challenges
- `system_design` - ML system architecture
- `behavioral` - Soft skills questions

## Example
```
You: /start ml_theory 2

🎯 Starting Ml Theory Interview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Question 1/2:
Explain the bias-variance tradeoff and how it relates to model complexity.

You: [Your answer here]

📊 Feedback:
Score: 8/10
[Detailed feedback from AI]
```
