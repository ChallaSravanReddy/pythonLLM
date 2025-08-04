"""
Translator Tool for Level 3
Handles English to German translation
"""

import re
from typing import Dict, Any, Optional

class TranslatorTool:
    """Translator tool for English to German translation"""
    
    def __init__(self):
        # Simple English to German dictionary for common phrases
        # In a real implementation, this would use a translation API
        self.translation_dict = {
            'good morning': 'Guten Morgen',
            'good afternoon': 'Guten Tag',
            'good evening': 'Guten Abend',
            'good night': 'Gute Nacht',
            'hello': 'Hallo',
            'hi': 'Hallo',
            'goodbye': 'Auf Wiedersehen',
            'thank you': 'Danke',
            'please': 'Bitte',
            'yes': 'Ja',
            'no': 'Nein',
            'sunshine': 'Sonnenschein',
            'have a nice day': 'Einen schönen Tag noch',
            'how are you': 'Wie geht es dir',
            'i am fine': 'Mir geht es gut',
            'welcome': 'Willkommen',
            'excuse me': 'Entschuldigung',
            'sorry': 'Entschuldigung',
            'water': 'Wasser',
            'bread': 'Brot',
            'house': 'Haus',
            'car': 'Auto',
            'book': 'Buch',
            'friend': 'Freund',
            'family': 'Familie',
            'work': 'Arbeit',
            'school': 'Schule',
            'time': 'Zeit',
            'day': 'Tag',
            'night': 'Nacht',
            'morning': 'Morgen',
            'afternoon': 'Nachmittag',
            'evening': 'Abend',
            'week': 'Woche',
            'month': 'Monat',
            'year': 'Jahr',
            'today': 'Heute',
            'tomorrow': 'Morgen',
            'yesterday': 'Gestern',
            'big': 'Groß',
            'small': 'Klein',
            'good': 'Gut',
            'bad': 'Schlecht',
            'beautiful': 'Schön',
            'ugly': 'Hässlich',
            'hot': 'Heiß',
            'cold': 'Kalt',
            'new': 'Neu',
            'old': 'Alt',
            'young': 'Jung',
            'happy': 'Glücklich',
            'sad': 'Traurig',
            'angry': 'Wütend',
            'tired': 'Müde',
            'hungry': 'Hungrig',
            'thirsty': 'Durstig',
            'love': 'Liebe',
            'hate': 'Hass',
            'like': 'Gefallen',
            'want': 'Wollen',
            'need': 'Brauchen',
            'can': 'Können',
            'must': 'Müssen',
            'should': 'Sollten',
            'will': 'Werden',
            'would': 'Würden',
            'could': 'Könnten',
            'may': 'Dürfen',
            'might': 'Könnten'
        }
    
    def detect_translation_request(self, text: str) -> Optional[Dict[str, Any]]:
        """Detect if text contains a translation request"""
        text_lower = text.lower()
        
        # Patterns for translation requests
        patterns = [
            r'translate\s+[\'"]([^\'"]+)[\'"]\s+into\s+german',
            r'translate\s+[\'"]([^\'"]+)[\'"]\s+to\s+german',
            r'[\'"]([^\'"]+)[\'"]\s+in\s+german',
            r'how\s+do\s+you\s+say\s+[\'"]([^\'"]+)[\'"]\s+in\s+german',
            r'german\s+for\s+[\'"]([^\'"]+)[\'"]',
            r'what\s+is\s+[\'"]([^\'"]+)[\'"]\s+in\s+german'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                english_text = match.group(1).strip()
                return {
                    'english_text': english_text,
                    'target_language': 'german',
                    'original_text': text
                }
        
        return None
    
    def translate(self, english_text: str) -> Dict[str, Any]:
        """Translate English text to German"""
        try:
            english_lower = english_text.lower().strip()
            
            # Check if we have a direct translation
            if english_lower in self.translation_dict:
                german_translation = self.translation_dict[english_lower]
                return {
                    'success': True,
                    'english_text': english_text,
                    'german_translation': german_translation,
                    'confidence': 'high'
                }
            
            # Try to translate word by word for simple phrases
            words = english_lower.split()
            translated_words = []
            
            for word in words:
                if word in self.translation_dict:
                    translated_words.append(self.translation_dict[word])
                else:
                    # For unknown words, provide a placeholder
                    translated_words.append(f"[{word}]")
            
            if translated_words:
                german_translation = ' '.join(translated_words)
                return {
                    'success': True,
                    'english_text': english_text,
                    'german_translation': german_translation,
                    'confidence': 'partial',
                    'note': 'Some words may not be accurately translated'
                }
            
            # If no translation found
            return {
                'success': False,
                'english_text': english_text,
                'error': 'Translation not available for this text',
                'suggestion': 'Try a simpler phrase or common words'
            }
            
        except Exception as e:
            return {
                'success': False,
                'english_text': english_text,
                'error': str(e)
            }
    
    def process_query(self, text: str) -> Optional[Dict[str, Any]]:
        """Process a text query and return translation result if applicable"""
        translation_request = self.detect_translation_request(text)
        
        if translation_request:
            result = self.translate(translation_request['english_text'])
            result['original_query'] = text
            return result
        
        return None
    
    def format_result(self, result: Dict[str, Any]) -> str:
        """Format the translation result for display"""
        if result['success']:
            confidence_note = f" (Confidence: {result['confidence']})" if 'confidence' in result else ""
            note = f"\nNote: {result['note']}" if 'note' in result else ""
            return f"🌍 Translation Result: '{result['english_text']}' → '{result['german_translation']}'{confidence_note}{note}"
        else:
            return f"❌ Translation Error: {result['error']}"

# Example usage and testing
if __name__ == "__main__":
    translator = TranslatorTool()
    
    # Test cases
    test_queries = [
        "Translate 'Good Morning' into German",
        "What is 'Have a nice day' in German?",
        "Translate 'Sunshine' to German",
        "How do you say 'Hello' in German?",
        "What is the capital of Italy?",
        "Add 10 and 20"
    ]
    
    print("🌍 Translator Tool Test")
    print("=" * 40)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = translator.process_query(query)
        if result:
            print(f"Result: {translator.format_result(result)}")
        else:
            print("Result: No translation request detected") 