# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Korean-language statistics education platform called "PracticalStatisticsForDataScientists" that provides interactive learning through multiple interfaces (CLI, web, and notebooks). The system features adaptive learning, personalized content delivery, and comprehensive statistical tutorials across three skill levels.

## Common Development Commands

### Running the Application
- **Main CLI Interface**: `python main.py` - Interactive menu system with multiple learning modes
- **Web Interface**: `python webapp.py` - Flask-based web server (default port 5000)
- **Standalone Demo**: `python modules/standalone_demo.py` - Self-contained learning system demo
- **Test System**: `python test_standalone.py` - Automated testing of the learning system

### Development and Testing
- **Validate Documentation**: `python validate_docs.py` - Checks all documentation files exist and are properly linked
- **Interactive Demo**: Start Jupyter and open `notebooks/interactive_demo.ipynb`

### Dependencies
- Install requirements: `pip install -r requirements.txt`
- Core dependencies: Flask, pandas, matplotlib, seaborn, numpy, scikit-learn, plotly, ipywidgets, markdown

## Architecture Overview

### Core System Components
- **`main.py`**: Primary entry point with CLI launcher and multiple learning modes
- **`webapp.py`**: Flask web application providing browser-based interface
- **`modules/standalone_demo.py`**: Self-contained learning system with no external dependencies
- **`modules/adaptive_learning_engine.py`**: Personalized learning path optimization
- **`modules/cognitive_load_optimizer.py`**: Dynamic difficulty adjustment based on performance
- **`modules/content_integration.py`**: Unified content management across skill levels

### Learning Content Structure
The educational content is organized in three progressive levels:

1. **Beginner (`docs/beginner/`)**: 13 chapters on qualitative research methodology
2. **Intermediate (`docs/intermediate/`)**: 4 chapters on factor analysis theory  
3. **Advanced (`docs/advanced/`)**: 8 chapters on statistical learning and machine learning

### Key Data Flow
1. User interacts through CLI, web interface, or notebook
2. Adaptive learning engine analyzes performance and recommends content
3. Cognitive load optimizer adjusts difficulty based on user responses
4. Content integration system delivers unified datasets across skill levels
5. Visualization and tutorial engines provide interactive explanations

### Testing Strategy
The system uses a custom test framework in `test_standalone.py` that validates:
- Learner registration and profile management
- Personalized content recommendation
- Question/answer submission and scoring
- Learning analytics and progress tracking
- Adaptive difficulty adjustment
- System statistics and monitoring

### File Organization
- **`/modules/`**: Core Python modules for learning system functionality
- **`/docs/`**: Educational content organized by skill level with markdown files
- **`/templates/`**: HTML templates for web interface
- **`/notebooks/`**: Jupyter notebooks for interactive demonstrations

### Language and Internationalization
The system is primarily developed in Korean with Korean-language educational content, interface text, and documentation. Variable names and code comments are in Korean.

### Adaptive Learning Features
- Real-time difficulty adjustment based on user performance
- Personalized content recommendation using performance analytics
- Multi-modal learning with text, visualizations, and interactive problems
- Progress tracking with detailed learning analytics
- Cross-reference learning paths between skill levels

### Visualization System
The platform includes sophisticated visualization capabilities:
- Statistical plots and correlation heatmaps
- ASCII visualizations for terminal mode
- Interactive charts using matplotlib, seaborn, and plotly
- Custom visualization widgets for educational content