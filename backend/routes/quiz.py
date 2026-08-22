# backend/routes/quiz.py
"""
Quiz API Routes
Educational Phishing Detection Simulator
"""

from flask import Blueprint, request, jsonify, session
from backend.database.db_manager import DatabaseManager
import uuid

quiz_bp = Blueprint('quiz', __name__)
db = DatabaseManager()

# Quiz questions
QUIZ_QUESTIONS = [
    {
        'id': 1,
        'question': 'What is phishing?',
        'options': [
            'A type of fish',
            'A cyber attack that tricks users into revealing sensitive information',
            'A software update',
            'A computer virus'
        ],
        'correct': 1,
        'explanation': 'Phishing is a cyber attack where attackers impersonate legitimate entities to steal sensitive information like passwords and credit card numbers.'
    },
    {
        'id': 2,
        'question': 'Which of the following is a sign of a phishing email?',
        'options': [
            'Personalized greeting with your name',
            'Generic greeting like "Dear Customer"',
            'Official company logo',
            'Professional formatting'
        ],
        'correct': 1,
        'explanation': 'Phishing emails often use generic greetings because they are sent in bulk. Legitimate companies usually address you by name.'
    },
    {
        'id': 3,
        'question': 'What should you do if you receive a suspicious email asking you to verify your account?',
        'options': [
            'Click the link and verify immediately',
            'Reply with your password',
            'Contact the company directly through their official website',
            'Forward it to all your contacts'
        ],
        'correct': 2,
        'explanation': 'Always verify requests by contacting the company directly through their official website or phone number, not through links in the email.'
    },
    {
        'id': 4,
        'question': 'Which URL is most likely to be legitimate for PayPal?',
        'options': [
            'http://paypal-secure.tk',
            'https://www.paypa1.com',
            'https://www.paypal.com',
            'http://paypal-verify.net'
        ],
        'correct': 2,
        'explanation': 'The legitimate PayPal URL is https://www.paypal.com. Watch for misspellings, unusual domains, and missing HTTPS.'
    },
    {
        'id': 5,
        'question': 'What does HTTPS in a URL indicate?',
        'options': [
            'The website is definitely safe',
            'The connection is encrypted',
            'The website has no viruses',
            'The company is legitimate'
        ],
        'correct': 1,
        'explanation': 'HTTPS indicates the connection is encrypted, but it doesn\'t guarantee the website is legitimate. Phishing sites can also use HTTPS.'
    },
    {
        'id': 6,
        'question': 'What is spear phishing?',
        'options': [
            'Fishing with a spear',
            'A targeted phishing attack against specific individuals',
            'A type of malware',
            'A firewall technique'
        ],
        'correct': 1,
        'explanation': 'Spear phishing is a targeted attack where attackers research specific individuals to make their phishing attempts more convincing.'
    },
    {
        'id': 7,
        'question': 'Which of these creates urgency in phishing attempts?',
        'options': [
            '"Your package has been delivered"',
            '"Account will be closed in 24 hours"',
            '"Thank you for your purchase"',
            '"Your subscription has been renewed"'
        ],
        'correct': 1,
        'explanation': 'Phishing emails create urgency to pressure you into acting without thinking. Phrases like "within 24 hours" or "immediate action required" are red flags.'
    },
    {
        'id': 8,
        'question': 'What is smishing?',
        'options': [
            'Phishing via SMS/text messages',
            'Smiling while fishing',
            'A type of antivirus',
            'A programming language'
        ],
        'correct': 0,
        'explanation': 'Smishing is phishing conducted through SMS text messages. Attackers send texts with malicious links or requests for information.'
    },
    {
        'id': 9,
        'question': 'What should you look for in the sender\'s email address?',
        'options': [
            'A professional-looking name',
            'The exact domain of the company',
            'A long email address',
            'Multiple numbers'
        ],
        'correct': 1,
        'explanation': 'Check the sender\'s domain carefully. Legitimate companies use their official domain. Be wary of slight misspellings or unusual domains.'
    },
    {
        'id': 10,
        'question': 'Is it safe to click on links in unexpected emails?',
        'options': [
            'Yes, always',
            'Yes, if it has a company logo',
            'No, verify first through official channels',
            'Yes, if it says "secure"'
        ],
        'correct': 2,
        'explanation': 'Never click links in unexpected emails. Instead, go directly to the company\'s official website by typing the URL yourself.'
    },
    {
        'id': 11,
        'question': 'What is a common trait of phishing websites?',
        'options': [
            'Professional design',
            'Misspelled domain names',
            'Customer reviews',
            'Contact information'
        ],
        'correct': 1,
        'explanation': 'Phishing sites often use domain names that are slight misspellings of legitimate sites (e.g., "paypa1.com" instead of "paypal.com").'
    },
    {
        'id': 12,
        'question': 'What is vishing?',
        'options': [
            'A vitamin supplement',
            'Voice phishing via phone calls',
            'A video game',
            'A type of fish'
        ],
        'correct': 1,
        'explanation': 'Vishing is voice phishing, where attackers use phone calls to trick victims into revealing sensitive information.'
    },
    {
        'id': 13,
        'question': 'Which is the best practice for passwords?',
        'options': [
            'Use the same password everywhere',
            'Write them on a sticky note',
            'Use unique, strong passwords for each account',
            'Share them with trusted friends'
        ],
        'correct': 2,
        'explanation': 'Use unique, strong passwords for each account. Consider using a password manager to keep track of them securely.'
    },
    {
        'id': 14,
        'question': 'What is two-factor authentication (2FA)?',
        'options': [
            'Using two passwords',
            'An extra layer of security requiring a second verification method',
            'Two people sharing an account',
            'A type of encryption'
        ],
        'correct': 1,
        'explanation': '2FA adds an extra security layer by requiring a second form of verification (like a code sent to your phone) in addition to your password.'
    },
    {
        'id': 15,
        'question': 'If you accidentally clicked a phishing link, what should you do?',
        'options': [
            'Nothing, it\'s too late',
            'Turn off your computer',
            'Change your passwords and scan for malware',
            'Delete your email account'
        ],
        'correct': 2,
        'explanation': 'If you clicked a phishing link, immediately change your passwords, run antivirus scans, and monitor your accounts for suspicious activity.'
    },
    {
        'id': 16,
        'question': 'What makes a URL suspicious?',
        'options': [
            'It uses HTTPS',
            'It contains many hyphens and subdomains',
            'It is short',
            'It has .com extension'
        ],
        'correct': 1,
        'explanation': 'Suspicious URLs often have excessive hyphens, many subdomains, misspellings, or unusual characters. Always examine URLs carefully.'
    },
    {
        'id': 17,
        'question': 'Can attachments in emails contain malware?',
        'options': [
            'No, email attachments are always safe',
            'Yes, always scan attachments from unknown sources',
            'Only .exe files are dangerous',
            'Only if the email is from a stranger'
        ],
        'correct': 1,
        'explanation': 'Email attachments can contain malware. Never open attachments from unknown sources, and scan them with antivirus software even if from known contacts.'
    },
    {
        'id': 18,
        'question': 'What should you do if you receive an email about a prize you didn\'t enter?',
        'options': [
            'Claim it immediately',
            'Delete it - it\'s likely a scam',
            'Forward it to friends',
            'Reply asking for more information'
        ],
        'correct': 1,
        'explanation': 'Unexpected prize notifications are almost always scams designed to steal your information or money. Delete them immediately.'
    },
    {
        'id': 19,
        'question': 'Why do phishing emails often have poor grammar?',
        'options': [
            'Attackers are not educated',
            'To bypass spam filters',
            'To target less cautious victims',
            'It\'s intentional to appear authentic'
        ],
        'correct': 2,
        'explanation': 'Poor grammar can be intentional to filter out savvy users, leaving only those more likely to fall for the scam. It can also be due to automated translation.'
    },
    {
        'id': 20,
        'question': 'What is the best way to report phishing?',
        'options': [
            'Ignore it',
            'Reply to tell them it\'s a scam',
            'Forward to your IT department or use email provider\'s report feature',
            'Post it on social media'
        ],
        'correct': 2,
        'explanation': 'Report phishing to your IT department, email provider, or use dedicated reporting tools. This helps protect others and track attackers.'
    }
]

