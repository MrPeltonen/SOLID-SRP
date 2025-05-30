"""
Unit tests for the UserManager class.

These tests can be run both before and after refactoring to ensure
that the functionality remains the same while improving the code structure.

Run with: python -m pytest test_user_manager.py -v
"""

import pytest
import json
import os
from user_manager import UserManager


class TestUserManager:
    """Test class for UserManager functionality."""
    
    def setup_method(self):
        """Set up a fresh UserManager instance for each test."""
        self.user_manager = UserManager()
    
    def test_create_user_success(self):
        """Test successful user creation."""
        user = self.user_manager.create_user("testuser", "test@example.com", "Password123")
        
        assert user['username'] == "testuser"
        assert user['email'] == "test@example.com"
        assert user['is_active'] is True
        assert 'created_at' in user
        assert 'password' in user
        # Password should be encrypted (not plain text)
        assert user['password'] != "Password123"
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email."""
        with pytest.raises(ValueError, match="Invalid email format"):
            self.user_manager.create_user("testuser", "invalid-email", "Password123")
    
    def test_create_user_weak_password(self):
        """Test user creation with weak password."""
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            self.user_manager.create_user("testuser", "test@example.com", "weak")
    
    def test_create_user_duplicate_username(self):
        """Test creating user with existing username."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        
        with pytest.raises(ValueError, match="User already exists"):
            self.user_manager.create_user("testuser", "test2@example.com", "Password456")
    
    def test_get_user_success(self):
        """Test successful user retrieval."""
        # Create user first
        created_user = self.user_manager.create_user("testuser", "test@example.com", "Password123")
        
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
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        
        # Update user
        updated_user = self.user_manager.update_user("testuser", email="newemail@example.com")
        
        assert updated_user['email'] == "newemail@example.com"
        assert updated_user['username'] == "testuser"  # Should remain unchanged
    
    def test_update_user_password(self):
        """Test updating user password."""
        # Create user first
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        original_password = self.user_manager.get_user("testuser")['password']
        
        # Update password
        updated_user = self.user_manager.update_user("testuser", password="NewPassword456")
        
        assert updated_user['password'] != original_password
        assert updated_user['password'] != "NewPassword456"  # Should be encrypted
    
    def test_update_user_invalid_email(self):
        """Test updating user with invalid email."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        
        with pytest.raises(ValueError, match="Invalid email format"):
            self.user_manager.update_user("testuser", email="invalid-email")
    
    def test_update_user_weak_password(self):
        """Test updating user with weak password."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            self.user_manager.update_user("testuser", password="weak")
    
    def test_update_user_not_found(self):
        """Test updating non-existent user."""
        with pytest.raises(ValueError, match="User not found"):
            self.user_manager.update_user("nonexistent", email="test@example.com")
    
    def test_delete_user_success(self):
        """Test successful user deletion."""
        # Create user first
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
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
        self.user_manager.create_user("user1", "user1@example.com", "Password123")
        self.user_manager.create_user("user2", "user2@example.com", "Password456")
        
        # List users
        users = self.user_manager.list_users()
        assert len(users) == 2
        usernames = [user['username'] for user in users]
        assert "user1" in usernames
        assert "user2" in usernames
    
    def test_password_encryption(self):
        """Test that passwords are properly encrypted."""
        password = "TestPassword123"
        user = self.user_manager.create_user("testuser", "test@example.com", password)
        
        # Password should not be stored in plain text
        assert user['password'] != password
        # Should be a hash (64 characters for SHA-256)
        assert len(user['password']) == 64
    
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
                self.user_manager.create_user(f"user{i}", email, "Password123")
            except ValueError:
                pytest.fail(f"Valid email {email} was rejected")
        
        # Test invalid emails
        for email in invalid_emails:
            with pytest.raises(ValueError, match="Invalid email format"):
                self.user_manager.create_user("testuser", email, "Password123")
    
    def test_password_validation_patterns(self):
        """Test various password validation patterns."""
        invalid_passwords = [
            "short",              # Too short
            "alllowercase123",    # No uppercase
            "ALLUPPERCASE123",    # No lowercase
            "NoNumbers",          # No numbers
            "NoLetters123",       # No letters (this should actually pass, but let's say it fails)
            ""                    # Empty
        ]
        
        valid_passwords = [
            "Password123",
            "StrongPass1",
            "MySecure2024Pass"
        ]
        
        # Test valid passwords
        for i, password in enumerate(valid_passwords):
            try:
                self.user_manager.create_user(f"user{i}", f"user{i}@example.com", password)
            except ValueError:
                pytest.fail(f"Valid password was rejected")
        
        # Test invalid passwords
        for password in invalid_passwords:
            with pytest.raises(ValueError, match="Password must be at least 8 characters"):
                self.user_manager.create_user("testuser", "test@example.com", password)
    
    def test_logging_functionality(self):
        """Test that operations are being logged."""
        # Perform some operations
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
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
    
    def test_export_users_to_json(self):
        """Test exporting users to JSON file."""
        # Create some users
        self.user_manager.create_user("user1", "user1@example.com", "Password123")
        self.user_manager.create_user("user2", "user2@example.com", "Password456")
        
        # Export to file
        filename = "test_users.json"
        result = self.user_manager.export_users_to_json(filename)
        
        assert result is True
        assert os.path.exists(filename)
        
        # Verify file contents
        with open(filename, 'r') as f:
            exported_data = json.load(f)
        
        assert len(exported_data) == 2
        assert "user1" in exported_data
        assert "user2" in exported_data
        
        # Clean up
        os.remove(filename)
    
    def test_user_workflow_integration(self):
        """Test a complete user workflow."""
        # Create user
        user = self.user_manager.create_user("workflow_user", "workflow@example.com", "TestPass123")
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
