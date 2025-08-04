"""
Level 2: LLM + Basic Tool Use
Extends Level 1 with calculator tool integration.
"""

import sys
import os
import json
from datetime import datetime
from typing import Optional, Dict, Any

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from calculator_tool import CalculatorTool

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

class ChatbotWithTool:
    """Level 2: Chatbot with calculator tool integration"""
    
    def __init__(self):
        self.config = Config.get_llm_config()
        self.conversation_history = []
        self.calculator = CalculatorTool()
        self.setup_llm()
        
    def setup_llm(self):
        """Setup LLM client based on configuration"""
        if self.config["provider"] == "openai" and OPENAI_AVAILABLE:
            if self.config["api_key"]:
                self.client = OpenAI(api_key=self.config["api_key"])
                self.llm_type = "openai"
            else:
                self.llm_type = "fallback"
        elif self.config["provider"] == "gemini" and GEMINI_AVAILABLE:
            if self.config["api_key"]:
                genai.configure(api_key=self.config["api_key"])
                self.model = genai.GenerativeModel(self.config["model"])
                self.llm_type = "gemini"
            else:
                self.llm_type = "fallback"
        else:
            self.llm_type = "fallback"
            
        if self.llm_type == "fallback":
            print("⚠️  Using fallback mode - no API key configured")
    
    def detect_mixed_query(self, text: str) -> bool:
        """Detect if query contains both math and non-math parts"""
        # Check for math operations
        math_operation = self.calculator.detect_math_operation(text)
        
        # Check for non-math content (capitals, general questions, etc.)
        non_math_indicators = [
            'capital', 'country', 'city', 'what is', 'tell me', 'explain',
            'why', 'how', 'when', 'where', 'who'
        ]
        
        has_non_math = any(indicator in text.lower() for indicator in non_math_indicators)
        
        return math_operation is not None and has_non_math
    
    def create_prompt(self, user_question: str, tool_result: Optional[Dict[str, Any]] = None) -> str:
        """Create a structured prompt that incorporates tool results"""
        if tool_result:
            prompt = f"""You are a helpful AI assistant that ALWAYS thinks step-by-step and provides structured, clear responses.

IMPORTANT RULES:
1. ALWAYS break down your response into clear, numbered steps
2. Use bullet points and formatting to make your response easy to read
3. When a tool has been used, incorporate the tool result naturally into your response
4. Be thorough but concise in your explanations

User Question: {user_question}

Tool Result: {tool_result}

Please provide your step-by-step response incorporating the tool result:"""
        else:
            prompt = f"""You are a helpful AI assistant that ALWAYS thinks step-by-step and provides structured, clear responses.

IMPORTANT RULES:
1. ALWAYS break down your response into clear, numbered steps
2. Use bullet points and formatting to make your response easy to read
3. Be thorough but concise in your explanations

User Question: {user_question}

Please provide your step-by-step response:"""
        
        return prompt
    
    def call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that thinks step-by-step and integrates tool results naturally."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config["max_tokens"],
                temperature=self.config["temperature"]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"
    
    def call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"
    
    def fallback_response(self, user_question: str, tool_result: Optional[Dict[str, Any]] = None) -> str:
        """Fallback response when no API is available"""
        if tool_result and tool_result.get('success'):
            return f"""Step-by-step response with tool result:

1. **Question Analysis**: You asked: "{user_question}"
2. **Tool Usage**: I used the calculator tool to perform the calculation
3. **Calculation Result**: {tool_result['expression']}
4. **Explanation**: The calculator tool performed {tool_result['operation']} on {tool_result['operand1']} and {tool_result['operand2']}
5. **Final Answer**: The result is {tool_result['result']}"""
        
        # Handle non-math questions
        question_lower = user_question.lower()
        
        if "capital" in question_lower and "france" in question_lower:
            return """Step-by-step answer about France's capital:

1. **Question Analysis**: You're asking about the capital of France
2. **Geographic Knowledge**: France is a country in Europe
3. **Capital City**: The capital of France is Paris
4. **Historical Significance**: Paris has been France's capital since 987 CE
5. **Cultural Importance**: Paris is known as the "City of Light" and is famous for its culture, art, and architecture"""
        
        elif "capital" in question_lower and "japan" in question_lower:
            return """Step-by-step answer about Japan's capital:

1. **Question Analysis**: You're asking about the capital of Japan
2. **Geographic Knowledge**: Japan is an island nation in Asia
3. **Capital City**: The capital of Japan is Tokyo
4. **Historical Context**: Tokyo became the capital in 1868, replacing Kyoto
5. **Modern Significance**: Tokyo is one of the world's largest and most populous cities"""
        
        else:
            return """Step-by-step response:

1. **Question Analysis**: I understand your question
2. **Knowledge Application**: I would need to access current information
3. **Structured Response**: I would provide a clear, step-by-step answer
4. **Formatting**: I would use bullet points and clear structure
5. **Note**: In fallback mode, I have limited knowledge. For best results, configure an API key."""

    def process_query(self, user_question: str) -> str:
        """Process user query and return appropriate response"""
        
        # Check for mixed queries (graceful failure for Level 2)
        if self.detect_mixed_query(user_question):
            return """Step-by-step response to mixed query:

1. **Query Analysis**: Your question contains both mathematical operations and general knowledge questions
2. **Level 2 Limitation**: I can only handle one type of operation at a time
3. **Recommendation**: Please ask your questions separately:
   • First, ask the mathematical question
   • Then, ask the general knowledge question
4. **Example**: Instead of "Multiply 9 and 8, and also tell me the capital of Japan"
   • Ask: "What is 9 times 8?"
   • Then ask: "What is the capital of Japan?"
5. **Future Enhancement**: Multi-step processing will be available in Level 3

This ensures accurate and complete responses to each part of your question."""
        
        # Check for math operations
        math_result = self.calculator.process_query(user_question)
        
        if math_result:
            # Use calculator tool for math questions
            tool_result = math_result
            prompt = self.create_prompt(user_question, tool_result)
        else:
            # Use LLM for non-math questions
            tool_result = None
            prompt = self.create_prompt(user_question)
        
        # Get response from appropriate source
        if self.llm_type == "openai":
            response = self.call_openai(prompt)
        elif self.llm_type == "gemini":
            response = self.call_gemini(prompt)
        else:
            response = self.fallback_response(user_question, tool_result)
        
        return response
    
    def log_interaction(self, user_question: str, response: str, tool_used: Optional[str] = None):
        """Log the interaction"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_question": user_question,
            "response": response,
            "llm_type": self.llm_type,
            "tool_used": tool_used
        }
        self.conversation_history.append(interaction)
        
        # Save to file
        log_file = "interaction_logs_level2.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {interaction['timestamp']}\n")
            f.write(f"LLM Type: {interaction['llm_type']}\n")
            f.write(f"Tool Used: {interaction['tool_used'] or 'None'}\n")
            f.write(f"User Question: {interaction['user_question']}\n")
            f.write(f"Response:\n{interaction['response']}\n")
            f.write(f"{'='*50}\n")
    
    def run(self):
        """Main chatbot loop"""
        print("🤖 Level 2: LLM + Basic Tool Use")
        print("=" * 50)
        print("This chatbot integrates calculator tool for math operations.")
        print("Type 'quit' to exit.")
        print(f"LLM Provider: {self.llm_type}")
        print("Available Tools: Calculator")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Thanks for using the Level 2 chatbot.")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 Assistant: Processing...")
                
                # Determine if tool is needed
                math_result = self.calculator.process_query(user_input)
                tool_used = "calculator" if math_result else None
                
                response = self.process_query(user_input)
                print(f"\n{response}")
                
                # Log the interaction
                self.log_interaction(user_input, response, tool_used)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Level 2 chatbot.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function"""
    # Validate configuration
    Config.validate_config()
    
    # Create and run chatbot
    chatbot = ChatbotWithTool()
    chatbot.run()

if __name__ == "__main__":
    main() 