"""
This file provides a partial template for how the refactored code should look after applying SRP.
This is a starting template to help guide your refactoring exercise.

EXERCISE: Complete the missing implementations marked with TODO comments.
Estimated time: 40 minutes

The original UserManager class has multiple responsibilities:
1. User data management (CRUD operations)
2. Email validation
3. Logging operations

This violates SRP because the class has multiple reasons to change:
- Changes in user data structure
- Changes in email validation rules
- Changes in logging requirements

Your task: Complete the TODO sections to make this a fully working SRP-compliant solution.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re


# ========================
# 1. User Model (Data)
# ========================
class User:
    """Represents a user entity - Single responsibility: Hold user data."""
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
        self.created_at = datetime.now().isoformat()
        self.is_active = True
    
    def to_dict(self):
        """Convert user to dictionary representation."""
        # TODO: Implement method to return user data as dictionary
        # Should return: {'username': ..., 'email': ..., 'created_at': ..., 'is_active': ...}
        pass
    
    def update(self, **kwargs):
        """Update user attributes."""
        # TODO: Implement method to update user attributes
        # Hint: Use setattr() and hasattr() to update only valid attributes
        pass


# ========================
# 2. Validation Services
# ========================
class EmailValidator:
    """Single responsibility: Validate email formats."""
    
    @staticmethod
    def is_valid(email: str) -> bool:
        """Check if email format is valid."""
        # TODO: Implement email validation logic
        # Requirements:
        # - Use regex pattern to validate email format
        # - Pattern should be: r'^[a-zA-Z0-9][a-zA-Z0-9._+%-]*[a-zA-Z0-9]@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
        # - Check for consecutive dots (..) which should not be allowed
        # - Return True if valid, False otherwise
        pass


# ========================
# 3. Logging Service
# ========================
class Logger:
    """Single responsibility: Handle logging operations."""
    
    def __init__(self):
        self.log_entries = []
    
    def log(self, message: str):
        """Add a log entry."""
        # TODO: Implement logging functionality
        # Create a log entry with timestamp and message
        # Format: {'timestamp': datetime.now().isoformat(), 'message': message}
        # Add to self.log_entries list
        pass
    
    def get_logs(self):
        """Retrieve all log entries."""
        return self.log_entries


# ========================
# 4. Data Storage Service
# ========================
class UserRepository:
    """Single responsibility: Handle user data persistence."""
    
    def __init__(self):
        self.users = {}
    
    def save(self, user: User):
        """Save user to storage."""
        # TODO: Implement save functionality
        # Store the user in self.users dictionary using username as key
        pass
    
    def find_by_username(self, username: str):
        """Find user by username."""
        # TODO: Implement user lookup
        # Return the user object if found, None if not found
        pass
    
    def delete(self, username: str):
        """Delete user from storage."""
        # TODO: Implement user deletion
        # Remove user from self.users if exists
        # Return True if deleted, False if user didn't exist
        pass
    
    def find_all(self):
        """Get all users."""
        return list(self.users.values())
    
    def exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self.users


# ========================
# 4. Main Service (Orchestrator)
# ========================
class UserService:
    """
    Single responsibility: Orchestrate user operations.
    This class coordinates between other services but doesn't contain business logic for validation, etc.
    """
    
    def __init__(self, 
                 user_repository: UserRepository,
                 email_validator: EmailValidator,
                 logger: Logger):
        
        self.user_repository = user_repository
        self.email_validator = email_validator
        self.logger = logger
    
    def create_user(self, username: str, email: str):
        """Create a new user with validation."""
        # TODO: Implement user creation logic
        # Steps:
        # 1. Validate email using self.email_validator.is_valid()
        # 2. Check if user already exists using self.user_repository.exists()
        # 3. Create new User object
        # 4. Save user using self.user_repository.save()
        # 5. Log success message
        # 6. Return user.to_dict()
        # Remember to handle validation failures with proper logging and exceptions
        pass
    
    def get_user(self, username: str):
        """Retrieve user data."""
        # TODO: Implement user retrieval
        # 1. Find user using self.user_repository.find_by_username()
        # 2. Log appropriate message (success or failure)
        # 3. Return user.to_dict() if found, None if not found
        pass
    
    def update_user(self, username: str, **kwargs):
        """Update user data with validation."""
        # TODO: Implement user update logic
        # 1. Find user using repository
        # 2. If email is being updated, validate it
        # 3. Update user object
        # 4. Save updated user
        # 5. Log success
        # 6. Return updated user.to_dict()
        # Handle cases where user not found or email validation fails
        pass
    
    def delete_user(self, username: str):
        """Delete a user."""
        user = self.user_repository.find_by_username(username)
        if user is None:
            self.logger.log(f"Failed to delete user {username}: User not found")
            raise ValueError("User not found")
        
        # Delete user
        self.user_repository.delete(username)
        self.logger.log(f"User {username} deleted successfully")
        
        return True
    
    def list_users(self):
        """List all users."""
        self.logger.log("User list retrieved")
        users = self.user_repository.find_all()
        return [user.to_dict() for user in users]
    
    def get_logs(self):
        """Get system logs."""
        return self.logger.get_logs()


# ========================
# 5. Factory/Builder for Easy Setup
# ========================
def create_user_service():
    """Factory function to create a fully configured UserService."""
    logger = Logger()
    user_repository = UserRepository()
    email_validator = EmailValidator()
    
    return UserService(
        user_repository=user_repository,
        email_validator=email_validator,
        logger=logger
    )


# ========================
# Example Usage
# ========================
if __name__ == "__main__":
    # Create a properly structured user service
    user_service = create_user_service()
    
    # Same functionality as before, but now following SRP
    try:
        user1 = user_service.create_user("john_doe", "john@example.com")
        user2 = user_service.create_user("jane_smith", "jane@example.com")
        print("Users created successfully")
    except ValueError as e:
        print(f"Error creating user: {e}")
    
    # List users
    users = user_service.list_users()
    print(f"Total users: {len(users)}")
    
    # Update user
    try:
        user_service.update_user("john_doe", email="john.doe@newdomain.com")
        print("User updated successfully")
    except ValueError as e:
        print(f"Error updating user: {e}")
    
    # View logs
    logs = user_service.get_logs()
    print(f"Total log entries: {len(logs)}")
    
    # Delete user
    try:
        user_service.delete_user("jane_smith")
        print("User deleted successfully")
    except ValueError as e:
        print(f"Error deleting user: {e}")