def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        db.create_user(session['session_id'])
    return session['session_id']

@quiz_bp.route('/quiz/questions', methods=['GET'])
def get_quiz_questions():
    """Get quiz questions"""
    try:
        # Return questions without correct answers
        questions = [
            {
                'id': q['id'],
                'question': q['question'],
                'options': q['options']
            }
            for q in QUIZ_QUESTIONS
        ]
        
        return jsonify({
            'success': True,
            'questions': questions,
            'total': len(questions)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz answers"""
    try:
        data = request.get_json()
        
        if not data or 'answers' not in data:
            return jsonify({'error': 'Answers are required'}), 400
        
        answers = data['answers']
        session_id = get_session_id()
        
        # Calculate score
        score = 0
        total = len(QUIZ_QUESTIONS)
        results = []
        
        for question in QUIZ_QUESTIONS:
            user_answer = answers.get(str(question['id']))
            is_correct = user_answer == question['correct']
            
            if is_correct:
                score += 1
            
            results.append({
                'id': question['id'],
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
        
        percentage = (score / total) * 100
        
        # Save to database
        db.save_quiz_result(
            session_id=session_id,
            score=score,
            total_questions=total,
            answers_data={'answers': answers}
        )
        
        # Get performance level
        if percentage >= 90:
            level = 'Expert'
            message = 'Excellent! You have strong phishing awareness.'
        elif percentage >= 70:
            level = 'Advanced'
            message = 'Good job! You understand most phishing concepts.'
        elif percentage >= 50:
            level = 'Intermediate'
            message = 'Fair. Review the explanations to improve your awareness.'
        else:
            level = 'Beginner'
            message = 'You need more training. Study the explanations carefully.'
        
        return jsonify({
            'success': True,
            'score': score,
            'total': total,
            'percentage': round(percentage, 2),
            'level': level,
            'message': message,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/quiz/results', methods=['GET'])
def get_quiz_results():
    """Get quiz result history"""
    try:
        session_id = get_session_id()
        results = db.get_quiz_results(session_id=session_id, limit=10)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500