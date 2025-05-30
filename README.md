# Upskilling: Single Responsibility Principle (SRP) Exercise

Welcome to the hands-on exercise for learning the Single Responsibility Principle (SRP) - the first principle of SOLID design principles. This repository contains a practical Python example that violates SRP, along with comprehensive unit tests to help you understand and practice refactoring code to follow SRP.

## 🎯 Learning Objectives

By the end of this exercise, you will:
- ✅ Understand what SRP means and why it matters
- ✅ Identify multiple responsibilities in a single class
- ✅ Refactor code to follow SRP principles
- ✅ See the immediate benefits of cleaner, more modular code
- ✅ Experience how proper SRP makes testing easier

## 📋 Prerequisites

Before starting this exercise, ensure you have:

### Required Software
- **Git** - For cloning the repository
- **Python 3.9 or higher** - The programming language for this exercise
- **Code Editor** - We recommend VS Code, but any editor works
- **Terminal/Command Prompt** - For running commands

### Knowledge Prerequisites
- Basic Python programming knowledge
- Understanding of classes and object-oriented programming
- Familiarity with running Python scripts and tests


## 🚀 Getting Started

### Step 1: Download the Code

Clone this repository to your local machine:

```bash
# Clone the repository (replace YOUR_REPOSITORY_URL with the actual URL)
git clone YOUR_REPOSITORY_URL
cd srp-exercise
```

### Step 2: Set Up Python Environment

#### For macOS Users:

1. **Check if Python 3.9+ is installed:**
   ```bash
   python3 --version
   ```
   If Python 3.9+ is not installed, install it using Homebrew:
   ```bash
   # Install Homebrew if you don't have it
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install Python
   brew install python@3.9
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

#### For Windows Users:

1. **Install Python 3.9+:**
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - Verify installation by opening Command Prompt and running:
     ```cmd
     python --version
     ```

2. **Create a virtual environment (recommended):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

### Step 3: Verify Your Setup

Run the example code to make sure everything works:

```bash
# Run the example (shows SRP violations in action)
python user_manager.py

# Run the unit tests (all should pass)
python -m pytest test_user_manager.py -v
```

If you see the example output and all tests pass, you're ready to start! 🎉

## 📚 Understanding the Exercise

### The Problem: SRP Violations

The `UserManager` class in `user_manager.py` violates the Single Responsibility Principle because it handles multiple responsibilities:

1. **User Data Management** - CRUD operations for users
2. **Email Validation** - Checking if emails are properly formatted
3. **Password Validation** - Ensuring passwords meet security requirements
4. **Password Encryption** - Hashing passwords for security
5. **Email Sending** - Sending welcome/goodbye emails
6. **Logging** - Recording system events
7. **File Operations** - Exporting user data to JSON

### Why This Is a Problem

- **Hard to maintain** - Changes to one responsibility might break others
- **Difficult to test** - Testing one feature requires setting up all features
- **Poor reusability** - Can't reuse validation logic without the entire class
- **Violates separation of concerns** - Multiple reasons for the class to change

### The Solution: Apply SRP

Your task is to refactor this code into multiple classes, each with a single responsibility:

- `User` - Represents user data
- `UserRepository` - Handles user data storage/retrieval
- `EmailValidator` - Validates email formats
- `PasswordValidator` - Validates password strength
- `PasswordEncryption` - Handles password hashing
- `EmailService` - Sends emails
- `Logger` - Handles logging
- `UserService` - Orchestrates user operations

## 🧪 Running Tests

The repository includes comprehensive unit tests that work both before and after refactoring:

### Option 1: Using pytest (recommended)
```bash
# Run all tests with verbose output
python -m pytest test_user_manager.py -v

# Run tests with coverage report
python -m pytest test_user_manager.py --cov=user_manager --cov-report=html

