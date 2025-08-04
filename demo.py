"""
Demo Script for LLM + Agentic Thinking Application
Showcases all three levels with example interactions
"""

import os
import sys
import time

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n{step_num}. {description}")

def demo_level1():
    """Demo Level 1: LLM-Only Smart Assistant"""
    print_header("Level 1: LLM-Only Smart Assistant")
    print("This level demonstrates prompt engineering for step-by-step reasoning.")
    print("The chatbot refuses math calculations and suggests using tools.")
    
    print_step(1, "Running Level 1 chatbot...")
    print("Example interactions:")
    print("  • 'What are the colors in a rainbow?' → Step-by-step explanation")
    print("  • 'Tell me why the sky is blue?' → Step-by-step explanation")
    print("  • 'Which planet is the hottest?' → Step-by-step reasoning")
    print("  • 'What is 15 + 23?' → Refuses calculation, suggests calculator tool")
    
    print("\nTo test Level 1:")
    print("  cd level1")
    print("  python chatbot.py")

def demo_level2():
    """Demo Level 2: LLM + Basic Tool Use"""
    print_header("Level 2: LLM + Basic Tool Use")
    print("This level extends Level 1 with calculator tool integration.")
    print("Math operations are automatically detected and calculated.")
    
    print_step(1, "Running Level 2 chatbot with calculator tool...")
    print("Example interactions:")
    print("  • 'What is 12 times 7?' → Uses calculator tool")
    print("  • 'Add 45 and 30' → Uses calculator tool")
    print("  • 'What is the capital of France?' → Direct LLM answer")
    print("  • 'Multiply 9 and 8, and also tell me the capital of Japan.' → Graceful failure")
    
    print("\nTo test Level 2:")
    print("  cd level2")
    print("  python chatbot_with_tool.py")

def demo_level3():
    """Demo Level 3: Full Agentic AI with Multi-Step Tasks"""
    print_header("Level 3: Full Agentic AI with Multi-Step Tasks")
    print("This level demonstrates complete agentic behavior with multi-step reasoning.")
    print("Multiple tools are orchestrated to handle complex queries.")
    
    print_step(1, "Running Level 3 full agent...")
    print("Example interactions:")
    print("  • 'Translate \"Good Morning\" into German and then multiply 5 and 6.' → Multi-step")
    print("  • 'Add 10 and 20, then translate \"Have a nice day\" into German.' → Multi-step")
    print("  • 'Tell me the capital of Italy, then multiply 12 and 12.' → Multi-step")
    print("  • 'Translate \"Sunshine\" into German.' → Single step")
    print("  • 'Add 2 and 2 and multiply 3 and 3.' → Multiple calculations")
    print("  • 'What is the distance between Earth and Mars?' → LLM direct answer")
    
    print("\nTo test Level 3:")
    print("  cd level3")
    print("  python full_agent.py")

def show_project_structure():
    """Show the project structure"""
    print_header("Project Structure")
    
    structure = """
college project/
├── README.md                    # Comprehensive documentation
├── requirements.txt             # Python dependencies
├── config.py                    # Configuration and API settings
├── demo.py                      # This demo script
├── level1/
│   ├── chatbot.py              # Level 1: LLM-only chatbot
│   └── interaction_logs_level1.txt
├── level2/
│   ├── chatbot_with_tool.py    # Level 2: Chatbot + calculator
│   ├── calculator_tool.py      # Calculator tool implementation
│   └── interaction_logs_level2.txt
├── level3/
│   ├── full_agent.py           # Level 3: Full agentic AI
│   ├── calculator_tool.py      # Calculator tool (copied)
│   ├── translator_tool.py      # Translator tool implementation
│   └── interaction_logs_level3.txt
└── logs/
    └── full_history.json       # Complete interaction history
"""
    print(structure)

