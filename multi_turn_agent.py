from dotenv import load_dotenv
import instructor
from groq import Groq
import os 
from enum import Enum
from pydantic import BaseModel, Field
from typing import Annotated

load_dotenv()

client = instructor.from_groq(
    Groq(api_key=os.getenv('GROQ_API_KEY'))
)

class Confidence(str, Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

class Assistant(BaseModel):
    agent_name: Annotated[str, Field(min_length=5, max_length=50)]
    short_description: Annotated[str, Field(min_length=100, max_length=1500)]
    target_users: Annotated[list[str], Field(min_length=3, max_length=5)]
    core_tools_needed: Annotated[list[str], Field(min_length=4, max_length=6)]
    suggested_tech_stack: Annotated[list[str], Field(min_length=4, max_length=7)]
    first_milestone: Annotated[str, Field(min_length=100, max_length=500)]
    potential_challenges: Annotated[list[str], Field(min_length=3, max_length=5)]
    confidence: Confidence

def ask_structured_question(user_string: str, user_history: list):
    user_history.append({'role': 'user', 'content': user_string})

    system_prompt = '''You are a Senior AI Agent Architect. 

CRITICAL CONSTRAINTS:
1. agent_name: Must be professional and catchy.
2. short_description: Explain the 'how' and 'benefit' clearly. Keep it under 100 words.
3. target_users: Provide a list of 3 to 5 hyper-specific personas.
4. core_tools_needed: Provide a list of 4 to 6 specific functions or integrations.
5. suggested_tech_stack: Provide 4 to 7 realistic, Python-based tools.
6. first_milestone: Provide a concrete task achievable within 14 days. Be descriptive to meet length requirements.
7. potential_challenges: Provide 3 to 5 distinct technical or logical risks.
8. confidence: Use ONLY lowercase: 'high', 'medium', or 'low'.'''

    messages = [{'role': 'system', 'content': system_prompt}] + user_history
    
    data = client.create(
        response_model=Assistant,
        model='llama-3.3-70b-versatile',
        max_retries=3,
        messages=messages
    )

    user_history.append({'role': 'assistant', 'content': data.model_dump_json()})

    print('Agent Name:', data.agent_name)
    print('Short description:', data.short_description)
    
    if data.target_users:
        print('Target users:')
        for point in data.target_users:
            print('.', point)
    
    if data.core_tools_needed:
        print('Core tools needed:')
        for point in data.core_tools_needed:
            print('.', point)

    if data.suggested_tech_stack:
        print('Suggested tech stack:')
        for point in data.suggested_tech_stack:
            print('.', point)

    print('First milestone:', data.first_milestone)

    if data.potential_challenges:
        print('Potential challenges:')
        for point in data.potential_challenges:
            print('.', point)

    print('Confidence:', data.confidence.value)

if __name__ == "__main__":
    user_history = []
    question = None
    while True: 
        question = input('Ask your question (Type "exit" to exit)\n')
        if question == 'exit':
            break
        ask_structured_question(question, user_history)

    