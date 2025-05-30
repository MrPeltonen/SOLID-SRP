# Upskilling: Single Responsibility Principle (SRP) Exercise

Welcome to the hands-on exercise for learning the Single Responsibility Principle (SRP) - the first principle of SOLID design principles. This repository contains a practical Python example that violates SRP, along with comprehensive unit tests to help you understand and practice refactoring code to follow SRP.

**⏱️ Estimated Duration: 1 hour**

## 🎯 Learning Objectives

By the end of this exercise, you will:
- ✅ Understand what SRP means and why it matters
- ✅ Identify multiple responsibilities in a single class
- ✅ Refactor code to follow SRP principles
- ✅ See the immediate benefits of cleaner, more modular code

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
# Clone the repository
git clone git@github.com:MrPeltonen/SOLID-SRP.git
cd SOLID-SRP
```

### Step 2: Set Up Python Environment

#### For macOS Users:

1. **Check if Python 3.9+ is installed:**
   ```bash
   python3 --version
   ```
   If Python 3.9+ is not installed, install it using Homebrew:
   ```bash
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
# Run the unit tests
python -m pytest test_user_manager.py -v
```

**Expected Results:** You should see 16 tests pass and 12 tests fail. The failing tests are for the refactored implementation (which you'll complete during the exercise). The passing tests are for the original implementation, confirming your setup works correctly.

If you see this mix of passing and failing tests, you're ready to start! 🎉

## 📚 Understanding the Exercise

### The Problem: SRP Violations

This UserManager class has multiple responsibilities:
1. User data management (CRUD operations)
2. Email validation

This violates SRP because the class has multiple reasons to change:
- Changes in user data structure
- Changes in email validation rules

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
- `UserService` - Orchestrates user operations

**Note:** A partial template solution is available in `refactored_partial.py` to help guide your refactoring. This template provides the class structure and method signatures, but you'll need to complete the implementation marked with TODO comments.

## 🧪 Running Tests

The repository includes comprehensive unit tests that work both before and after refactoring. The test file (`test_user_manager.py`) is designed to automatically test both the original `UserManager` class and the refactored solution when available.

**Important:** Until you complete the implementation in `refactored_partial.py`, some tests will fail for the refactored version. This is expected and part of the exercise - your goal is to make all tests pass for both implementations.

### Using pytest (recommended)
```bash
# Run all tests with verbose output
python -m pytest test_user_manager.py -v

# Run tests with coverage report
python -m pytest test_user_manager.py --cov=user_manager --cov-report=html

# Run specific test
python -m pytest test_user_manager.py::TestUserManager::test_create_user_success -v
```

### How the Tests Work

The tests use a smart fixture that automatically detects and tests both implementations:
- **Original Implementation**: Tests the `UserManager` class from `user_manager.py`
- **Refactored Implementation**: Tests the refactored solution from `refactored_partial.py` (when available)

This ensures that both versions maintain identical functionality!

### Test Categories

The tests cover:

- ✅ User creation with valid/invalid data
- ✅ User retrieval and updates
- ✅ User deletion
- ✅ Email validation patterns
- ✅ Logging functionality
- ✅ Complete workflow integration

### Understanding Test Failures

When you first run the tests with the incomplete `refactored_partial.py`, you'll see failures like:
- `TypeError: 'NoneType' object is not subscriptable` - Methods returning `None` instead of expected data
- `Failed: DID NOT RAISE <class 'ValueError'>` - Validation logic not implemented
- `assert 0 > 0` - Empty logs because logging isn't implemented

This is expected! As you implement each TODO section, more tests will pass.

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

1. **Complete the template** - Use `refactored_partial.py` as your starting point
2. **Implement TODO sections** - Fill in the missing functionality marked with TODO comments
3. **Run tests frequently** - After each implementation, verify tests pass
4. **Refine and improve** - Clean up code and improve design

**Note**: The template in `refactored_partial.py` provides the class structure and method signatures to help guide your refactoring, but you'll need to complete the implementation marked with TODO comments.

**Recommended Implementation Order:**
1. Start with `User.to_dict()` method (simplest)
2. Implement `EmailValidator.is_valid()` 
3. Complete `Logger.log()` method
4. Implement `UserRepository` methods (`save`, `find_by_username`, `delete`)
5. Complete `User.update()` method
6. Finally, implement `UserService` methods (`create_user`, `get_user`, `update_user`)

### Phase 4: Reflection (15 minutes)

1. **Compare before/after** - What improved?
2. **Run tests again** - Verify everything still works
3. **Discuss benefits** - What's easier now?

## 📁 Repository Structure

```text
SOLID-SRP/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── user_manager.py          # Original code with SRP violations
├── test_user_manager.py     # Comprehensive unit tests (pytest)
├── refactored_partial.py    # Partial template solution (complete the TODOs)
├── users_backup.json       # Backup data file (generated during testing)
├── .gitignore              # Git ignore file
├── venv/                   # Virtual environment (created after setup)
└── __pycache__/            # Python cache files (generated)
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
