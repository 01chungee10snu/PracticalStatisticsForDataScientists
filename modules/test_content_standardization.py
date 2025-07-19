"""
Tests for the content standardization module
"""

import os
import unittest
from modules.content_standardization import TemplateEngine, DifficultyLevel, ContentTemplate


class TestTemplateEngine(unittest.TestCase):
    """Test cases for the TemplateEngine class"""
    
    def setUp(self):
        """Set up test environment"""
        self.engine = TemplateEngine()
    
    def test_get_template(self):
        """Test getting templates for different difficulty levels"""
        for level in DifficultyLevel:
            template = self.engine.get_template(level.value)
            self.assertIsInstance(template, ContentTemplate)
            self.assertEqual(template.difficulty_level, level)
    
    def test_invalid_difficulty_level(self):
        """Test getting template with invalid difficulty level"""
        with self.assertRaises(ValueError):
            self.engine.get_template("invalid_level")
    
    def test_apply_template(self):
        """Test applying template to content data"""
        content_data = {
            'title': 'Test Content',
            'difficulty_level': 'foundation',
            'sections': {
                'concept_introduction': {
                    'content': 'This is a test concept introduction.'
                }
            }
        }
        
        result = self.engine.apply_template(content_data)
        
        # Check that template was applied correctly
        self.assertEqual(result['title'], 'Test Content')
        self.assertEqual(result['difficulty_level'], 'foundation')
        
        # Check that required sections were added
        self.assertIn('visual_explanation', result['sections'])
        self.assertIn('practical_example', result['sections'])
        self.assertIn('common_misconceptions', result['sections'])
        self.assertIn('self_assessment', result['sections'])
    
    def test_validate_against_template_valid(self):
        """Test validating valid content against template"""
        content_data = {
            'title': 'Test Content',
            'difficulty_level': 'foundation',
            'sections': {
                'concept_introduction': {
                    'content': ' '.join(['word'] * 100)  # 100 words
                },
                'visual_explanation': {
                    'content': 'This is a visual explanation.'
                },
                'practical_example': {
                    'content': 'This is a practical example.\n```python\nprint("Hello, world!")\n```'
                },
                'common_misconceptions': {
                    'content': '- Misconception 1\n- Misconception 2'
                },
                'self_assessment': {
                    'content': '1. Question 1\n2. Question 2\n3. Question 3'
                }
            }
        }
        
        is_valid, issues = self.engine.validate_against_template(content_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)
    
    def test_validate_against_template_invalid(self):
        """Test validating invalid content against template"""
        content_data = {
            'title': 'Test Content',
            'difficulty_level': 'foundation',
            'sections': {
                'concept_introduction': {
                    'content': 'Too short'  # Less than 100 words
                },
                'visual_explanation': {
                    'content': 'This is a visual explanation.'
                },
                'practical_example': {
                    'content': 'This is a practical example without code block.'
                },
                'common_misconceptions': {
                    'content': '- Only one misconception'  # Less than 2 items
                },
                'self_assessment': {
                    'content': '1. Only one question'  # Less than 3 questions
                }
            }
        }
        
        is_valid, issues = self.engine.validate_against_template(content_data)
        self.assertFalse(is_valid)
        self.assertGreater(len(issues), 0)
    
    def test_generate_markdown(self):
        """Test generating markdown from content data"""
        content_data = {
            'title': 'Test Content',
            'difficulty_level': 'foundation',
            'estimated_time': 20,
            'prerequisites': ['Basic Math'],
            'sections': {
                'concept_introduction': {
                    'content': 'This is a concept introduction.'
                },
                'visual_explanation': {
                    'content': 'This is a visual explanation.'
                }
            }
        }
        
        markdown = self.engine.generate_markdown(content_data)
        
        # Check that markdown contains expected elements
        self.assertIn('# Test Content', markdown)
        self.assertIn('**난이도:** foundation', markdown)
        self.assertIn('**예상 소요 시간:** 20분', markdown)
        self.assertIn('**선수 지식:**', markdown)
        self.assertIn('- Basic Math', markdown)
        self.assertIn('## Concept Introduction', markdown)
        self.assertIn('This is a concept introduction.', markdown)
        self.assertIn('## Visual Explanation', markdown)
        self.assertIn('This is a visual explanation.', markdown)


if __name__ == '__main__':
    unittest.main()