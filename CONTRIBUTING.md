# Contributing to PiShock Universal App

Thank you for your interest in contributing to the PiShock Universal App! This document provides guidelines for contributing to the project.

## 🚀 **Getting Started**

### Prerequisites
- Python 3.7 or higher
- Git
- Basic understanding of Python and GUI development

### Setting Up Development Environment

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/PiShock.git
   cd PiShock
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   python pishock_app.py
   ```

## 🔧 **Development Guidelines**

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write clear, descriptive variable and function names
- Add docstrings to all functions and classes

### Testing
- Test all changes thoroughly
- Test with both PiShock and OpenShock platforms
- Verify safety features work correctly
- Test error handling scenarios

### Safety Considerations
- **Never remove safety features** without discussion
- Always test with low intensity settings first
- Ensure emergency stop functionality works
- Validate all user inputs

## 📝 **Types of Contributions**

### Bug Reports
- Use the GitHub issue template
- Include steps to reproduce
- Provide error messages and logs
- Specify platform and version

### Feature Requests
- Use the GitHub issue template
- Describe the use case
- Consider safety implications
- Discuss implementation approach

### Code Contributions
- Create a feature branch
- Make small, focused commits
- Write clear commit messages
- Update documentation as needed

## 🛠️ **Development Workflow**

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following style guidelines
   - Add tests if applicable
   - Update documentation

3. **Test your changes:**
   ```bash
   python pishock_app.py
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: Brief description of changes"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request:**
   - Use the PR template
   - Describe your changes
   - Link to related issues

## 🧪 **Testing Guidelines**

### Manual Testing
- Test with different platforms (PiShock, OpenShock)
- Test safety features (confirmation, cooldown, rate limiting)
- Test error handling (invalid credentials, network issues)
- Test UI responsiveness and usability

### Test Scenarios
1. **Platform Switching:**
   - Switch between platforms
   - Verify UI updates correctly
   - Test with different credentials

2. **Safety Features:**
   - Test confirmation dialogs
   - Test emergency stop
   - Test cooldown periods
   - Test rate limiting

3. **Error Handling:**
   - Invalid API keys
   - Network timeouts
   - Invalid input values
   - Platform-specific errors

## 📋 **Pull Request Guidelines**

### Before Submitting
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Safety features tested
- [ ] No breaking changes without discussion

### PR Description
- Clear title describing the change
- Detailed description of what was changed
- Screenshots if UI changes
- Testing instructions
- Any breaking changes noted

## 🐛 **Bug Report Template**

```markdown
**Bug Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior:**
What you expected to happen

**Actual Behavior:**
What actually happened

**Platform:**
- OS: [e.g., Windows 10, macOS, Linux]
- Python Version: [e.g., 3.9.0]
- App Version: [e.g., 1.0.0]

**Additional Context:**
Any other context about the problem
```

## 💡 **Feature Request Template**

```markdown
**Feature Description:**
Brief description of the feature

**Use Case:**
Why would this feature be useful?

**Proposed Solution:**
How should this feature work?

**Alternatives Considered:**
Other solutions you've considered

**Additional Context:**
Any other context about the feature request
```

## 🔒 **Security Considerations**

- Never commit API keys or sensitive data
- Use environment variables for sensitive configuration
- Validate all user inputs
- Follow secure coding practices
- Report security issues privately

## 📚 **Documentation**

- Update README.md for user-facing changes
- Update code comments for complex logic
- Add docstrings for new functions
- Update installation instructions if needed

## 🤝 **Community Guidelines**

- Be respectful and constructive
- Help others learn and grow
- Follow the code of conduct
- Focus on the code, not the person
- Be patient with newcomers

## 📞 **Getting Help**

- Check existing issues and discussions
- Ask questions in GitHub discussions
- Join the community chat (if available)
- Read the documentation thoroughly

## 🎯 **Areas for Contribution**

- **Platform Support:** Add support for new platforms
- **UI/UX:** Improve user interface and experience
- **Safety Features:** Enhance safety mechanisms
- **Documentation:** Improve documentation and examples
- **Testing:** Add automated tests
- **Performance:** Optimize app performance
- **Accessibility:** Improve accessibility features

## 📄 **License**

By contributing, you agree that your contributions will be licensed under the same license as the project (CC BY-NC 4.0).

---

Thank you for contributing to the PiShock Universal App! 🎉
