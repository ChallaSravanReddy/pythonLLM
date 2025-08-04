"""
Level 1: LLM-Only Smart Assistant
A simple CLI program that takes user questions and sends them to an LLM
with prompt engineering to force step-by-step thinking.
"""

import sys
import os
import google.generativeai as genai
import json
from datetime import datetime
from typing import Optional

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

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

class LLMOnlyChatbot:
    """Level 1: LLM-only chatbot with step-by-step reasoning"""
    
    def __init__(self):
        self.config = Config.get_llm_config()
        self.conversation_history = []
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
    
    def create_prompt(self, user_question: str) -> str:
        """Create a structured prompt that forces step-by-step thinking"""
        prompt = f"""You are a helpful AI assistant that ALWAYS thinks step-by-step and provides structured, clear responses.

IMPORTANT RULES:
1. ALWAYS break down your response into clear, numbered steps
2. Use bullet points and formatting to make your response easy to read
3. If the question involves mathematical calculations, DO NOT solve them directly
4. For math questions, explain that you need a calculator tool and suggest using one
5. Be thorough but concise in your explanations

User Question: {user_question}

Please provide your step-by-step response:"""
        return prompt
    
    def call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.config["model"],
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that thinks step-by-step."},
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
    
    def fallback_response(self, user_question: str) -> str:
        """Fallback response when no API is available"""
        # Simple rule-based responses for demonstration
        question_lower = user_question.lower()
        
        if "rainbow" in question_lower and "color" in question_lower:
            return """Step-by-step explanation of rainbow colors:

1. **Understanding Light**: White light from the sun contains all colors
2. **Dispersion Process**: When light passes through water droplets, it gets separated
3. **Color Spectrum**: The colors separate based on their wavelengths
4. **ROYGBIV Order**: The colors appear in this specific order:
   • Red (longest wavelength)
   • Orange
   • Yellow
   • Green
   • Blue
   • Indigo
   • Violet (shortest wavelength)
5. **Formation**: This creates the beautiful arc of colors we see in the sky"""
        
        elif "sky" in question_lower and "blue" in question_lower:
            return """Step-by-step explanation of why the sky is blue:

1. **Sunlight Composition**: Sunlight contains all colors of the rainbow
2. **Atmospheric Scattering**: When sunlight hits Earth's atmosphere, it gets scattered
3. **Rayleigh Scattering**: Gas molecules scatter shorter wavelengths more than longer ones
4. **Blue Light Dominance**: Blue light (short wavelength) is scattered in all directions
5. **Our Perspective**: From the ground, we see the scattered blue light coming from all directions
6. **Result**: This makes the sky appear blue to our eyes"""
        
        elif "planet" in question_lower and "hottest" in question_lower:
            return """Step-by-step reasoning about the hottest planet:

1. **Understanding Planetary Heat**: Planets get heat from two sources:
   • Distance from the sun
   • Atmospheric composition
2. **Mercury Analysis**: Closest to the sun, but no atmosphere to trap heat
3. **Venus Analysis**: Second closest, but has thick CO2 atmosphere
4. **Greenhouse Effect**: Venus's atmosphere traps heat extremely effectively
5. **Temperature Comparison**:
   • Mercury: ~800°F (day), -290°F (night)
   • Venus: ~900°F (constant, day and night)
6. **Conclusion**: Venus is the hottest planet due to its greenhouse effect"""
        
        elif any(op in question_lower for op in ["+", "plus", "add", "multiply", "times", "divide", "subtract", "minus"]):
            return """Step-by-step response to mathematical question:

1. **Question Analysis**: You're asking for a mathematical calculation
2. **Tool Requirement**: I cannot perform calculations directly
3. **Recommended Solution**: You should use a calculator tool for this
4. **Why**: Mathematical operations require precise computation tools
5. **Suggestion**: Try asking me to use a calculator tool, or use a calculator yourself

I'm designed to help with reasoning and explanations, but for calculations, I need specialized tools."""
        
        else:
            return """Step-by-step response:

1. **Question Analysis**: I understand your question
2. **Knowledge Application**: I would need to access current information
3. **Structured Response**: I would provide a clear, step-by-step answer
4. **Formatting**: I would use bullet points and clear structure
5. **Note**: In fallback mode, I have limited knowledge. For best results, configure an API key."""

    def get_response(self, user_question: str) -> str:
        """Get response from appropriate LLM"""
        prompt = self.create_prompt(user_question)
        
        if self.llm_type == "openai":
            return self.call_openai(prompt)
        elif self.llm_type == "gemini":
            return self.call_gemini(prompt)
        else:
            return self.fallback_response(user_question)
    
    def log_interaction(self, user_question: str, response: str):
        """Log the interaction"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_question": user_question,
            "response": response,
            "llm_type": self.llm_type
        }
        self.conversation_history.append(interaction)
        
        # Save to file
        log_file = "interaction_logs_level1.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {interaction['timestamp']}\n")
            f.write(f"LLM Type: {interaction['llm_type']}\n")
            f.write(f"User Question: {interaction['user_question']}\n")
            f.write(f"Response:\n{interaction['response']}\n")
            f.write(f"{'='*50}\n")
    
    def run(self):
        """Main chatbot loop"""
        print("🤖 Level 1: LLM-Only Smart Assistant")
        print("=" * 50)
        print("This chatbot uses prompt engineering for step-by-step reasoning.")
        print("Type 'quit' to exit.")
        print(f"LLM Provider: {self.llm_type}")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Thanks for using the Level 1 chatbot.")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤖 Assistant: Thinking...")
                response = self.get_response(user_input)
                print(f"\n{response}")
                
                # Log the interaction
                self.log_interaction(user_input, response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Level 1 chatbot.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function"""
    # Validate configuration
    Config.validate_config()
    
    # Create and run chatbot
    chatbot = LLMOnlyChatbot()
    chatbot.run()

if __name__ == "__main__":
    main() 