def show_features_comparison():
    """Show features comparison across levels"""
    print_header("Features Comparison")
    
    comparison = """
| Feature | Level 1 | Level 2 | Level 3 |
|---------|---------|---------|---------|
| LLM Integration | ✅ | ✅ | ✅ |
| Step-by-step Reasoning | ✅ | ✅ | ✅ |
| Tool Integration | ❌ | ✅ (Calculator) | ✅ (Multiple) |
| Multi-step Tasks | ❌ | ❌ | ✅ |
| Memory/Context | ❌ | ❌ | ✅ |
| Complex Query Parsing | ❌ | ❌ | ✅ |
| Graceful Failure | ✅ | ✅ | ✅ |
| Interaction Logging | ✅ | ✅ | ✅ |
"""
    print(comparison)

def show_mandatory_use_cases():
    """Show mandatory use cases for each level"""
    print_header("Mandatory Use Cases")
    
    print("\n🟢 Level 1 - LLM-Only:")
    print("  • 'What are the colors in a rainbow?' → List step-by-step")
    print("  • 'Tell me why the sky is blue?' → Step-by-step explanation")
    print("  • 'Which planet is the hottest?' → Reason and explain")
    print("  • 'What is 15 + 23?' → Must refuse and hint at calculator tool")
    
    print("\n🟡 Level 2 - LLM + Basic Tool:")
    print("  • 'What is 12 times 7?' → Use calculator tool")
    print("  • 'Add 45 and 30' → Use calculator tool")
    print("  • 'What is the capital of France?' → Direct LLM answer")
    print("  • 'Multiply 9 and 8, and also tell me the capital of Japan.' → Graceful failure")
    
    print("\n🔴 Level 3 - Full Agentic AI:")
    print("  • 'Translate \"Good Morning\" into German and then multiply 5 and 6.'")
    print("  • 'Add 10 and 20, then translate \"Have a nice day\" into German.'")
    print("  • 'Tell me the capital of Italy, then multiply 12 and 12.'")
    print("  • 'Translate \"Sunshine\" into German.' (only one step)")
    print("  • 'Add 2 and 2 and multiply 3 and 3.'")
    print("  • 'What is the distance between Earth and Mars?' (LLM direct answer)")

def show_setup_instructions():
    """Show setup instructions"""
    print_header("Setup Instructions")
    
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n2. Configure API keys (optional):")
    print("   Create a .env file with:")
    print("   OPENAI_API_KEY=your_openai_api_key_here")
    print("   GEMINI_API_KEY=your_gemini_api_key_here")
    
    print("\n3. Run any level:")
    print("   cd level1 && python chatbot.py")
    print("   cd level2 && python chatbot_with_tool.py")
    print("   cd level3 && python full_agent.py")
    
    print("\nNote: Without API keys, the system runs in fallback mode")
    print("with pre-programmed responses for demonstration purposes.")

def main():
    """Main demo function"""
    print_header("LLM + Agentic Thinking Python Application")
    print("A comprehensive demonstration of LLM integration and agentic AI capabilities")
    print("across three progressive levels of complexity.")
    
    while True:
        print("\n" + "="*60)
        print("🎮 Demo Menu:")
        print("1. Show Project Structure")
        print("2. Show Features Comparison")
        print("3. Show Mandatory Use Cases")
        print("4. Demo Level 1")
        print("5. Demo Level 2")
        print("6. Demo Level 3")
        print("7. Show Setup Instructions")
        print("8. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            show_project_structure()
        elif choice == '2':
            show_features_comparison()
        elif choice == '3':
            show_mandatory_use_cases()
        elif choice == '4':
            demo_level1()
        elif choice == '5':
            demo_level2()
        elif choice == '6':
            demo_level3()
        elif choice == '7':
            show_setup_instructions()
        elif choice == '8':
            print("\n👋 Thank you for exploring the LLM + Agentic Thinking Application!")
            print("Check out the README.md for detailed documentation.")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-8.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 