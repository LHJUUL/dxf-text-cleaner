# Contributing to DXF Text Cleaner

First off, thanks for taking the time to contribute! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Sample DXF file** (if possible - anonymized if needed)
- **Python version** and OS
- **Full error message** (if applicable)

### Suggesting Features

Feature suggestions are welcome! Please:

- **Check existing issues** first
- **Describe the use case** clearly
- **Explain why** this feature would be useful
- Include **mockups/examples** if applicable

### Pull Requests

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly (include test DXF files if possible)
5. Commit with clear messages: `git commit -m 'Add support for MLEADER entities'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style

- Follow PEP 8 (Python style guide)
- Use descriptive variable names
- Comment complex logic
- Keep functions focused and small
- Add docstrings to new functions

### Testing

If adding new features, include:
- Test cases (if applicable)
- Sample DXF files that demonstrate the feature
- Expected output description

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/dxf-text-cleaner.git
cd dxf-text-cleaner

# Install dependencies
pip install -r requirements.txt

# Run tests (if you add them)
python -m pytest
```

## Questions?

Feel free to open an issue with the question label!

---

**Thanks for contributing! 🙏**
