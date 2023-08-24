text = '''1. Can you tell us about your experience in the banking industry?
4. Can you provide details about any projects you have worked on in the banking sector?
5. What skills do you possess that are relevant to the banking industry?
6. Are you familiar with any specific technologies or programming languages used in banking? If so, which ones?
7. What languages are you proficient in, and how would you rate your proficiency level?
8. Have you undergone any training or workshops related to banking or finance?
9. Can you share any achievements or accomplishments related to your work in banking or finance?
10. What interests you about working in the banking industry?
11. How do you stay updated with the latest trends and developments in the banking sector?
12. Can you provide an example of a time when you demonstrated problem-solving skills in a banking context?
13. How do you handle working in a team environment? Can you provide an example of a successful team project you have been a part of?
14. How do you adapt to new technologies and tools in the banking industry?
15. Can you describe a situation where you had to meet project deadlines in a cooperative team environment?'''

# Splitting the text into separate questions
questions_list = text.split('\n')

# Cleaning up the list to remove empty items and extracting the questions
questions_list = [question.split('. ', 1)[1] for question in questions_list if question.strip()]

# Printing each question on a separate line
for question in questions_list:
    print(question)
