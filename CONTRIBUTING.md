# Contributing to ResearchGraph AI

Thank you for considering contributing to ResearchGraph AI! This document outlines our contribution guidelines.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch (`git checkout -b feature/my-feature`)
4. **Make** your changes
5. **Test** your code
6. **Commit** with clear messages
7. **Push** to your branch
8. **Create** a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ResearchGraph-AI.git
cd ResearchGraph-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools
pip install pytest black flake8
```

## Making Changes

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep lines under 100 characters

### Formatting
```bash
# Format code
black .

# Check code quality
flake8 .
```

### Testing
```bash
# Run tests
python tests.py

# Run specific test
pytest tests.py::TestClassName::test_method -v
```

### Commit Messages
- Use clear, descriptive messages
- Start with a verb (Add, Fix, Update, etc.)
- Example: "Add paper similarity scoring algorithm"

## Areas for Contribution

### Code
- Bug fixes
- Performance improvements
- New features
- Better error handling

### Documentation
- README improvements
- API documentation
- Usage examples
- Tutorials

### Testing
- Unit tests
- Integration tests
- Edge case coverage

### Feedback
- Bug reports
- Feature suggestions
- Documentation feedback

## Pull Request Process

1. **Update** documentation if needed
2. **Add** tests for new features
3. **Ensure** all tests pass
4. **Write** clear PR description
5. **Link** related issues
6. **Wait** for review

## Feature Development

### Adding a New Feature

1. **Create issue** discussing the feature
2. **Get approval** from maintainers
3. **Create branch** from develop
4. **Implement** with tests
5. **Update** documentation
6. **Submit** pull request

### File Structure for New Modules

```python
"""
Module Description
Usage and examples
"""

import logging

logger = logging.getLogger(__name__)

class MyClass:
    """Class description"""
    
    def __init__(self):
        """Initialize"""
        pass
    
    def my_method(self, param: str) -> str:
        """
        Method description
        
        Args:
            param: Parameter description
        
        Returns:
            Description of return value
        """
        pass
```

## Documentation Standards

### Docstrings
```python
def function(param1: str, param2: int) -> bool:
    """
    Brief description of function
    
    Longer description if needed, explaining the purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When input is invalid
        RuntimeError: When something goes wrong
    
    Example:
        >>> result = function("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Reporting Issues

### Bug Reports
Include:
- Clear, descriptive title
- Step-by-step reproduction
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages/stack traces

### Feature Requests
Include:
- Clear description of feature
- Motivation and use cases
- Proposed implementation (if any)
- Examples of desired behavior

## Review Process

1. **Initial Review**: Check for code quality and tests
2. **Testing**: Run automated tests
3. **Feedback**: Request changes if needed
4. **Approval**: Approve once ready
5. **Merge**: Merge to main branch

## Licensing

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Open an issue for questions
- Check existing discussions
- Reach out to maintainers

## Thank You! 🙏

Your contributions make ResearchGraph AI better for everyone!

---

**Last Updated**: May 2026
