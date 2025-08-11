# AI Python Starter Template

A comprehensive Python starter template with AI integration boilerplate code and a clear project structure. This template provides everything you need to get started on an AI-related Python project with modern development practices and tools.

## Features

- **Modern Python Setup**: Python 3.11+ with proper project structure
- **AI Integration Ready**: Boilerplate code for AI/ML projects
- **Development Tools**: Black, isort, ruff, mypy for code quality
- **Testing Framework**: pytest with example tests
- **Configuration Management**: Pydantic-based settings with environment variables
- **Logging**: Structured logging with Loguru
- **CLI Interface**: Command-line interface with argparse
- **CI/CD**: GitHub Actions workflow for automated testing and linting
- **Documentation**: Clear project structure and usage examples

## Setup

### Prerequisites

- Python 3.11 or higher
- pip or poetry for package management

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jbastruz/ai-python-starter-template.git
cd ai-python-starter-template
```

2. Install dependencies:
```bash
make install
# or manually:
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Command Line Interface

Run the main CLI application:
```bash
make run
# or directly:
python -m src.ai_starter.main
```

### Development Commands

Use the included Makefile for common development tasks:

```bash
# Install dependencies
make install

# Format code
make format

# Run linting
make lint

# Run tests
make test

# Run the application
make run
```

## Project Structure

```
ai-python-starter-template/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── src/
│   └── ai_starter/
│       ├── __init__.py         # Package version
│       ├── config.py           # Pydantic configuration loader
│       ├── logging.py          # Loguru logger setup
│       ├── main.py             # CLI entrypoint
│       └── services/
│           ├── __init__.py
│           └── example_service.py  # Example service class
├── tests/
│   └── test_example_service.py # pytest test examples
├── .env.example                # Environment variables template
├── .gitignore                  # Python gitignore defaults
├── LICENSE                     # MIT License
├── Makefile                    # Development automation
├── pyproject.toml              # Tool configuration
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## Development Workflow

### Code Quality Standards

This project enforces high code quality through multiple tools:

- **Black**: Code formatting for consistent style
- **isort**: Import statement organization
- **Ruff**: Fast Python linter for code quality
- **mypy**: Static type checking
- **pytest**: Unit testing framework

### Before Committing

Always run the following before committing code:

```bash
# Format code
make format

# Check linting
make lint

# Run tests
make test
```

### Configuration

Tool configurations are defined in `pyproject.toml`:
- Black formatting settings
- isort import organization
- Ruff linting rules
- mypy type checking options

## Continuous Integration

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that automatically:

- Sets up Python 3.11 environment
- Installs dependencies
- Runs linting with ruff and mypy
- Executes the test suite with pytest

All pull requests must pass CI checks before merging.

## Dependencies

### Core Dependencies
- `python-dotenv`: Environment variable management
- `loguru`: Structured logging
- `pydantic`: Data validation and settings
- `requests`: HTTP client library

### Development Dependencies
- `pytest`: Testing framework
- `black`: Code formatter
- `isort`: Import sorter
- `mypy`: Type checker
- `ruff`: Python linter

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Jean-Baptiste ASTRUZ

## Contributing

Contributions are welcome! Please ensure your code follows the project's coding standards and passes all tests before submitting a pull request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

---

**Happy coding! 🚀**
