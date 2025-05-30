"""
This file provides a template/example of how the refactored code might look after applying SRP.
This is for reference and discussion during the training session.

DO NOT look at this until after you've attempted the refactoring yourself!

This UserManager class has multiple responsibilities:
1. User data management (CRUD operations)
2. Email validation
3. Logging operations
4. File operations (JSON export)

This violates SRP because the class has multiple reasons to change:
- Changes in user data structure
- Changes in email validation rules
- Changes in logging requirements
- Changes in file export format
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
import json


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
        return {
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'is_active': self.is_active
        }
    
    def update(self, **kwargs):
        """Update user attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# ========================
# 2. Validation Services
# ========================
class EmailValidator:
    """Single responsibility: Validate email formats."""
    
    @staticmethod
    def is_valid(email: str) -> bool:
        """Check if email format is valid."""
        # Pattern that allows valid characters but prevents consecutive dots
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+%-]*[a-zA-Z0-9]@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
        # Check for consecutive dots which should not be allowed
        if '..' in email:
            return False
        return re.match(pattern, email) is not None


# ========================
# 3. Logging Service
# ========================
class Logger:
    """Single responsibility: Handle logging operations."""
    
    def __init__(self):
        self.log_entries = []
    
    def log(self, message: str):
        """Add a log entry."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.log_entries.append(log_entry)
    
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
        self.users[user.username] = user
    
    def find_by_username(self, username: str):
        """Find user by username."""
        return self.users.get(username)
    
    def delete(self, username: str):
        """Delete user from storage."""
        if username in self.users:
            del self.users[username]
            return True
        return False
    
    def find_all(self):
        """Get all users."""
        return list(self.users.values())
    
    def exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self.users


# ========================
# 5. File Operations Service
# ========================
class DataExporter:
    """Single responsibility: Handle data export operations."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def export_to_json(self, data: dict, filename: str) -> bool:
        """Export data to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.logger.log(f"Data exported to {filename}")
            return True
        except Exception as e:
            self.logger.log(f"Failed to export data: {str(e)}")
            return False


# ========================
# 6. Main Service (Orchestrator)
# ========================
class UserService:
    """
    Single responsibility: Orchestrate user operations.
    This class coordinates between other services but doesn't contain business logic for validation, etc.
    """
    
    def __init__(self, 
                 user_repository: UserRepository,
                 email_validator: EmailValidator,
                 logger: Logger,
                 data_exporter: DataExporter):
        
        self.user_repository = user_repository
        self.email_validator = email_validator
        self.logger = logger
        self.data_exporter = data_exporter
    
    def create_user(self, username: str, email: str):
        """Create a new user with validation."""
        # Validate email
        if not self.email_validator.is_valid(email):
            self.logger.log(f"Failed to create user {username}: Invalid email")
            raise ValueError("Invalid email format")
        
        # Check if user already exists
        if self.user_repository.exists(username):
            self.logger.log(f"Failed to create user {username}: User already exists")
            raise ValueError("User already exists")
        
        # Create user
        user = User(username, email)
        
        # Save user
        self.user_repository.save(user)
        self.logger.log(f"User {username} created successfully")
        
        return user.to_dict()
    
    def get_user(self, username: str):
        """Retrieve user data."""
        user = self.user_repository.find_by_username(username)
        if user is None:
            self.logger.log(f"Failed to retrieve user {username}: User not found")
            return None
        
        self.logger.log(f"User {username} retrieved successfully")
        return user.to_dict()
    
    def update_user(self, username: str, **kwargs):
        """Update user data with validation."""
        user = self.user_repository.find_by_username(username)
        if user is None:
            self.logger.log(f"Failed to update user {username}: User not found")
            raise ValueError("User not found")
        
        # Validate email if being updated
        if 'email' in kwargs:
            if not self.email_validator.is_valid(kwargs['email']):
                self.logger.log(f"Failed to update user {username}: Invalid email")
                raise ValueError("Invalid email format")
        
        # Update user
        user.update(**kwargs)
        self.user_repository.save(user)  # Save updated user
        self.logger.log(f"User {username} updated successfully")
        
        return user.to_dict()
    
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
    
    def export_users_to_json(self, filename: str):
        """Export users to JSON file."""
        users = self.user_repository.find_all()
        users_dict = {user.username: user.to_dict() for user in users}
        return self.data_exporter.export_to_json(users_dict, filename)
    
    def get_logs(self):
        """Get system logs."""
        return self.logger.get_logs()


# ========================
# 7. Factory/Builder for Easy Setup
# ========================
def create_user_service():
    """Factory function to create a fully configured UserService."""
    logger = Logger()
    user_repository = UserRepository()
    email_validator = EmailValidator()
    data_exporter = DataExporter(logger)
    
    return UserService(
        user_repository=user_repository,
        email_validator=email_validator,
        logger=logger,
        data_exporter=data_exporter
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
    
    # Export data
    user_service.export_users_to_json("users_backup.json")
    
    # View logs
    logs = user_service.get_logs()
    print(f"Total log entries: {len(logs)}")
    
    # Delete user
    try:
        user_service.delete_user("jane_smith")
        print("User deleted successfully")
    except ValueError as e:
        print(f"Error deleting user: {e}")
