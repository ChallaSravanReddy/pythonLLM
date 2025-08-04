"""
Level 3: Full Agentic AI with Multi-Step Tasks
Complete agentic system with multi-step reasoning and tool orchestration.
"""

import sys
import os
import json
import re
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from calculator_tool import CalculatorTool
from translator_tool import TranslatorTool

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

class TaskStep:
    """Represents a single step in a multi-step task"""
    
    def __init__(self, description: str, tool_type: Optional[str] = None, parameters: Optional[Dict] = None):
        self.description = description
        self.tool_type = tool_type  # 'calculator', 'translator', 'llm', or None
        self.parameters = parameters or {}
        self.result = None
        self.completed = False
        self.error = None

class FullAgent:
    """Level 3: Full agentic AI with multi-step task processing"""
    
    def __init__(self):
        self.config = Config.get_llm_config()
        self.conversation_history = []
        self.calculator = CalculatorTool()
        self.translator = TranslatorTool()
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
    
    def analyze_query(self, user_query: str) -> List[TaskStep]:
        """Analyze user query and break it down into steps"""
        steps = []
        query_lower = user_query.lower()
        
        # Check for translation requests
        translation_request = self.translator.detect_translation_request(user_query)
        if translation_request:
            steps.append(TaskStep(
                description=f"Translate '{translation_request['english_text']}' to German",
                tool_type="translator",
                parameters={"english_text": translation_request['english_text']}
            ))
        
        # Check for math operations
        math_operations = self.extract_math_operations(user_query)
        for i, math_op in enumerate(math_operations):
            steps.append(TaskStep(
                description=f"Calculate {math_op['expression']}",
                tool_type="calculator",
                parameters=math_op
            ))
        
        # Check for general knowledge questions
        knowledge_questions = self.extract_knowledge_questions(user_query)
        for question in knowledge_questions:
            steps.append(TaskStep(
                description=f"Answer: {question}",
                tool_type="llm",
                parameters={"question": question}
            ))
        
        # If no specific operations detected, treat as general question
        if not steps:
            steps.append(TaskStep(
                description=f"Process query: {user_query}",
                tool_type="llm",
                parameters={"question": user_query}
            ))
        
        return steps
    
    def extract_math_operations(self, text: str) -> List[Dict[str, Any]]:
        """Extract multiple math operations from text"""
        operations = []
        
        # Look for patterns like "add X and Y and multiply A and B"
        add_patterns = [
            r'add\s+(\d+)\s+and\s+(\d+)',
            r'(\d+)\s*\+\s*(\d+)',
            r'(\d+)\s+plus\s+(\d+)'
        ]
        
        multiply_patterns = [
            r'multiply\s+(\d+)\s+and\s+(\d+)',
            r'(\d+)\s*\*\s*(\d+)',
            r'(\d+)\s+times\s+(\d+)'
        ]
        
        # Find all addition operations
        for pattern in add_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                operations.append({
                    'operation': '+',
                    'operand1': float(match.group(1)),
                    'operand2': float(match.group(2)),
                    'expression': f"{match.group(1)} + {match.group(2)}"
                })
        
        # Find all multiplication operations
        for pattern in multiply_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                operations.append({
                    'operation': '*',
                    'operand1': float(match.group(1)),
                    'operand2': float(match.group(2)),
                    'expression': f"{match.group(1)} × {match.group(2)}"
                })
        
        return operations
    
    def extract_knowledge_questions(self, text: str) -> List[str]:
        """Extract general knowledge questions from text"""
        questions = []
        
        # Look for patterns that indicate knowledge questions
        patterns = [
            r'tell\s+me\s+(.+?)(?:\s+and\s+|\s+then\s+|$)',
            r'what\s+is\s+(?:the\s+)?(.+?)(?:\s+and\s+|\s+then\s+|$)',
            r'which\s+(.+?)(?:\s+and\s+|\s+then\s+|$)',
            r'capital\s+of\s+(\w+)',
            r'distance\s+between\s+(.+?)(?:\s+and\s+|\s+then\s+|$)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                question = match.group(1).strip()
                if question and len(question) > 3:  # Avoid very short matches
                    questions.append(question)
        
        return questions
    
    def execute_step(self, step: TaskStep) -> Dict[str, Any]:
        """Execute a single task step"""
        try:
            if step.tool_type == "calculator":
                result = self.calculator.calculate(
                    step.parameters['operation'],
                    step.parameters['operand1'],
                    step.parameters['operand2']
                )
                step.result = result
                step.completed = True
                return result
                
            elif step.tool_type == "translator":
                result = self.translator.translate(step.parameters['english_text'])
                step.result = result
                step.completed = True
                return result
                
            elif step.tool_type == "llm":
                prompt = self.create_prompt(step.parameters['question'])
                if self.llm_type == "openai":
                    result = self.call_openai(prompt)
                elif self.llm_type == "gemini":
                    result = self.call_gemini(prompt)
                else:
                    result = self.fallback_response(step.parameters['question'])
                
                step.result = {"response": result}
                step.completed = True
                return step.result
                
            else:
                step.error = "Unknown tool type"
                step.completed = False
                return {"error": "Unknown tool type"}
                
        except Exception as e:
            step.error = str(e)
            step.completed = False
            return {"error": str(e)}
    
    def create_prompt(self, question: str) -> str:
        """Create a prompt for LLM queries"""
        return f"""You are a helpful AI assistant that ALWAYS thinks step-by-step and provides structured, clear responses.

IMPORTANT RULES:
1. ALWAYS break down your response into clear, numbered steps
2. Use bullet points and formatting to make your response easy to read
3. Be thorough but concise in your explanations

User Question: {question}

Please provide your step-by-step response:"""
    
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
    
    def fallback_response(self, question: str) -> str:
        """Fallback response for knowledge questions"""
        question_lower = question.lower()
        
        if "capital" in question_lower and "italy" in question_lower:
            return """Step-by-step answer about Italy's capital:

1. **Question Analysis**: You're asking about the capital of Italy
2. **Geographic Knowledge**: Italy is a country in Southern Europe
3. **Capital City**: The capital of Italy is Rome
4. **Historical Significance**: Rome has been Italy's capital since 1871
5. **Cultural Importance**: Rome is known as the "Eternal City" and is famous for its ancient history, art, and architecture"""
        
        elif "distance" in question_lower and "earth" in question_lower and "mars" in question_lower:
            return """Step-by-step answer about Earth-Mars distance:

1. **Question Analysis**: You're asking about the distance between Earth and Mars
2. **Orbital Dynamics**: Both planets orbit the sun at different speeds and distances
3. **Variable Distance**: The distance varies due to their elliptical orbits
4. **Range**: The distance ranges from about 54.6 million km (closest) to 401 million km (farthest)
5. **Average Distance**: On average, Earth and Mars are about 225 million km apart
6. **Current Context**: The exact distance depends on the current positions in their orbits"""
        
        else:
            return f"""Step-by-step response to: {question}

1. **Question Analysis**: I understand your question about {question}
2. **Knowledge Application**: I would need to access current information
3. **Structured Response**: I would provide a clear, step-by-step answer
4. **Formatting**: I would use bullet points and clear structure
5. **Note**: In fallback mode, I have limited knowledge. For best results, configure an API key."""
    
    def synthesize_results(self, steps: List[TaskStep], original_query: str) -> str:
        """Synthesize results from all steps into a coherent response"""
        if len(steps) == 1:
            # Single step - return result directly
            step = steps[0]
            if step.tool_type == "calculator" and step.result.get('success'):
                return f"""Step-by-step response:

1. **Question Analysis**: You asked for a mathematical calculation
2. **Tool Usage**: I used the calculator tool
3. **Calculation**: {step.result['expression']}
4. **Result**: The answer is {step.result['result']}"""
            
            elif step.tool_type == "translator" and step.result.get('success'):
                return f"""Step-by-step response:

1. **Question Analysis**: You asked for a translation
2. **Tool Usage**: I used the translator tool
3. **Translation**: '{step.result['english_text']}' → '{step.result['german_translation']}'
4. **Result**: The German translation is '{step.result['german_translation']}'"""
            
            elif step.tool_type == "llm":
                return step.result.get('response', 'No response available')
            
            else:
                return f"Error in processing: {step.error or 'Unknown error'}"
        
        else:
            # Multiple steps - synthesize results
            response_parts = ["Step-by-step multi-task response:"]
            
            for i, step in enumerate(steps, 1):
                response_parts.append(f"\n{i}. **{step.description}**")
                
                if step.completed:
                    if step.tool_type == "calculator" and step.result.get('success'):
                        response_parts.append(f"   Result: {step.result['expression']}")
                    elif step.tool_type == "translator" and step.result.get('success'):
                        response_parts.append(f"   Result: '{step.result['german_translation']}'")
                    elif step.tool_type == "llm":
                        response_parts.append(f"   Result: {step.result.get('response', 'No response')}")
                else:
                    response_parts.append(f"   Error: {step.error}")
            
            response_parts.append(f"\n**Summary**: Successfully completed {len([s for s in steps if s.completed])} out of {len(steps)} tasks.")
            
            return "\n".join(response_parts)
    
    def process_query(self, user_query: str) -> str:
        """Process user query with multi-step reasoning"""
        print(f"\n🔍 Analyzing query: {user_query}")
        
        # Step 1: Analyze and break down the query
        steps = self.analyze_query(user_query)
        print(f"📋 Identified {len(steps)} task(s):")
        for i, step in enumerate(steps, 1):
            print(f"   {i}. {step.description}")
        
        # Step 2: Execute each step
        print(f"\n⚙️  Executing tasks...")
        for i, step in enumerate(steps, 1):
            print(f"   {i}. Executing: {step.description}")
            result = self.execute_step(step)
            if step.completed:
                print(f"      ✅ Completed")
            else:
                print(f"      ❌ Failed: {step.error}")
        
        # Step 3: Synthesize results
        print(f"\n📝 Synthesizing results...")
        final_response = self.synthesize_results(steps, user_query)
        
        return final_response
    
    def log_interaction(self, user_question: str, response: str, steps: List[TaskStep]):
        """Log the interaction with full context"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_question": user_question,
            "response": response,
            "llm_type": self.llm_type,
            "steps": [
                {
                    "description": step.description,
                    "tool_type": step.tool_type,
                    "parameters": step.parameters,
                    "completed": step.completed,
                    "result": step.result,
                    "error": step.error
                }
                for step in steps
            ]
        }
        self.conversation_history.append(interaction)
        
        # Save to file
        log_file = "interaction_logs_level3.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Timestamp: {interaction['timestamp']}\n")
            f.write(f"LLM Type: {interaction['llm_type']}\n")
            f.write(f"User Question: {interaction['user_question']}\n")
            f.write(f"Steps Executed: {len(interaction['steps'])}\n")
            for i, step in enumerate(interaction['steps'], 1):
                f.write(f"  Step {i}: {step['description']} ({step['tool_type'] or 'none'})\n")
                f.write(f"    Completed: {step['completed']}\n")
                if step['error']:
                    f.write(f"    Error: {step['error']}\n")
            f.write(f"Response:\n{interaction['response']}\n")
            f.write(f"{'='*50}\n")
        
        # Also save to JSON for full history
        json_file = "../logs/full_history.json"
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []
        
        history.append(interaction)
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    def run(self):
        """Main agent loop"""
        print("🤖 Level 3: Full Agentic AI with Multi-Step Tasks")
        print("=" * 60)
        print("This agent can handle complex multi-step tasks with multiple tools.")
        print("Type 'quit' to exit.")
        print(f"LLM Provider: {self.llm_type}")
        print("Available Tools: Calculator, Translator, LLM")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Thanks for using the Level 3 agent.")
                    break
                
                if not user_input:
                    continue
                
                # Process the query
                response = self.process_query(user_input)
                print(f"\n🤖 Agent: {response}")
                
                # Log the interaction
                steps = self.analyze_query(user_input)
                self.log_interaction(user_input, response, steps)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Thanks for using the Level 3 agent.")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

def main():
    """Main function"""
    # Validate configuration
    Config.validate_config()
    
    # Create and run agent
    agent = FullAgent()
    agent.run()

if __name__ == "__main__":
    main() 