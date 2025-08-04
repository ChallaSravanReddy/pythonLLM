"""
Calculator Tool for Level 2
Handles basic mathematical operations
"""

import re
from typing import Dict, Any, Optional

class CalculatorTool:
    """Calculator tool for mathematical operations"""
    
    def __init__(self):
        self.supported_operations = {
            'add': '+',
            'plus': '+',
            'sum': '+',
            'multiply': '*',
            'times': '*',
            'subtract': '-',
            'minus': '-',
            'divide': '/',
            'division': '/'
        }
    
    def detect_math_operation(self, text: str) -> Optional[Dict[str, Any]]:
        """Detect if text contains a mathematical operation"""
        text_lower = text.lower()
        
        # Pattern 1: "What is X + Y?" or "X plus Y"
        patterns = [
            r'what\s+is\s+(\d+)\s*([+\-*/])\s*(\d+)',
            r'(\d+)\s+(plus|minus|times|multiply|divide)\s+(\d+)',
            r'add\s+(\d+)\s+and\s+(\d+)',
            r'multiply\s+(\d+)\s+and\s+(\d+)',
            r'(\d+)\s*\+\s*(\d+)',
            r'(\d+)\s*\*\s*(\d+)',
            r'(\d+)\s*-\s*(\d+)',
            r'(\d+)\s*/\s*(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                groups = match.groups()
                
                if len(groups) == 3:
                    # Pattern: "what is X op Y" or "X op Y"
                    num1 = float(groups[0])
                    op = groups[1]
                    num2 = float(groups[2])
                    
                    # Convert word operations to symbols
                    if op in self.supported_operations:
                        op = self.supported_operations[op]
                    
                elif len(groups) == 2:
                    # Pattern: "add X and Y" or "X + Y"
                    if 'add' in text_lower:
                        num1 = float(groups[0])
                        op = '+'
                        num2 = float(groups[1])
                    elif 'multiply' in text_lower:
                        num1 = float(groups[0])
                        op = '*'
                        num2 = float(groups[1])
                    else:
                        # Direct number patterns
                        num1 = float(groups[0])
                        op = '+'
                        num2 = float(groups[1])
                
                return {
                    'operation': op,
                    'operand1': num1,
                    'operand2': num2,
                    'original_text': text
                }
        
        return None
    
    def calculate(self, operation: str, operand1: float, operand2: float) -> Dict[str, Any]:
        """Perform the mathematical calculation"""
        try:
            if operation == '+':
                result = operand1 + operand2
                operation_name = "addition"
            elif operation == '-':
                result = operand1 - operand2
                operation_name = "subtraction"
            elif operation == '*':
                result = operand1 * operand2
                operation_name = "multiplication"
            elif operation == '/':
                if operand2 == 0:
                    return {
                        'success': False,
                        'error': 'Division by zero is not allowed',
                        'operation': operation_name,
                        'operand1': operand1,
                        'operand2': operand2
                    }
                result = operand1 / operand2
                operation_name = "division"
            else:
                return {
                    'success': False,
                    'error': f'Unsupported operation: {operation}',
                    'operation': operation,
                    'operand1': operand1,
                    'operand2': operand2
                }
            
            return {
                'success': True,
                'result': result,
                'operation': operation_name,
                'operand1': operand1,
                'operand2': operand2,
                'expression': f'{operand1} {operation} {operand2} = {result}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'operation': operation,
                'operand1': operand1,
                'operand2': operand2
            }
    
    def process_query(self, text: str) -> Optional[Dict[str, Any]]:
        """Process a text query and return calculation result if applicable"""
        math_operation = self.detect_math_operation(text)
        
        if math_operation:
            result = self.calculate(
                math_operation['operation'],
                math_operation['operand1'],
                math_operation['operand2']
            )
            result['original_query'] = text
            return result
        
        return None
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """Format the calculation result for display"""
        if result['success']:
            return f"🔢 Calculator Result: {result['expression']}"
        else:
            return f"❌ Calculator Error: {result['error']}"

# Example usage and testing
if __name__ == "__main__":
    calculator = CalculatorTool()
    
    # Test cases
    test_queries = [
        "What is 12 times 7?",
        "Add 45 and 30",
        "What is 15 + 23?",
        "Multiply 9 and 8",
        "What is the capital of France?",
        "Multiply 9 and 8, and also tell me the capital of Japan."
    ]
    
    print("🧮 Calculator Tool Test")
    print("=" * 40)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = calculator.process_query(query)
        if result:
            print(f"Result: {calculator.format_result(result)}")
        else:
            print("Result: No mathematical operation detected") 