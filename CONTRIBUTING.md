# Contributing to Forensic Cyber Tech Cloud Messenger

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/YOUR_USERNAME/forensic-messenger/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear use case
   - Proposed solution
   - Alternative solutions considered
   - Impact on existing functionality

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/forensic-messenger.git
   cd forensic-messenger
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest tests/ -v

   # Frontend build
   cd frontend
   npm run build
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Code style changes (formatting)
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Ensure CI/CD passes

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker Development

```bash
docker-compose up -d
```

## Code Style

### Python (Backend)
- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for functions and classes

### TypeScript (Frontend)
- Follow [TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html)
- Use functional components with hooks
- Prefer const over let
- Use meaningful variable names

## Testing

- Write unit tests for new features
- Maintain or improve code coverage
- Test edge cases and error handling
- Backend: pytest
- Frontend: Jest/Vitest (when configured)

## Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add comments for complex logic
- Update WEBSOCKET.md for event changes

## Review Process

1. Maintainers will review your PR
2. Address feedback and requested changes
3. Once approved, PR will be merged
4. Your contribution will be credited

## Questions?

- Open a [Discussion](https://github.com/YOUR_USERNAME/forensic-messenger/discussions)
- Join our community chat (if available)
- Email: support@forensiccybertech.com (if configured)

Thank you for contributing! 🎉
