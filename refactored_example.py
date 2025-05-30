"""
This file provides a template/example of how the refactored code might look after applying SRP.
This is for reference and discussion during the training session.

DO NOT look at this until after you've attempted the refactoring yourself!
"""

from abc import ABC, abstractmethod
from datetime import datetime
import hashlib
import re
import json


# ========================
# 1. User Model (Data)
# ========================
class User:
    """Represents a user entity - Single responsibility: Hold user data."""
    
    def __init__(self, username: str, email: str, encrypted_password: str):
        self.username = username
        self.email = email
        self.encrypted_password = encrypted_password
        self.created_at = datetime.now().isoformat()
        self.is_active = True
    
    def to_dict(self):
        """Convert user to dictionary representation."""
        return {
            'username': self.username,
            'email': self.email,
            'password': self.encrypted_password,
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
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


class PasswordValidator:
    """Single responsibility: Validate password strength."""
    
    @staticmethod
    def is_valid(password: str) -> bool:
        """Check if password meets security requirements."""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True


# ========================
# 3. Security Service
# ========================
class PasswordEncryption:
    """Single responsibility: Handle password encryption."""
    
    @staticmethod
    def encrypt(password: str) -> str:
        """Encrypt password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()


# ========================
# 4. Logging Service
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
# 5. Communication Service
# ========================
class EmailService:
    """Single responsibility: Handle email communications."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def send_welcome_email(self, email: str, username: str):
        """Send welcome email to new user."""
        message = f"Welcome {username}! Your account has been created successfully."
        self.logger.log(f"Welcome email sent to {email}: {message}")
        # In real implementation, integrate with email service provider
    
    def send_goodbye_email(self, email: str, username: str):
        """Send goodbye email to deleted user."""
        message = f"Goodbye {username}! Your account has been deleted."
        self.logger.log(f"Goodbye email sent to {email}: {message}")
        # In real implementation, integrate with email service provider


# ========================
# 6. Data Storage Service
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
# 7. File Operations Service
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
# 8. Main Service (Orchestrator)
# ========================
class UserService:
    """
    Single responsibility: Orchestrate user operations.
    This class coordinates between other services but doesn't contain business logic for validation, encryption, etc.
    """
    
    def __init__(self, 
                 user_repository: UserRepository,
                 email_validator: EmailValidator,
                 password_validator: PasswordValidator,
                 password_encryption: PasswordEncryption,
                 email_service: EmailService,
                 logger: Logger,
                 data_exporter: DataExporter):
        
        self.user_repository = user_repository
        self.email_validator = email_validator
        self.password_validator = password_validator
        self.password_encryption = password_encryption
        self.email_service = email_service
        self.logger = logger
        self.data_exporter = data_exporter
    
    def create_user(self, username: str, email: str, password: str):
        """Create a new user with validation."""
        # Validate email
        if not self.email_validator.is_valid(email):
            self.logger.log(f"Failed to create user {username}: Invalid email")
            raise ValueError("Invalid email format")
        
        # Validate password
        if not self.password_validator.is_valid(password):
            self.logger.log(f"Failed to create user {username}: Weak password")
            raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and number")
        
        # Check if user already exists
        if self.user_repository.exists(username):
            self.logger.log(f"Failed to create user {username}: User already exists")
            raise ValueError("User already exists")
        
        # Create user
        encrypted_password = self.password_encryption.encrypt(password)
        user = User(username, email, encrypted_password)
        
        # Save user
        self.user_repository.save(user)
        self.logger.log(f"User {username} created successfully")
        
        # Send welcome email
        self.email_service.send_welcome_email(email, username)
        
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
        
        # Validate and encrypt password if being updated
        if 'password' in kwargs:
            if not self.password_validator.is_valid(kwargs['password']):
                self.logger.log(f"Failed to update user {username}: Weak password")
                raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and number")
            kwargs['encrypted_password'] = self.password_encryption.encrypt(kwargs['password'])
            del kwargs['password']  # Remove plain password
        
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
        
        email = user.email
        
        # Delete user
        self.user_repository.delete(username)
        self.logger.log(f"User {username} deleted successfully")
        
        # Send goodbye email
        self.email_service.send_goodbye_email(email, username)
        
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
# 9. Factory/Builder for Easy Setup
# ========================
def create_user_service():
    """Factory function to create a fully configured UserService."""
    logger = Logger()
    user_repository = UserRepository()
    email_validator = EmailValidator()
    password_validator = PasswordValidator()
    password_encryption = PasswordEncryption()
    email_service = EmailService(logger)
    data_exporter = DataExporter(logger)
    
    return UserService(
        user_repository=user_repository,
        email_validator=email_validator,
        password_validator=password_validator,
        password_encryption=password_encryption,
        email_service=email_service,
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
        user1 = user_service.create_user("john_doe", "john@example.com", "SecurePass123")
        user2 = user_service.create_user("jane_smith", "jane@example.com", "StrongPass456")
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
