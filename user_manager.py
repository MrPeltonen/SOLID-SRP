"""
Example of a Python class that violates the Single Responsibility Principle (SRP).

This UserManager class has multiple responsibilities:
1. User data management (CRUD operations)
2. Email validation
3. Password validation and encryption
4. Email sending functionality
5. Logging operations

This violates SRP because the class has multiple reasons to change:
- Changes in user data structure
- Changes in email validation rules
- Changes in password encryption methods
- Changes in email service providers
- Changes in logging requirements
"""

import hashlib
import re
import json
from datetime import datetime


class UserManager:
    """
    A class that violates Single Responsibility Principle by handling
    multiple concerns: user management, validation, encryption, email, and logging.
    """
    
    def __init__(self):
        self.users = {}
        self.log_entries = []
    
    def create_user(self, username, email, password):
        """Create a new user with validation and logging."""
        # Email validation responsibility
        if not self._is_valid_email(email):
            self._log(f"Failed to create user {username}: Invalid email")
            raise ValueError("Invalid email format")
        
        # Password validation responsibility
        if not self._is_valid_password(password):
            self._log(f"Failed to create user {username}: Weak password")
            raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and number")
        
        # Check if user already exists
        if username in self.users:
            self._log(f"Failed to create user {username}: User already exists")
            raise ValueError("User already exists")
        
        # Password encryption responsibility
        encrypted_password = self._encrypt_password(password)
        
        # User data management responsibility
        user_data = {
            'username': username,
            'email': email,
            'password': encrypted_password,
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        self.users[username] = user_data
        self._log(f"User {username} created successfully")
        
        # Email sending responsibility
        self._send_welcome_email(email, username)
        
        return user_data
    
    def get_user(self, username):
        """Retrieve user data."""
        if username not in self.users:
            self._log(f"Failed to retrieve user {username}: User not found")
            return None
        
        self._log(f"User {username} retrieved successfully")
        return self.users[username]
    
    def update_user(self, username, **kwargs):
        """Update user data with validation."""
        if username not in self.users:
            self._log(f"Failed to update user {username}: User not found")
            raise ValueError("User not found")
        
        # Email validation if email is being updated
        if 'email' in kwargs:
            if not self._is_valid_email(kwargs['email']):
                self._log(f"Failed to update user {username}: Invalid email")
                raise ValueError("Invalid email format")
        
        # Password validation and encryption if password is being updated
        if 'password' in kwargs:
            if not self._is_valid_password(kwargs['password']):
                self._log(f"Failed to update user {username}: Weak password")
                raise ValueError("Password must be at least 8 characters with uppercase, lowercase, and number")
            kwargs['password'] = self._encrypt_password(kwargs['password'])
        
        # Update user data
        self.users[username].update(kwargs)
        self._log(f"User {username} updated successfully")
        
        return self.users[username]
    
    def delete_user(self, username):
        """Delete a user."""
        if username not in self.users:
            self._log(f"Failed to delete user {username}: User not found")
            raise ValueError("User not found")
        
        email = self.users[username]['email']
        del self.users[username]
        self._log(f"User {username} deleted successfully")
        
        # Email sending responsibility
        self._send_goodbye_email(email, username)
        
        return True
    
    def list_users(self):
        """List all users."""
        self._log("User list retrieved")
        return list(self.users.values())
    
    def _is_valid_email(self, email):
        """Email validation responsibility - should be separate."""
        # Pattern that allows valid characters but prevents consecutive dots
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9._+%-]*[a-zA-Z0-9]@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$'
        # Check for consecutive dots which should not be allowed
        if '..' in email:
            return False
        return re.match(pattern, email) is not None
    
    def _is_valid_password(self, password):
        """Password validation responsibility - should be separate."""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    def _encrypt_password(self, password):
        """Password encryption responsibility - should be separate."""
        # Simple SHA-256 encryption (in real apps, use proper password hashing)
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _send_welcome_email(self, email, username):
        """Email sending responsibility - should be separate."""
        # Simulate sending email
        message = f"Welcome {username}! Your account has been created successfully."
        self._log(f"Welcome email sent to {email}: {message}")
        # In real implementation, this would integrate with email service
    
    def _send_goodbye_email(self, email, username):
        """Email sending responsibility - should be separate."""
        # Simulate sending email
        message = f"Goodbye {username}! Your account has been deleted."
        self._log(f"Goodbye email sent to {email}: {message}")
        # In real implementation, this would integrate with email service
    
    def _log(self, message):
        """Logging responsibility - should be separate."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message
        }
        self.log_entries.append(log_entry)
        # In real implementation, this might write to a file or external logging service
    
    def get_logs(self):
        """Retrieve all log entries."""
        return self.log_entries
    
    def export_users_to_json(self, filename):
        """Export users data to JSON file - another responsibility."""
        try:
            with open(filename, 'w') as f:
                json.dump(self.users, f, indent=2)
            self._log(f"Users exported to {filename}")
            return True
        except Exception as e:
            self._log(f"Failed to export users: {str(e)}")
            return False


# Example usage demonstrating the violations
if __name__ == "__main__":
    # This demonstrates how the class is doing too many things
    user_manager = UserManager()
    
    # Creating users (involves validation, encryption, logging, email sending)
    try:
        user1 = user_manager.create_user("john_doe", "john@example.com", "SecurePass123")
        user2 = user_manager.create_user("jane_smith", "jane@example.com", "StrongPass456")
        print("Users created successfully")
    except ValueError as e:
        print(f"Error creating user: {e}")
    
    # List users
    users = user_manager.list_users()
    print(f"Total users: {len(users)}")
    
    # Update user (involves validation and encryption if password changed)
    try:
        user_manager.update_user("john_doe", email="john.doe@newdomain.com")
        print("User updated successfully")
    except ValueError as e:
        print(f"Error updating user: {e}")
    
    # Export data (file operations)
    user_manager.export_users_to_json("users_backup.json")
    
    # View logs
    logs = user_manager.get_logs()
    print(f"Total log entries: {len(logs)}")
    
    # Delete user (involves email sending)
    try:
        user_manager.delete_user("jane_smith")
        print("User deleted successfully")
    except ValueError as e:
        print(f"Error deleting user: {e}")
