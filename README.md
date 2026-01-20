# LLM Interview Coach 🤖

An intelligent Telegram bot that helps data scientists and ML engineers prepare for technical interviews using GPT-4o.

## Features

- 50+ Curated Questions across 6 categories  
- AI-Powered Feedback with detailed evaluation  
- LeetCode Integration: Direct links to SQL and algorithm problems  
- Difficulty Levels: Easy, Medium, Hard for coding questions  
- Smart Retry System: Option to retry questions with low scores (<7)  
- Complexity Analysis: Time/space complexity feedback for code  
- Progress Tracking: Interview summaries with personalized recommendations  

## Interview Categories

- **ML Theory** - Machine learning concepts and algorithms
- **Statistics** - Statistical methods and hypothesis testing
- **SQL** - Database queries (LeetCode-style problems)
- **Algorithms** - Coding challenges (LeetCode-style problems)
- **System Design** - ML system architecture
- **Behavioral** - Soft skills and situational questions

## Installation

1. **Clone the repository**
2. **Install dependencies**
```bash
pip install openai python-dotenv python-telegram-bot
```

3. **Set up environment variables**

Create a `.env` file in the project root:
```
OPENAI_API_KEY=your-openai-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

To get a Telegram bot token:
- Message [@BotFather](https://t.me/botfather) on Telegram
- Use `/newbot` command and follow instructions
- Copy the token to your `.env` file

4. **Run the bot**
```bash
python interview_bot.py
```

## Bot Commands

- `/start` - Welcome message and introduction
- `/interview` - Start a practice interview
- `/help` - Show available commands and features
- `/cancel` - Cancel current interview

## How to Use

1. Start a chat with your bot on Telegram
2. Type `/interview` to begin
3. Choose a category (ML Theory, SQL, Algorithms, etc.)
4. For SQL/Algorithms: select difficulty (Easy/Medium/Hard)
5. Choose number of questions (3 or 5)
6. Answer each question thoroughly
7. Receive AI-powered feedback with scores
8. Get a comprehensive summary at the end

## Example Session
```
You: /interview

Bot: 📚 Choose an interview category:
[Buttons: ML Theory | Statistics | SQL | Algorithms | System Design | Behavioral]

You: [Click "SQL"]

Bot: 💡 SQL Interview
Choose difficulty level:
[Buttons: Easy | Medium | Hard]

You: [Click "Medium"]

Bot: 🟡 SQL - Medium
How many questions?
[Buttons: 3 Questions | 5 Questions]

You: [Click "3 Questions"]

Bot: 🎯 Starting SQL (Medium) Interview
━━━━━━━━━━━━━━━━━━━━━━━━

Question: Employees Earning More Than Managers
Find employees who earn more than their managers.

Schema: [Table structure shown]
🔗 View on LeetCode

Type your answer below...

You: SELECT e1.name
FROM Employee e1
JOIN Employee e2 ON e1.managerId = e2.id
WHERE e1.salary > e2.salary

Bot: 📊 Feedback:

Score: 9/10

What you did well:
- Correct self-join approach
- Proper WHERE clause for salary comparison
- Clean, readable query

What you could improve:
- Consider NULL handling for managerId
...

[Buttons: Next Question]
```

## Features in Detail

### Smart Evaluation System
- Focuses on **technical understanding**, ignores typos/grammar
- For coding: analyzes **time/space complexity**
- Suggests **optimizations** for suboptimal solutions
- Max score of 7/10 for correct but inefficient code

### Retry Mechanism
- Questions with score < 7 offer retry option
- High scores (≥7) automatically proceed to next question
- Encourages learning from mistakes

### Comprehensive Summaries
- Overall performance score (1-10)
- Top 3 strengths identified
- Top 3 areas for improvement
- Personalized study recommendations
- Interview duration tracking

## Tech Stack

- **Python 3.9+**
- **OpenAI GPT-4o** - AI evaluation and feedback
- **python-telegram-bot** - Telegram Bot API wrapper
- **LeetCode** - SQL and algorithm problem database

