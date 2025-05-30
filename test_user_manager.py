"""
Unit tests for both the original UserManager class and the refactored UserService.

These tests can be run both before and after refactoring to ensure
that the functionality remains the same while improving the code structure.

Run with: python -m pytest test_user_manager.py -v
"""

import pytest
from user_manager import UserManager

# Import the refactored components
try:
    from refactored_partial import create_user_service
    REFACTORED_AVAILABLE = True
except ImportError:
    REFACTORED_AVAILABLE = False


def get_implementations():
    """Get available implementations to test."""
    implementations = [("original", lambda: UserManager())]
    
    if REFACTORED_AVAILABLE:
        implementations.append(("refactored", lambda: create_user_service()))
    
    return implementations


class TestUserManager:
    """Test class for UserManager functionality."""
    
    @pytest.fixture(params=get_implementations(), ids=lambda x: x[0])
    def user_service(self, request):
        """Fixture that provides both original and refactored implementations."""
        _, factory = request.param
        return factory()
    
    def test_create_user_success(self, user_service):
        """Test successful user creation."""
        user = user_service.create_user("testuser", "test@example.com")
        
        assert user['username'] == "testuser"
        assert user['email'] == "test@example.com"
        assert user['is_active'] is True
        assert 'created_at' in user
    
    def test_create_user_invalid_email(self, user_service):
        """Test user creation with invalid email."""
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.create_user("testuser", "invalid-email")
    
    def test_create_user_duplicate_username(self, user_service):
        """Test creating user with existing username."""
        user_service.create_user("testuser", "test@example.com")
        
        with pytest.raises(ValueError, match="User already exists"):
            user_service.create_user("testuser", "test2@example.com")
    
    def test_get_user_success(self, user_service):
        """Test successful user retrieval."""
        # Create user first
        created_user = user_service.create_user("testuser", "test@example.com")
        
        # Retrieve user
        retrieved_user = user_service.get_user("testuser")
        
        assert retrieved_user is not None
        assert retrieved_user['username'] == "testuser"
        assert retrieved_user['email'] == "test@example.com"
    
    def test_get_user_not_found(self, user_service):
        """Test retrieving non-existent user."""
        user = user_service.get_user("nonexistent")
        assert user is None
    
    def test_update_user_success(self, user_service):
        """Test successful user update."""
        # Create user first
        user_service.create_user("testuser", "test@example.com")
        
        # Update user
        updated_user = user_service.update_user("testuser", email="newemail@example.com")
        
        assert updated_user['email'] == "newemail@example.com"
        assert updated_user['username'] == "testuser"  # Should remain unchanged
    
    def test_update_user_invalid_email(self, user_service):
        """Test updating user with invalid email."""
        user_service.create_user("testuser", "test@example.com")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            user_service.update_user("testuser", email="invalid-email")
    
    def test_update_user_not_found(self, user_service):
        """Test updating non-existent user."""
        with pytest.raises(ValueError, match="User not found"):
            user_service.update_user("nonexistent", email="test@example.com")
    
    def test_delete_user_success(self, user_service):
        """Test successful user deletion."""
        # Create user first
        user_service.create_user("testuser", "test@example.com")
        assert user_service.get_user("testuser") is not None
        
        # Delete user
        result = user_service.delete_user("testuser")
        
        assert result is True
        assert user_service.get_user("testuser") is None
    
    def test_delete_user_not_found(self, user_service):
        """Test deleting non-existent user."""
        with pytest.raises(ValueError, match="User not found"):
            user_service.delete_user("nonexistent")
    
    def test_list_users(self, user_service):
        """Test listing all users."""
        # Initially empty
        users = user_service.list_users()
        assert len(users) == 0
        
        # Create some users
        user_service.create_user("user1", "user1@example.com")
        user_service.create_user("user2", "user2@example.com")
        
        # List users
        users = user_service.list_users()
        assert len(users) == 2
        usernames = [user['username'] for user in users]
        assert "user1" in usernames
        assert "user2" in usernames
    
    def test_email_validation_patterns(self, user_service):
        """Test various email validation patterns."""
        valid_emails = [
            "user@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user123@test-domain.com"
        ]
        
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "user@",
            "user@.com",
            "user..name@example.com",
            ""
        ]
        
        # Test valid emails
        for i, email in enumerate(valid_emails):
            try:
                user_service.create_user(f"user{i}", email)
            except ValueError:
                pytest.fail(f"Valid email {email} was rejected")
        
        # Test invalid emails
        for i, email in enumerate(invalid_emails):
            with pytest.raises(ValueError, match="Invalid email format"):
                user_service.create_user(f"testuser{i}", email)
    
    def test_logging_functionality(self, user_service):
        """Test that operations are being logged."""
        # Perform some operations
        user_service.create_user("testuser", "test@example.com")
        user_service.get_user("testuser")
        user_service.update_user("testuser", email="newemail@example.com")
        
        # Check logs
        logs = user_service.get_logs()
        assert len(logs) > 0
        
        # Check log structure
        for log in logs:
            assert 'timestamp' in log
            assert 'message' in log
            assert isinstance(log['timestamp'], str)
            assert isinstance(log['message'], str)
    
    def test_user_workflow_integration(self, user_service):
        """Test a complete user workflow."""
        # Create user
        user = user_service.create_user("workflow_user", "workflow@example.com")
        assert user['username'] == "workflow_user"
        
        # Verify user exists
        retrieved = user_service.get_user("workflow_user")
        assert retrieved is not None
        
        # Update user
        updated = user_service.update_user("workflow_user", email="updated@example.com")
        assert updated['email'] == "updated@example.com"
        
        # List users (should contain our user)
        users = user_service.list_users()
        assert len(users) == 1
        assert users[0]['username'] == "workflow_user"
        
        # Delete user
        result = user_service.delete_user("workflow_user")
        assert result is True
        
        # Verify user is gone
        deleted_user = user_service.get_user("workflow_user")
        assert deleted_user is None
        
        # List should be empty
        users = user_service.list_users()
        assert len(users) == 0

if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])
