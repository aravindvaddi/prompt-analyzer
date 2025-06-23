# Contributing to Prompt Analyzer

First off, thank you for considering contributing to Prompt Analyzer! It's people like you that make this tool better for everyone.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct: be respectful, constructive, and professional.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed and expected
* Include screenshots if relevant
* Include your environment details (OS, Python version, Node version, etc.)

### Suggesting Enhancements

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and expected behavior
* Explain why this enhancement would be useful

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Process

1. Clone your fork:
   ```bash
   git clone https://github.com/your-username/prompt-analyzer.git
   cd prompt-analyzer
   ```

2. Set up the development environment:
   ```bash
   # Backend
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   
   # Frontend
   cd ../frontend
   npm install
   ```

3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Make your changes and test:
   ```bash
   # Backend tests
   cd backend
   pytest -v
   ruff check .
   
   # Frontend tests
   cd frontend
   npm test
   npm run lint
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "Add your meaningful commit message"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Open a Pull Request

## Style Guides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Python Style Guide

* Follow PEP 8
* Use ruff for linting and formatting
* Write docstrings for all public functions
* Use type hints where appropriate

### JavaScript Style Guide

* Use ESLint configuration provided
* Use TypeScript for type safety
* Follow React best practices
* Use functional components with hooks

### Documentation Style Guide

* Use Markdown for documentation
* Reference function names with backticks
* Include code examples where helpful
* Keep explanations clear and concise

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing!