"""
Unit tests for the UserManager class.

These tests can be run both before and after refactoring to ensure
that the functionality remains the same while improving the code structure.

Run with: python -m pytest test_user_manager.py -v
"""

import pytest
from user_manager import UserManager


class TestUserManager:
    """Test class for UserManager functionality."""
    
    def setup_method(self):
        """Set up a fresh UserManager instance for each test."""
        self.user_manager = UserManager()
    
    def test_create_user_success(self):
        """Test successful user creation."""
        user = self.user_manager.create_user("testuser", "test@example.com")
        
        assert user['username'] == "testuser"
        assert user['email'] == "test@example.com"
        assert user['is_active'] is True
        assert 'created_at' in user
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        with pytest.raises(ValueError, match="Invalid email format"):
            self.user_manager.create_user("testuser", "invalid-email")
    
    def test_create_user_duplicate_username(self):
        """Test creating user with existing username."""
        self.user_manager.create_user("testuser", "test@example.com")
        
        with pytest.raises(ValueError, match="User already exists"):
            self.user_manager.create_user("testuser", "test2@example.com")
    
    def test_get_user_success(self):
        """Test successful user retrieval."""
        # Create user first
        created_user = self.user_manager.create_user("testuser", "test@example.com")
        
        # Retrieve user
        retrieved_user = self.user_manager.get_user("testuser")
        
        assert retrieved_user is not None
        assert retrieved_user['username'] == "testuser"
        assert retrieved_user['email'] == "test@example.com"
    
    def test_get_user_not_found(self):
        """Test retrieving non-existent user."""
        user = self.user_manager.get_user("nonexistent")
        assert user is None
    
    def test_update_user_success(self):
        """Test successful user update."""
        # Create user first
        self.user_manager.create_user("testuser", "test@example.com")
        
        # Update user
        updated_user = self.user_manager.update_user("testuser", email="newemail@example.com")
        
        assert updated_user['email'] == "newemail@example.com"
        assert updated_user['username'] == "testuser"  # Should remain unchanged
    
    def test_update_user_invalid_email(self):
        """Test updating user with invalid email."""
        self.user_manager.create_user("testuser", "test@example.com")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            self.user_manager.update_user("testuser", email="invalid-email")
    
    def test_update_user_not_found(self):
        """Test updating non-existent user."""
        with pytest.raises(ValueError, match="User not found"):
            self.user_manager.update_user("nonexistent", email="test@example.com")
    
    def test_delete_user_success(self):
        """Test successful user deletion."""
        # Create user first
        self.user_manager.create_user("testuser", "test@example.com")
        assert self.user_manager.get_user("testuser") is not None
        
        # Delete user
        result = self.user_manager.delete_user("testuser")
        
        assert result is True
        assert self.user_manager.get_user("testuser") is None
    
    def test_delete_user_not_found(self):
        """Test deleting non-existent user."""
        with pytest.raises(ValueError, match="User not found"):
            self.user_manager.delete_user("nonexistent")
    
    def test_list_users(self):
        """Test listing all users."""
        # Initially empty
        users = self.user_manager.list_users()
        assert len(users) == 0
        
        # Create some users
        self.user_manager.create_user("user1", "user1@example.com")
        self.user_manager.create_user("user2", "user2@example.com")
        
        # List users
        users = self.user_manager.list_users()
        assert len(users) == 2
        usernames = [user['username'] for user in users]
        assert "user1" in usernames
        assert "user2" in usernames
    
    def test_email_validation_patterns(self):
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
                self.user_manager.create_user(f"user{i}", email)
            except ValueError:
                pytest.fail(f"Valid email {email} was rejected")
        
        # Test invalid emails
        for i, email in enumerate(invalid_emails):
            with pytest.raises(ValueError, match="Invalid email format"):
                self.user_manager.create_user(f"testuser{i}", email)
    
    def test_logging_functionality(self):
        """Test that operations are being logged."""
        # Perform some operations
        self.user_manager.create_user("testuser", "test@example.com")
        self.user_manager.get_user("testuser")
        self.user_manager.update_user("testuser", email="newemail@example.com")
        
        # Check logs
        logs = self.user_manager.get_logs()
        assert len(logs) > 0
        
        # Check log structure
        for log in logs:
            assert 'timestamp' in log
            assert 'message' in log
            assert isinstance(log['timestamp'], str)
            assert isinstance(log['message'], str)
    
    def test_user_workflow_integration(self):
        """Test a complete user workflow."""
        # Create user
        user = self.user_manager.create_user("workflow_user", "workflow@example.com")
        assert user['username'] == "workflow_user"
        
        # Verify user exists
        retrieved = self.user_manager.get_user("workflow_user")
        assert retrieved is not None
        
        # Update user
        updated = self.user_manager.update_user("workflow_user", email="updated@example.com")
        assert updated['email'] == "updated@example.com"
        
        # List users (should contain our user)
        users = self.user_manager.list_users()
        assert len(users) == 1
        assert users[0]['username'] == "workflow_user"
        
        # Delete user
        result = self.user_manager.delete_user("workflow_user")
        assert result is True
        
        # Verify user is gone
        deleted_user = self.user_manager.get_user("workflow_user")
        assert deleted_user is None
        
        # List should be empty
        users = self.user_manager.list_users()
        assert len(users) == 0


if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__, "-v"])
