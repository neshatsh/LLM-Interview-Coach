"""
Data Science Interview Practice Bot
An AI interviewer that helps you practice technical and behavioral interviews
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class InterviewBot:
    def __init__(self, api_key: str = None):
        """Initialize the interview bot"""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"

        # Interview state
        self.current_question = None
        self.question_number = 0
        self.interview_type = None
        self.conversation_history = []
        self.performance_log = []

        # Question banks by category
        self.question_banks = {
            "ml_theory": [
                "Explain the bias-variance tradeoff and how it relates to model complexity.",
                "What's the difference between L1 and L2 regularization? When would you use each?",
                "How does gradient descent work? What are some variations and their advantages?",
                "Explain how a Random Forest works and why it's effective.",
                "What is cross-validation and why is it important?",
                "Describe the difference between supervised and unsupervised learning with examples.",
                "What are precision and recall? How do they differ and when would you optimize for one over the other?",
                "Explain what overfitting is and how you would detect and prevent it.",
                "How does a neural network learn? Explain backpropagation in simple terms.",
                "What's the curse of dimensionality and how does it affect machine learning models?"
            ],
            "statistics": [
                "Explain the Central Limit Theorem and why it's important.",
                "What's the difference between Type I and Type II errors?",
                "How would you test if a coin is fair using statistics?",
                "Explain p-values and confidence intervals. How are they related?",
                "What assumptions does linear regression make?",
                "Explain Bayes' Theorem with a real-world example.",
                "What's the difference between correlation and causation?",
                "How do you handle imbalanced datasets in classification problems?",
                "Explain A/B testing and how you would design an experiment.",
                "What is statistical power and why does it matter?"
            ],
            "coding": [
                "Write a function to find the mode (most frequent element) in a list.",
                "How would you detect if a string is a palindrome?",
                "Write a SQL query to find the top 5 customers by total purchase amount.",
                "Implement a function to calculate the moving average of a time series.",
                "How would you merge two sorted arrays efficiently?",
                "Write code to remove duplicates from a list while preserving order.",
                "Create a function that finds all pairs in an array that sum to a target value.",
                "How would you handle missing values in a pandas DataFrame?",
                "Write a query to find employees who earn more than their managers.",
                "Implement a simple k-means clustering algorithm from scratch."
            ],
            "system_design": [
                "Design a recommendation system for an e-commerce platform.",
                "How would you build a fraud detection system for credit card transactions?",
                "Design a system to predict customer churn for a subscription service.",
                "How would you architect a real-time sentiment analysis system for social media?",
                "Design a search ranking algorithm for a job posting website.",
                "How would you build a model to predict delivery times for a food delivery app?",
                "Design an ML system to detect spam emails at scale.",
                "How would you build a face recognition system that needs to work in real-time?",
                "Design a system for personalized news feed ranking.",
                "How would you build a price prediction model for Airbnb listings?"
            ],
            "behavioral": [
                "Tell me about a time when you had to explain a complex technical concept to a non-technical stakeholder.",
                "Describe a machine learning project that didn't go as planned. What did you learn?",
                "Tell me about a time when you had to make a decision with incomplete data.",
                "How do you stay current with new developments in machine learning and data science?",
                "Describe a situation where you disagreed with a team member about a technical approach.",
                "Tell me about the most challenging data problem you've solved.",
                "How do you prioritize when you have multiple projects with tight deadlines?",
                "Describe a time when you had to debug a complex model that wasn't performing well.",
                "Tell me about a time you had to learn a new technology or tool quickly.",
                "How would you approach a problem where the stakeholder's requirements keep changing?"
            ]
        }

    def start_interview(self, interview_type: str, num_questions: int = 5):
        """Start a new interview session"""
        if num_questions < 1 or num_questions > 10:
            return "Error: Number of questions must be between 1 and 10"
        if interview_type not in self.question_banks:
            valid_types = ", ".join(self.question_banks.keys())
            return f"Invalid interview type. Choose from: {valid_types}"

        try:
            self.interview_type = interview_type
            self.question_number = 0
            self.conversation_history = []
            self.performance_log = []

            # Select random questions
            import random
            questions = random.sample(self.question_banks[interview_type],
                                     min(num_questions, len(self.question_banks[interview_type])))
            self.selected_questions = questions

            intro = f"""
            🎯 Starting {interview_type.replace('_', ' ').title()} Interview
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            
            I'll ask you {len(questions)} questions. Take your time to think through each answer.
            I'll provide feedback after each response. Ready to begin?
            
            """
            return intro + self.ask_next_question()

        except Exception as e:
            return f"Error starting interview: {str(e)}"

    def ask_next_question(self) -> str:
        """Get the next question"""
        if self.question_number >= len(self.selected_questions):
            return self.end_interview()

        self.current_question = self.selected_questions[self.question_number]
        self.question_number += 1

        return f"\n❓ Question {self.question_number}/{len(self.selected_questions)}:\n{self.current_question}\n"

    def evaluate_answer(self, user_answer: str) -> str:
        """Evaluate the user's answer using GPT"""

        evaluation_prompt = f"""You are an experienced data science interviewer. A candidate just answered this question:

Question: {self.current_question}

Candidate's Answer: {user_answer}

Provide constructive feedback with:
1. A score from 1-10
2. What they did well
3. What could be improved
4. Key points they should have mentioned
5. One follow-up question to probe deeper (if appropriate)

Be encouraging but honest. Format your response clearly."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": evaluation_prompt
                }],
                max_tokens=2000,
                temperature=0.7
            )

            feedback = response.choices[0].message.content

            # Log performance
            self.performance_log.append({
                "question": self.current_question,
                "answer": user_answer,
                "feedback": feedback,
                "timestamp": datetime.now().isoformat()
            })

            return f"\n📊 Feedback:\n{feedback}\n"

        except Exception as e:
            return f"Error getting feedback: {str(e)}"

    def process_answer(self, user_answer: str) -> str:
        """Process user's answer and provide feedback"""
        if not self.current_question:
            return "Please start an interview first using start_interview()"

        # Get evaluation
        feedback = self.evaluate_answer(user_answer)

        # Check if interview is complete
        if self.question_number >= len(self.selected_questions):
            return feedback + "\n" + self.end_interview()
        else:
            return feedback + "\n" + self.ask_next_question()

    def end_interview(self) -> str:
        """End the interview and provide summary"""
        summary_prompt = f"""Review this interview performance and provide:
1. Overall assessment (1-10 score)
2. Top 3 strengths
3. Top 3 areas for improvement
4. Specific resources or topics to study
5. Encouraging closing remarks

Interview type: {self.interview_type}
Number of questions: {len(self.selected_questions)}

Performance log:
{json.dumps(self.performance_log, indent=2)}"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": summary_prompt
                }],
                max_tokens=2000,
                temperature=0.7
            )

            summary = response.choices[0].message.content

            result = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 INTERVIEW COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{summary}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            return result

        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def save_session(self, filename: str = None):
        """Save interview session to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"interview_session_{timestamp}.json"

        session_data = {
            "interview_type": self.interview_type,
            "date": datetime.now().isoformat(),
            "questions": self.selected_questions,
            "performance_log": self.performance_log
        }

        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"✓ Session saved to {filename}")

    def get_available_types(self) -> List[str]:
        """Get list of available interview types"""
        return list(self.question_banks.keys())