# Run specific test
python -m pytest test_user_manager.py::TestUserManager::test_create_user_success -v
```

### Option 2: Using simple test runner (if pytest has issues)
```bash
# Run all tests with simple runner
python simple_tests.py
```

**Note:** If you encounter pytest compatibility issues, use the simple test runner. Both test suites cover the same functionality and ensure your code works correctly.

### Test Categories

The tests cover:

- ✅ User creation with valid/invalid data
- ✅ User retrieval and updates
- ✅ User deletion
- ✅ Email validation patterns
- ✅ Password validation patterns
- ✅ Password encryption
- ✅ Logging functionality
- ✅ Data export features
- ✅ Complete workflow integration

## 🎯 Exercise Instructions

### Phase 1: Analyze the Current Code (15 minutes)

1. **Read through `user_manager.py`** - Identify all the different responsibilities
2. **Run the code** - See how it works: `python user_manager.py`
3. **Run the tests** - Understand what functionality needs to be preserved
4. **List the violations** - Write down each responsibility you identify

### Phase 2: Plan Your Refactoring (10 minutes)

1. **Design new classes** - Decide what classes you'll create
2. **Define interfaces** - Think about how classes will interact
3. **Plan migration** - Decide the order of refactoring

### Phase 3: Refactor the Code (45 minutes)

1. **Create individual classes** - Start with the simplest responsibilities
2. **Update the main class** - Make it use the new specialized classes
3. **Run tests frequently** - Ensure functionality is preserved
4. **Refine and improve** - Clean up code and improve design

### Phase 4: Reflection (15 minutes)

1. **Compare before/after** - What improved?
2. **Run tests again** - Verify everything still works
3. **Discuss benefits** - What's easier now?

## 📁 Repository Structure

```text
srp-exercise/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── user_manager.py          # Original code with SRP violations
├── test_user_manager.py     # Comprehensive unit tests (pytest)
├── simple_tests.py          # Simple test runner (alternative to pytest)
├── refactored_example.py    # Reference solution (don't peek!)
├── .gitignore              # Git ignore file
└── refactored/             # (You'll create this during the exercise)
    ├── models/
    ├── services/
    ├── validators/
    └── ...
```

## 💡 Tips for Success

1. **Start small** - Refactor one responsibility at a time
2. **Run tests often** - After each change, verify tests still pass
3. **Keep the interface** - Don't change how external code uses your classes
4. **Use dependency injection** - Make classes depend on abstractions, not concrete implementations
5. **Think about testability** - Each class should be easy to test in isolation

## 🔧 Troubleshooting

### Common Issues

**Tests failing after refactoring?**
- Check that you didn't change the public interface
- Ensure all functionality is preserved
- Verify import statements are correct

**Import errors?**
- Make sure your virtual environment is activated
- Check that all required files are in the correct locations
- Verify Python path is set correctly

**Python version issues?**
- Ensure you're using Python 3.9 or higher
- Consider using pyenv to manage multiple Python versions

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Verify your environment setup
3. Review the original working code
4. Ask for help during the session!

## 🎉 Expected Outcomes

After completing this exercise, you should have:

- ✅ **Cleaner code** - Each class has a single, clear responsibility
- ✅ **Better testability** - Individual components can be tested in isolation
- ✅ **Improved maintainability** - Changes to one feature don't affect others
- ✅ **Enhanced reusability** - Validators and services can be reused elsewhere
- ✅ **Deeper understanding** - Concrete experience with SRP benefits

## 🌟 Next Steps

Want to continue learning? Try these challenges:

1. **Add new features** - See how easy it is with proper SRP
2. **Write more tests** - Test individual classes in isolation
3. **Apply other SOLID principles** - Open/Closed, Liskov Substitution, etc.
4. **Refactor your own code** - Apply SRP to your current projects

## 📖 Additional Resources

- [SOLID Principles Explained](https://en.wikipedia.org/wiki/SOLID)
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)
- [Effective Python by Brett Slatkin](https://effectivepython.com/)

---

**Happy coding! 🚀** Remember: The goal isn't perfect code, but better code. Every small improvement in following SRP makes your software more maintainable and testable.
