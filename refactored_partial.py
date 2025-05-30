"""
This file provides a partial template for how the refactored code should look after applying SRP.
This is a starting template to help guide your refactoring exercise.

EXERCISE: Complete the missing implementations marked with TODO comments.
Estimated time: 30 minutes

The original UserManager class has multiple responsibilities:
1. User data management (CRUD operations)  
2. Email validation

This violates SRP because the class has multiple reasons to change:
- Changes in user data structure
- Changes in email validation rules

Your task: Complete the TODO sections to make this a fully working SRP-compliant solution.

"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


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
        # Should return: {
        #     'username': self.username,
        #     'email': self.email,
        #     'created_at': self.created_at,
        #     'is_active': self.is_active
        # }
        pass
    
    def update(self, **kwargs):
        """Update user attributes."""
        # TODO: Implement method to update user attributes
        # For each key, value in kwargs.items():
        #   - Check if the attribute exists using hasattr(self, key)
        #   - If it exists, update it using setattr(self, key, value)
        # This allows updating email, is_active, or other valid attributes
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
        # - Use regex pattern: r'^[a-zA-Z0-9][a-zA-Z0-9._+%-]*[a-zA-Z0-9]@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
        # - Check for consecutive dots (..) which should not be allowed
        # - Return True if valid, False otherwise
        # Hint: if '..' in email: return False, then use re.match(pattern, email) is not None
        pass


# ========================
# 3. Data Storage Service
# ========================
class UserRepository:
    """Single responsibility: Handle user data persistence."""
    
    def __init__(self):
        self.users = {}
    
    def save(self, user: User):
        """Save user to storage."""
        # TODO: Implement save functionality
        # Store the user in self.users dictionary using username as key:
        # self.users[user.username] = user
        pass
    
    def find_by_username(self, username: str):
        """Find user by username."""
        # TODO: Implement user lookup
        # Check if username exists in self.users, return the user object if found
        # Return None if not found: return self.users.get(username)
        pass
    
    def delete(self, username: str):
        """Delete user from storage."""
        # TODO: Implement user deletion
        # Check if user exists, then delete from self.users
        # Return True if deleted, False if user didn't exist
        # if username in self.users:
        #     del self.users[username]
        #     return True
        # return False
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
                 email_validator: EmailValidator):
        
        self.user_repository = user_repository
        self.email_validator = email_validator
        self.logger = logging.getLogger(__name__)
    
    def create_user(self, username: str, email: str):
        """Create a new user with validation."""
        # TODO: Implement user creation logic
        # Steps:
        # 1. Validate email using self.email_validator.is_valid(email)
        #    - If invalid: log error and raise ValueError("Invalid email format")
        # 2. Check if user already exists using self.user_repository.exists(username)
        #    - If exists: log error and raise ValueError("User already exists")
        # 3. Create new User object: user = User(username, email)
        # 4. Save user using self.user_repository.save(user)
        # 5. Log success message: self.logger.info(f"User {username} created successfully")
        # 6. Return user.to_dict()
        # Error logging format: self.logger.error(f"Failed to create user {username}: reason")
        pass
    
    def get_user(self, username: str):
        """Retrieve user data."""
        # TODO: Implement user retrieval
        # 1. Find user using self.user_repository.find_by_username(username)
        # 2. If user not found:
        #    - Log warning: self.logger.warning(f"Failed to retrieve user {username}: User not found")
        #    - Return None
        # 3. If user found:
        #    - Log success: self.logger.info(f"User {username} retrieved successfully")
        #    - Return user.to_dict()
        pass
    
    def update_user(self, username: str, **kwargs):
        """Update user data with validation."""
        # TODO: Implement user update logic
        # 1. Find user using self.user_repository.find_by_username(username)
        #    - If not found: log error and raise ValueError("User not found")
        # 2. If 'email' in kwargs:
        #    - Validate email using self.email_validator.is_valid(kwargs['email'])
        #    - If invalid: log error and raise ValueError("Invalid email format")
        # 3. Update user object using user.update(**kwargs)
        # 4. Save updated user using self.user_repository.save(user)
        # 5. Log success: self.logger.info(f"User {username} updated successfully")
        # 6. Return user.to_dict()
        # Error logging format: self.logger.error(f"Failed to update user {username}: reason")
        pass
    
    def delete_user(self, username: str):
        """Delete a user."""
        user = self.user_repository.find_by_username(username)
        if user is None:
            self.logger.error(f"Failed to delete user {username}: User not found")
            raise ValueError("User not found")
        
        # Delete user
        self.user_repository.delete(username)
        self.logger.info(f"User {username} deleted successfully")
        
        return True
    
    def list_users(self):
        """List all users."""
        self.logger.info("User list retrieved")
        users = self.user_repository.find_all()
        return [user.to_dict() for user in users]
    
    def get_logs(self):
        """Return a dummy log structure for test compatibility."""
        # This is just for backward compatibility with tests
        # In the real implementation, you would use Python's logging module
        return [{'timestamp': datetime.now().isoformat(), 'message': 'Logging now handled by Python logger'}]


# ========================
# 5. Factory/Builder for Easy Setup
# ========================
def create_user_service():
    """Factory function to create a fully configured UserService."""
    user_repository = UserRepository()
    email_validator = EmailValidator()
    
    return UserService(
        user_repository=user_repository,
        email_validator=email_validator
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