def main():
    """Command-line interface"""
    print("=" * 60)
    print("🎤 DATA SCIENCE INTERVIEW PRACTICE BOT")
    print("=" * 60)
    print("\nCommands:")
    print("  /start <type> [num]  - Start interview (default 5 questions)")
    print("  /types               - Show available interview types")
    print("  /save                - Save current session")
    print("  /quit                - Exit")
    print("\nInterview Types:")
    print("  - ml_theory: Machine learning concepts")
    print("  - statistics: Statistical methods and theory")
    print("  - coding: Programming and algorithms")
    print("  - system_design: ML system architecture")
    print("  - behavioral: Soft skills and experience")
    print("=" * 60 + "\n")

    bot = InterviewBot()
    in_interview = False

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                parts = user_input.split()
                command = parts[0].lower()

                if command == "/quit":
                    print("Good luck with your interviews! 🚀")
                    break

                elif command == "/types":
                    types = bot.get_available_types()
                    print(f"\nAvailable types: {', '.join(types)}\n")

                elif command == "/start":
                    if len(parts) < 2:
                        print("Usage: /start <type> [num_questions]\n")
                        continue

                    interview_type = parts[1]
                    num_questions = int(parts[2]) if len(parts) > 2 else 5

                    result = bot.start_interview(interview_type, num_questions)
                    print(result)
                    in_interview = True

                elif command == "/save":
                    bot.save_session()
                    print()

                else:
                    print(f"Unknown command: {command}\n")

                continue

            # Process answer during interview
            if in_interview:
                response = bot.process_answer(user_input)
                print(response)

                # Check if interview ended
                if "INTERVIEW COMPLETE" in response:
                    in_interview = False
            else:
                print("Start an interview first with /start <type>\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()