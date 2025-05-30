"""
Simple test runner for the UserManager class without pytest dependency.
This can be used if pytest is not available or has compatibility issues.

Run with: python simple_tests.py
"""

import sys
import traceback
from user_manager import UserManager


class SimpleTestRunner:
    """A simple test runner that doesn't require pytest."""
    
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results."""
        self.tests_run += 1
        print(f"Running {test_name}...", end=" ")
        
        try:
            test_func()
            print("✅ PASSED")
            self.tests_passed += 1
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            self.tests_failed += 1
            # Uncomment the next line to see full traceback
            # traceback.print_exc()
    
    def assert_equal(self, actual, expected, message=""):
        """Simple assertion helper."""
        if actual != expected:
            raise AssertionError(f"Expected {expected}, got {actual}. {message}")
    
    def assert_true(self, condition, message=""):
        """Assert that condition is True."""
        if not condition:
            raise AssertionError(f"Expected True, got False. {message}")
    
    def assert_false(self, condition, message=""):
        """Assert that condition is False."""
        if condition:
            raise AssertionError(f"Expected False, got True. {message}")
    
    def assert_raises(self, exception_type, func, *args, **kwargs):
        """Assert that function raises specific exception."""
        try:
            func(*args, **kwargs)
            raise AssertionError(f"Expected {exception_type.__name__} to be raised")
        except exception_type:
            pass  # Expected exception was raised
        except Exception as e:
            raise AssertionError(f"Expected {exception_type.__name__}, got {type(e).__name__}: {e}")
    
    def print_summary(self):
        """Print test results summary."""
        print("\n" + "="*50)
        print(f"Tests run: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        
        if self.tests_failed == 0:
            print("🎉 All tests passed!")
        else:
            print(f"😞 {self.tests_failed} test(s) failed")
        print("="*50)


def test_create_user_success():
    """Test successful user creation."""
    user_manager = UserManager()
    user = user_manager.create_user("testuser", "test@example.com", "Password123")
    
    runner.assert_equal(user['username'], "testuser")
    runner.assert_equal(user['email'], "test@example.com")
    runner.assert_true(user['is_active'])
    runner.assert_true('created_at' in user)
    runner.assert_true('password' in user)
    # Password should be encrypted (not plain text)
    runner.assert_true(user['password'] != "Password123")


def test_create_user_invalid_email():
    """Test user creation with invalid email."""
    user_manager = UserManager()
    runner.assert_raises(ValueError, user_manager.create_user, "testuser", "invalid-email", "Password123")


def test_create_user_weak_password():
    """Test user creation with weak password."""
    user_manager = UserManager()
    runner.assert_raises(ValueError, user_manager.create_user, "testuser", "test@example.com", "weak")


def test_create_user_duplicate():
    """Test creating user with existing username."""
    user_manager = UserManager()
    user_manager.create_user("testuser", "test@example.com", "Password123")
    runner.assert_raises(ValueError, user_manager.create_user, "testuser", "test2@example.com", "Password456")


def test_get_user_success():
    """Test successful user retrieval."""
    user_manager = UserManager()
    user_manager.create_user("testuser", "test@example.com", "Password123")
    
    retrieved_user = user_manager.get_user("testuser")
    runner.assert_true(retrieved_user is not None)
    runner.assert_equal(retrieved_user['username'], "testuser")
    runner.assert_equal(retrieved_user['email'], "test@example.com")


def test_get_user_not_found():
    """Test retrieving non-existent user."""
    user_manager = UserManager()
    user = user_manager.get_user("nonexistent")
    runner.assert_true(user is None)


def test_update_user_success():
    """Test successful user update."""
    user_manager = UserManager()
    user_manager.create_user("testuser", "test@example.com", "Password123")
    
    updated_user = user_manager.update_user("testuser", email="newemail@example.com")
    runner.assert_equal(updated_user['email'], "newemail@example.com")
    runner.assert_equal(updated_user['username'], "testuser")


def test_update_user_invalid_email():
    """Test updating user with invalid email."""
    user_manager = UserManager()
    user_manager.create_user("testuser", "test@example.com", "Password123")
    runner.assert_raises(ValueError, user_manager.update_user, "testuser", email="invalid-email")


def test_delete_user_success():
    """Test successful user deletion."""
    user_manager = UserManager()
    user_manager.create_user("testuser", "test@example.com", "Password123")
    runner.assert_true(user_manager.get_user("testuser") is not None)
    
    result = user_manager.delete_user("testuser")
    runner.assert_true(result)
    runner.assert_true(user_manager.get_user("testuser") is None)


def test_delete_user_not_found():
    """Test deleting non-existent user."""
    user_manager = UserManager()
    runner.assert_raises(ValueError, user_manager.delete_user, "nonexistent")


def test_list_users():
    """Test listing all users."""
    user_manager = UserManager()
    
    # Initially empty
    users = user_manager.list_users()
    runner.assert_equal(len(users), 0)
    
    # Create some users
    user_manager.create_user("user1", "user1@example.com", "Password123")
    user_manager.create_user("user2", "user2@example.com", "Password456")
    
    # List users
    users = user_manager.list_users()
    runner.assert_equal(len(users), 2)
    usernames = [user['username'] for user in users]
    runner.assert_true("user1" in usernames)
    runner.assert_true("user2" in usernames)


def test_password_encryption():
    """Test that passwords are properly encrypted."""
    user_manager = UserManager()
    password = "TestPassword123"
    user = user_manager.create_user("testuser", "test@example.com", password)
    
    # Password should not be stored in plain text
    runner.assert_true(user['password'] != password)
    # Should be a hash (64 characters for SHA-256)
    runner.assert_equal(len(user['password']), 64)


def test_logging_functionality():
    """Test that operations are being logged."""
    user_manager = UserManager()
    
    # Perform some operations
    user_manager.create_user("testuser", "test@example.com", "Password123")
    user_manager.get_user("testuser")
    user_manager.update_user("testuser", email="newemail@example.com")
    
    # Check logs
    logs = user_manager.get_logs()
    runner.assert_true(len(logs) > 0)
    
    # Check log structure
    for log in logs:
        runner.assert_true('timestamp' in log)
        runner.assert_true('message' in log)


def test_email_validation_patterns():
    """Test various email validation patterns."""
    user_manager = UserManager()
    
    valid_emails = [
        "user@example.com",
        "user.name@example.com",
        "user+tag@example.co.uk"
    ]
    
    invalid_emails = [
        "invalid-email",
        "@example.com",
        "user@",
        "user@.com"
    ]
    
    # Test valid emails
    for i, email in enumerate(valid_emails):
        try:
            user_manager.create_user(f"user{i}", email, "Password123")
        except ValueError:
            raise AssertionError(f"Valid email {email} was rejected")
    
    # Test invalid emails - create new user_manager for each test
    for email in invalid_emails:
        user_manager_test = UserManager()
        runner.assert_raises(ValueError, user_manager_test.create_user, "testuser", email, "Password123")


def test_user_workflow_integration():
    """Test a complete user workflow."""
    user_manager = UserManager()
    
    # Create user
    user = user_manager.create_user("workflow_user", "workflow@example.com", "TestPass123")
    runner.assert_equal(user['username'], "workflow_user")
    
    # Verify user exists
    retrieved = user_manager.get_user("workflow_user")
    runner.assert_true(retrieved is not None)
    
    # Update user
    updated = user_manager.update_user("workflow_user", email="updated@example.com")
    runner.assert_equal(updated['email'], "updated@example.com")
    
    # List users (should contain our user)
    users = user_manager.list_users()
    runner.assert_equal(len(users), 1)
    runner.assert_equal(users[0]['username'], "workflow_user")
    
    # Delete user
    result = user_manager.delete_user("workflow_user")
    runner.assert_true(result)
    
    # Verify user is gone
    deleted_user = user_manager.get_user("workflow_user")
    runner.assert_true(deleted_user is None)
    
    # List should be empty
    users = user_manager.list_users()
    runner.assert_equal(len(users), 0)


# Global runner instance
runner = SimpleTestRunner()


if __name__ == "__main__":
    print("Running UserManager Tests")
    print("="*50)
    
    # Run all tests
    runner.run_test("test_create_user_success", test_create_user_success)
    runner.run_test("test_create_user_invalid_email", test_create_user_invalid_email)
    runner.run_test("test_create_user_weak_password", test_create_user_weak_password)
    runner.run_test("test_create_user_duplicate", test_create_user_duplicate)
    runner.run_test("test_get_user_success", test_get_user_success)
    runner.run_test("test_get_user_not_found", test_get_user_not_found)
    runner.run_test("test_update_user_success", test_update_user_success)
    runner.run_test("test_update_user_invalid_email", test_update_user_invalid_email)
    runner.run_test("test_delete_user_success", test_delete_user_success)
    runner.run_test("test_delete_user_not_found", test_delete_user_not_found)
    runner.run_test("test_list_users", test_list_users)
    runner.run_test("test_password_encryption", test_password_encryption)
    runner.run_test("test_logging_functionality", test_logging_functionality)
    runner.run_test("test_email_validation_patterns", test_email_validation_patterns)
    runner.run_test("test_user_workflow_integration", test_user_workflow_integration)
    
    # Print summary
    runner.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if runner.tests_failed == 0 else 1)
