"""
Telegram Interview Coach Bot
AI-powered interview practice bot for data science and ML roles
"""

import os
import json
import random
import re
import html
from datetime import datetime
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

load_dotenv()

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

THEORY_QUESTIONS = {
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

# LeetCode-style SQL questions
SQL_QUESTIONS = {
    "easy": [
        {
            "title": "Big Countries",
            "description": "Find the name, population, and area of countries with area >= 3,000,000 or population >= 25,000,000.",
            "schema": """Table: World
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| name        | varchar |
| continent   | varchar |
| area        | int     |
| population  | int     |
| gdp         | bigint  |
+-------------+---------+
name is the primary key.""",
            "leetcode": "https://leetcode.com/problems/big-countries/"
        },
        {
            "title": "Recyclable and Low Fat Products",
            "description": "Find the ids of products that are both low fat and recyclable.",
            "schema": """Table: Products
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| low_fats    | enum    |
| recyclable  | enum    |
+-------------+---------+
product_id is the primary key.
low_fats is ENUM of ('Y', 'N').
recyclable is ENUM of ('Y', 'N').""",
            "leetcode": "https://leetcode.com/problems/recyclable-and-low-fat-products/"
        },
        {
            "title": "Find Customer Referee",
            "description": "Find the names of customers who were NOT referred by the customer with id = 2.",
            "schema": """Table: Customer
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| referee_id  | int     |
+-------------+---------+
id is the primary key.
referee_id can be NULL.""",
            "leetcode": "https://leetcode.com/problems/find-customer-referee/"
        },
        {
            "title": "Article Views I",
            "description": "Find all authors who viewed at least one of their own articles. Return in ascending order.",
            "schema": """Table: Views
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| article_id    | int     |
| author_id     | int     |
| viewer_id     | int     |
| view_date     | date    |
+---------------+---------+
There is no primary key (may have duplicates).
Each row indicates that viewer_id viewed article_id on view_date.""",
            "leetcode": "https://leetcode.com/problems/article-views-i/"
        },
        {
            "title": "Invalid Tweets",
            "description": "Find the IDs of invalid tweets (content length > 15 characters).",
            "schema": """Table: Tweets
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| tweet_id       | int     |
| content        | varchar |
+----------------+---------+
tweet_id is the primary key.""",
            "leetcode": "https://leetcode.com/problems/invalid-tweets/"
        }
    ],
    "medium": [
        {
            "title": "Employees Earning More Than Managers",
            "description": "Find employees who earn more than their managers.",
            "schema": """Table: Employee
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| managerId   | int     |
+-------------+---------+
id is the primary key.
managerId is a foreign key to id (can be NULL).""",
            "leetcode": "https://leetcode.com/problems/employees-earning-more-than-their-managers/"
        },
        {
            "title": "Department Highest Salary",
            "description": "Find employees who have the highest salary in each department.",
            "schema": """Table: Employee
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| departmentId| int     |
+-------------+---------+

Table: Department
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+""",
            "leetcode": "https://leetcode.com/problems/department-highest-salary/"
        },
        {
            "title": "Consecutive Numbers",
            "description": "Find all numbers that appear at least three times consecutively.",
            "schema": """Table: Logs
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
id is an autoincrement column.""",
            "leetcode": "https://leetcode.com/problems/consecutive-numbers/"
        },
        {
            "title": "Product Sales Analysis III",
            "description": "Select the first year that a product was sold and the quantity and price.",
            "schema": """Table: Sales
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+

Table: Product
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| product_name| varchar |
+-------------+---------+""",
            "leetcode": "https://leetcode.com/problems/product-sales-analysis-iii/"
        },
        {
            "title": "Monthly Transactions I",
            "description": "Find monthly stats: total transactions, approved transactions, total amount, and approved amount.",
            "schema": """Table: Transactions
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
state is ENUM of ('approved', 'declined').""",
            "leetcode": "https://leetcode.com/problems/monthly-transactions-i/"
        }
    ],
    "hard": [
        {
            "title": "Department Top Three Salaries",
            "description": "Find employees who earn in the top three unique salaries in each department.",
            "schema": """Table: Employee
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| departmentId| int     |
+-------------+---------+

Table: Department
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+""",
            "leetcode": "https://leetcode.com/problems/department-top-three-salaries/"
        },
        {
            "title": "Human Traffic of Stadium",
            "description": "Find records with 3+ consecutive rows where people >= 100.",
            "schema": """Table: Stadium
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| visit_date    | date    |
| people        | int     |
+---------------+---------+
id is autoincrement and visit_date has unique values.""",
            "leetcode": "https://leetcode.com/problems/human-traffic-of-stadium/"
        }
    ]
}

# LeetCode-style Algorithm questions
ALGORITHM_QUESTIONS = {
    "easy": [
        {
            "title": "Two Sum",
            "description": "Given an array of integers nums and an integer target, return indices of two numbers that add up to target.",
            "example": "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]",
            "leetcode": "https://leetcode.com/problems/two-sum/"
        },
        {
            "title": "Valid Parentheses",
            "description": "Given a string containing just '(', ')', '{', '}', '[' and ']', determine if the input string is valid. Opening brackets must be closed by the same type in correct order.",
            "example": "Input: s = '()[]{}'\nOutput: true",
            "leetcode": "https://leetcode.com/problems/valid-parentheses/"
        },
        {
            "title": "Palindrome Number",
            "description": "Given an integer x, return true if x is a palindrome (reads the same backward as forward).",
            "example": "Input: x = 121\nOutput: true",
            "leetcode": "https://leetcode.com/problems/palindrome-number/"
        },
        {
            "title": "Best Time to Buy and Sell Stock",
            "description": "Find the maximum profit from buying and selling one share of stock. You must buy before you sell.",
            "example": "Input: prices = [7,1,5,3,6,4]\nOutput: 5 (buy at 1, sell at 6)",
            "leetcode": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"
        },
        {
            "title": "Valid Anagram",
            "description": "Given two strings s and t, return true if t is an anagram of s.",
            "example": "Input: s = 'anagram', t = 'nagaram'\nOutput: true",
            "leetcode": "https://leetcode.com/problems/valid-anagram/"
        }
    ],
    "medium": [
        {
            "title": "Longest Substring Without Repeating Characters",
            "description": "Given a string s, find the length of the longest substring without repeating characters.",
            "example": "Input: s = 'abcabcbb'\nOutput: 3 (substring 'abc')",
            "leetcode": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"
        },
        {
            "title": "3Sum",
            "description": "Given an integer array nums, return all triplets [nums[i], nums[j], nums[k]] where i != j != k and nums[i] + nums[j] + nums[k] == 0.",
            "example": "Input: nums = [-1,0,1,2,-1,-4]\nOutput: [[-1,-1,2],[-1,0,1]]",
            "leetcode": "https://leetcode.com/problems/3sum/"
        },
        {
            "title": "Group Anagrams",
            "description": "Given an array of strings, group the anagrams together.",
            "example": "Input: strs = ['eat','tea','tan','ate','nat','bat']\nOutput: [['bat'],['nat','tan'],['ate','eat','tea']]",
            "leetcode": "https://leetcode.com/problems/group-anagrams/"
        },
        {
            "title": "Product of Array Except Self",
            "description": "Given an integer array nums, return an array where answer[i] equals the product of all elements except nums[i]. Do it in O(n) without division.",
            "example": "Input: nums = [1,2,3,4]\nOutput: [24,12,8,6]",
            "leetcode": "https://leetcode.com/problems/product-of-array-except-self/"
        },
        {
            "title": "Container With Most Water",
            "description": "Find two lines that together with x-axis form a container that holds the most water.",
            "example": "Input: height = [1,8,6,2,5,4,8,3,7]\nOutput: 49",
            "leetcode": "https://leetcode.com/problems/container-with-most-water/"
        }
    ],
    "hard": [
        {
            "title": "Median of Two Sorted Arrays",
            "description": "Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays. Runtime must be O(log(m+n)).",
            "example": "Input: nums1 = [1,3], nums2 = [2]\nOutput: 2.0",
            "leetcode": "https://leetcode.com/problems/median-of-two-sorted-arrays/"
        },
        {
            "title": "Trapping Rain Water",
            "description": "Given n non-negative integers representing elevation map where width of each bar is 1, compute how much water can be trapped after raining.",
            "example": "Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]\nOutput: 6",
            "leetcode": "https://leetcode.com/problems/trapping-rain-water/"
        }
    ]
}

user_sessions: Dict[int, dict] = {}


def extract_score(feedback: str) -> int:
    """Extract numerical score from feedback text"""
    match = re.search(r'[Ss]core[:\s]+(\d+)', feedback)
    if match:
        return int(match.group(1))
    match = re.search(r'(\d+)/10', feedback)
    if match:
        return int(match.group(1))
    return None


def format_question(question, category):
    """Format question based on type"""
    if category in ["sql", "algorithms"]:
        q_text = f"<b>Question: {question['title']}</b>\n\n"
        q_text += f"{question['description']}\n\n"

        if 'schema' in question:
            q_text += f"<pre>{question['schema']}</pre>\n\n"

        if 'example' in question:
            q_text += f"<b>Example:</b>\n<pre>{question['example']}</pre>\n\n"

        q_text += f'🔗 <a href="{question["leetcode"]}">View on LeetCode</a>'
        return q_text
    else:
        return f"<b>Question:</b>\n\n{question}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = update.effective_user.id

    welcome_message = """
                        🎯 <b>Welcome to DS Interview Coach!</b>
                        
I'm your AI-powered interview practice assistant. I'll help you prepare for data science and ML interviews with:

✅ 50+ curated questions across 5 categories
✅ Detailed AI feedback on your answers
✅ Progress tracking
✅ Personalized improvement suggestions

<b>Commands:</b>
/interview - Start a practice interview
/help - Show this message
/stats - View your statistics

Ready to practice? Use /interview to begin!
"""

    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
<b>Available Commands:</b>

/start - Welcome message
/interview - Start a practice interview
/stats - View your interview statistics
/cancel - Cancel current interview
/help - Show this help message

<b>How to use:</b>
1. Type /interview
2. Choose an interview category
3. Answer the questions
4. Get AI-powered feedback
5. Review your performance summary

<b>Categories:</b>
• ML Theory - Machine learning concepts
• Statistics - Statistical methods
• SQL - Database queries
• Algorithms - Coding problems
• System Design - ML system architecture
• Behavioral - Soft skills

<b>Features:</b>
• Choose difficulty: Easy, Medium, Hard
• Get retry option for low scores (< 7)
• Complexity analysis for code
• Direct links to LeetCode for reference

Good luck! 🚀
"""
    await update.message.reply_text(help_text, parse_mode='HTML')


async def interview_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /interview command - show category selection"""
    keyboard = [
        [
            InlineKeyboardButton("🤖 ML Theory", callback_data="cat_ml_theory"),
            InlineKeyboardButton("📊 Statistics", callback_data="cat_statistics")
        ],
        [
            InlineKeyboardButton("💾 SQL", callback_data="cat_sql"),
            InlineKeyboardButton("💻 Algorithms", callback_data="cat_algorithms")
        ],
        [
            InlineKeyboardButton("🏗️ System Design", callback_data="cat_system_design"),
            InlineKeyboardButton("💬 Behavioral", callback_data="cat_behavioral")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📚 <b>Choose an interview category:</b>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection"""
    query = update.callback_query
    await query.answer()

    category = query.data.replace("cat_", "")
    category_name = category.replace('_', ' ').title()

    if category in ["sql", "algorithms"]:
        keyboard = [
            [
                InlineKeyboardButton("🟢 Easy", callback_data=f"diff_{category}_easy"),
                InlineKeyboardButton("🟡 Medium", callback_data=f"diff_{category}_medium")
            ],
            [
                InlineKeyboardButton("🔴 Hard", callback_data=f"diff_{category}_hard")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"💡 <b>{category_name} Interview</b>\n\nChoose difficulty level:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    else:
        keyboard = [
            [
                InlineKeyboardButton("3 Questions", callback_data=f"num_{category}_3"),
                InlineKeyboardButton("5 Questions", callback_data=f"num_{category}_5")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"📝 <b>{category_name} Interview</b>\n\nHow many questions?",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )


async def difficulty_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle difficulty selection"""
    query = update.callback_query
    await query.answer()

    parts = query.data.split("_")
    category = parts[1]
    difficulty = parts[2]

    keyboard = [
        [
            InlineKeyboardButton("3 Questions", callback_data=f"start_{category}_{difficulty}_3"),
            InlineKeyboardButton("5 Questions", callback_data=f"start_{category}_{difficulty}_5")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    category_name = category.upper() if category == "sql" else category.title()

    await query.edit_message_text(
        f"{difficulty_emoji[difficulty]} <b>{category_name} - {difficulty.title()}</b>\n\nHow many questions?",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def start_interview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the interview"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if query.data.startswith("start_"):
        parts = query.data.split("_")
        category = parts[1]
        difficulty = parts[2]
        num_questions = int(parts[3])

        if category == "sql":
            questions = random.sample(
                SQL_QUESTIONS[difficulty],
                min(num_questions, len(SQL_QUESTIONS[difficulty]))
            )
        else:
            questions = random.sample(
                ALGORITHM_QUESTIONS[difficulty],
                min(num_questions, len(ALGORITHM_QUESTIONS[difficulty]))
            )

        difficulty_level = difficulty
    else:
        parts = query.data.split("_")
        category = "_".join(parts[1:-1])
        num_questions = int(parts[-1])
        difficulty_level = None

        questions = random.sample(
            THEORY_QUESTIONS[category],
            min(num_questions, len(THEORY_QUESTIONS[category]))
        )

    user_sessions[user_id] = {
        "category": category,
        "difficulty": difficulty_level,
        "questions": questions,
        "current_question_index": 0,
        "answers": [],
        "feedback": [],
        "start_time": datetime.now().isoformat()
    }

    first_question = format_question(questions[0], category)
    category_display = category.upper() if category == "sql" else category.replace('_', ' ').title()
    diff_text = f" ({difficulty_level.title()})" if difficulty_level else ""

    intro_message = f"""
🎯 <b>Starting {category_display}{diff_text} Interview</b>
━━━━━━━━━━━━━━━━━━━━━━━━

You'll be asked {len(questions)} questions.
Take your time and answer thoroughly.

{first_question}

<i>Type your answer below...</i>
"""

    await query.edit_message_text(intro_message, parse_mode='HTML', disable_web_page_preview=True)


async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user's answer"""
    user_id = update.effective_user.id

    if user_id not in user_sessions:
        await update.message.reply_text("No active interview. Start one with /interview")
        return

    session = user_sessions[user_id]
    user_answer = update.message.text
    current_q_index = session["current_question_index"]
    current_question = session["questions"][current_q_index]
    category = session["category"]

    await update.message.chat.send_action("typing")

    if category in ["sql", "algorithms"]:
        question_text = f"{current_question['title']}: {current_question['description']}"
        if 'schema' in current_question:
            question_text += f"\n\nSchema:\n{current_question['schema']}"
    else:
        question_text = current_question

    is_coding = category in ["sql", "algorithms"]

    if is_coding:
        evaluation_prompt = f"""You are a friendly and experienced data science interviewer giving feedback directly to the candidate on their CODING answer.

Question: {question_text}

Their Answer: {user_answer}

Provide personalized, conversational feedback speaking directly to them using "you":
1. A score from 1-10
2. What you did well (2-3 points)
3. What you could improve (2-3 points)
4. Key concepts you should have mentioned

CRITICAL REQUIREMENTS FOR OPTIMIZATION:
- ALWAYS analyze the time complexity (Big O) of their solution
- ALWAYS analyze the space complexity
- If their solution works but is NOT optimal, clearly state:
  * Current complexity: O(?)
  * Optimal complexity: O(?)
  * How to achieve optimal: [specific suggestion]
- Even if correct, if suboptimal, max score is 7/10
- Provide concrete optimization suggestions

PRIORITY ORDER:
1. Correctness
2. Time complexity optimization
3. Space complexity optimization  
4. Edge cases
5. Code style (mention only at end if at all)

Be encouraging but honest. Speak directly using "you". Keep concise (under 250 words)."""
    else:
        evaluation_prompt = f"""You are a friendly and experienced data science interviewer giving feedback directly to the candidate.

Question: {question_text}

Their Answer: {user_answer}

Provide personalized, conversational feedback:
1. A score from 1-10
2. What you did well (2-3 points)
3. What you could improve (2-3 points)
4. Key concepts you should have mentioned

IMPORTANT: 
- Focus ONLY on technical content
- IGNORE typos, grammar, spelling completely
- Evaluate conceptual understanding, not writing quality

Speak directly using "you" and "your". Keep concise (under 200 words)."""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": evaluation_prompt}],
            max_tokens=500,
            temperature=0.7
        )

        feedback = response.choices[0].message.content

        session["answers"].append(user_answer)
        session["feedback"].append(feedback)

        score = extract_score(feedback)

        safe_feedback = html.escape(feedback)
        feedback_message = f"📊 <b>Feedback:</b>\n\n{safe_feedback}"

        if score and score < 7:
            keyboard = [
                [
                    InlineKeyboardButton("🔄 Retry This Question", callback_data=f"retry_{user_id}"),
                    InlineKeyboardButton("➡️ Next Question", callback_data=f"next_{user_id}")
                ]
            ]
            await update.message.reply_text(
                feedback_message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        else:
            # Success! Score is high, so we increment and move on automatically
            await update.message.reply_text(feedback_message, parse_mode='HTML', disable_web_page_preview=True)
            session["current_question_index"] += 1

            # Check if we should ask another or finish
            if session["current_question_index"] < len(session["questions"]):
                await ask_next_question(update, context, user_id)
            else:
                await generate_summary(update, context, user_id)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


async def ask_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Ask the next question"""
    session = user_sessions[user_id]
    next_q_index = session["current_question_index"]
    next_question = session["questions"][next_q_index]
    category = session["category"]

    formatted_question = format_question(next_question, category)

    next_message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Question {next_q_index + 1}/{len(session["questions"])}:</b>

{formatted_question}

<i>Type your answer below...</i>
"""
    await update.message.reply_text(
        next_message,
        parse_mode='HTML',
        disable_web_page_preview=True
    )


async def handle_retry_or_next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle retry or next question button clicks"""
    query = update.callback_query
    await query.answer()

    action, user_id_str = query.data.split("_")
    user_id = int(user_id_str)

    if user_id not in user_sessions:
        await query.edit_message_text("Session expired. Start a new interview with /interview")
        return

    session = user_sessions[user_id]

    if action == "retry":
        current_question = session["questions"][session["current_question_index"]]
        formatted_q = format_question(current_question, session["category"])

        await query.edit_message_text(
            f"🔄 <b>Retry Attempt</b>\n\n{formatted_q}",
            parse_mode='HTML',
            disable_web_page_preview=True
        )

    elif action == "next":

        session["current_question_index"] += 1

        if session["current_question_index"] < len(session["questions"]):

            next_q_index = session["current_question_index"]
            next_question = session["questions"][next_q_index]
            category = session["category"]
            formatted_question = format_question(next_question, category)
            next_message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━
<b>Question {next_q_index + 1}/{len(session["questions"])}:</b>


    {formatted_question}


<i>Type your answer below...</i>
    """
            await query.edit_message_text(next_message, parse_mode='HTML',
                                          disable_web_page_preview=True)

        else:
            await generate_summary(query, context, user_id)


async def generate_summary(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    """Generate and send interview summary"""
    session = user_sessions.get(user_id)
    if not session:
        return

    start_time = datetime.fromisoformat(session["start_time"])
    duration = datetime.now() - start_time
    minutes = int(duration.total_seconds() // 60)
    seconds = int(duration.total_seconds() % 60)
    time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

    msg = update.message if update.message else update.callback_query.message
    await msg.chat.send_action("typing")

    summary_prompt = f"""You are a supportive data science interview coach. Review this interview performance and speak directly to the candidate using "you" and "your".

Provide:
1. Overall assessment (1-10 score) 
2. Your top 3 strengths
3. Your top 3 areas for improvement
4. 2-3 specific study recommendations for you

Interview category: {session["category"]}
Number of questions: {len(session["questions"])}

Performance:
{json.dumps(list(zip(session["questions"], session["feedback"])), indent=2)}
Total Interview Duration: {time_str}

Be encouraging, personal, and conversational. Speak directly to them. Keep it concise and actionable."""

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": summary_prompt}],
            max_tokens=800,
            temperature=0.7
        )

        summary = response.choices[0].message.content
        safe_summary = html.escape(summary)

        category_name = session["category"].replace('_', ' ').title()

        final_message = f"""
━━━━━━━━━━━━━━━━━━━━━━━━
🎓 <b>INTERVIEW COMPLETE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Category:</b> {category_name}
<b>Questions:</b> {len(session["questions"])}
<b>Duration:</b> {time_str}

{safe_summary}

━━━━━━━━━━━━━━━━━━━━━━━━

Great job! 🎉

Start another interview with /interview
"""
        await msg.reply_text(final_message, parse_mode='HTML')

        if user_id in user_sessions:
            del user_sessions[user_id]

    except Exception as e:
        await msg.reply_text(f"Error generating summary: {str(e)}")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics (placeholder)"""
    stats_message = """
📊 <b>Your Statistics</b>

<i>Feature coming soon!</i>

Track your progress across:
• Total interviews completed
• Average scores by category
• Improvement over time
• Areas needing focus

Keep practicing! 🚀
"""
    await update.message.reply_text(stats_message, parse_mode='HTML')


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current interview"""
    user_id = update.effective_user.id

    if user_id in user_sessions:
        del user_sessions[user_id]
        await update.message.reply_text("❌ Interview cancelled. Start a new one with /interview")
    else:
        await update.message.reply_text("No active interview to cancel.")


def main():
    """Run the bot"""
    # Get token from environment
    token = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in .env file!")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("interview", interview_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("cancel", cancel_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    application.add_handler(CallbackQueryHandler(category_selected, pattern="^cat_"))
    application.add_handler(CallbackQueryHandler(difficulty_selected, pattern="^diff_"))
    application.add_handler(CallbackQueryHandler(start_interview, pattern="^(num_|start_)"))
    application.add_handler(CallbackQueryHandler(handle_retry_or_next, pattern="^(retry|next)_"))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
