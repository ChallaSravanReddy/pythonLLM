# LLM + Agentic Thinking Python Application

This project implements a smart Python application with LLM integration and agentic thinking capabilities across three progressive levels of complexity.

## 🏗️ Project Structure

```
college project/
├── README.md
├── requirements.txt
├── config.py
├── level1/
│   ├── chatbot.py
│   └── interaction_logs_level1.txt
├── level2/
│   ├── chatbot_with_tool.py
│   ├── calculator_tool.py
│   └── interaction_logs_level2.txt
├── level3/
│   ├── full_agent.py
│   ├── calculator_tool.py
│   ├── translator_tool.py
│   └── interaction_logs_level3.txt
└── logs/
    └── full_history.json
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd college-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Create a `.env` file in the root directory
   - Add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## 🟢 Level 1: LLM-Only Smart Assistant

A simple CLI program that uses prompt engineering to force step-by-step thinking.

### Features
- Step-by-step reasoning for all queries
- Structured output formatting
- Refuses math calculations and hints at calculator tool

### Usage
```bash
cd level1
python chatbot.py
```

### Example Interactions
- "What are the colors in a rainbow?"
- "Tell me why the sky is blue?"
- "Which planet is the hottest?"
- "What is 15 + 23?"

## 🟡 Level 2: LLM + Basic Tool Use

Extends Level 1 with calculator tool integration.

### Features
- Automatic math calculation detection
- Calculator tool integration
- Graceful handling of mixed queries

### Usage
```bash
cd level2
python chatbot_with_tool.py
```

### Example Interactions
- "What is 12 times 7?"
- "Add 45 and 30"
- "What is the capital of France?"
- "Multiply 9 and 8, and also tell me the capital of Japan."

## 🔴 Level 3: Full Agentic AI with Multi-Step Tasks

Complete agentic system with multi-step reasoning and tool orchestration.

### Features
- Multi-step task breakdown
- Multiple tool integration (Calculator + Translator)
- Memory and context management
- Complex query handling

### Tools Available
- **Calculator Tool**: Addition, multiplication operations
- **Translator Tool**: English to German translation

### Usage
```bash
cd level3
python full_agent.py
```

### Example Interactions
- "Translate 'Good Morning' into German and then multiply 5 and 6."
- "Add 10 and 20, then translate 'Have a nice day' into German."
- "Tell me the capital of Italy, then multiply 12 and 12."
- "Translate 'Sunshine' into German."
- "Add 2 and 2 and multiply 3 and 3."
- "What is the distance between Earth and Mars?"

## 📊 Features by Level

| Feature | Level 1 | Level 2 | Level 3 |
|---------|---------|---------|---------|
| LLM Integration | ✅ | ✅ | ✅ |
| Step-by-step Reasoning | ✅ | ✅ | ✅ |
| Tool Integration | ❌ | ✅ (Calculator) | ✅ (Multiple) |
| Multi-step Tasks | ❌ | ❌ | ✅ |
| Memory/Context | ❌ | ❌ | ✅ |
| Complex Query Parsing | ❌ | ❌ | ✅ |

## 🔧 Configuration

The application uses a configuration system that supports multiple LLM providers:

- **OpenAI GPT**: Primary LLM for reasoning and responses
- **Gemini**: Alternative LLM option
- **Fallback Mode**: Local reasoning when API is unavailable

## 📝 Logging

All interactions are logged for analysis:
- **Level 1**: Simple text logs
- **Level 2**: Structured text/JSON logs
- **Level 3**: Full history with context and tool usage

## 🧪 Testing

Each level includes example interactions that demonstrate the mandatory use cases. Run the programs and follow the prompts to test all features.

## 📋 Submission Checklist

- ✅ GitHub repository structure
- ✅ Python code files for all levels
- ✅ Comprehensive README.md
- ✅ Interaction logs for each level
- ✅ Requirements and setup instructions
- ✅ Example interactions demonstrating all use cases

## 🤝 Contributing

This is an academic project demonstrating LLM integration and agentic AI concepts. Feel free to extend the functionality or improve the implementation.

## 📄 License

This project is created for educational purposes as part of a college assignment. 