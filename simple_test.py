#!/usr/bin/env python3

# Simple test for content standardization
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module
try:
    import modules.content_standardization as cs
    print("Module imported successfully")
    print("Available classes:", [name for name in dir(cs) if not name.startswith('_')])
    
    # Try to create instances
    standardizer = cs.ContentStandardizer()
    print("ContentStandardizer created successfully")
    
    # Test basic functionality
    test_data = {
        'title': 'Test Content',
        'difficulty_level': 'foundation',
        'sections': {
            'concept_introduction': {
                'content': 'This is a test content for the concept introduction section.'
            }
        }
    }
    
    result = standardizer.standardize_content(test_data)
    print("Content standardization successful")
    print(f"Result has {len(result['sections'])} sections")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()