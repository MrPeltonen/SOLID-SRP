"""
Example of a Python class that violates the Single Responsibility Principle (SRP).

"""

import re
from datetime import datetime

class UserManager:
    """
    A class that violates Single Responsibility Principle.
    """
    
    def __init__(self):
        self.users = {}
        self.log_entries = []
    
    def create_user(self, username, email):
        """Create a new user with validation and logging."""
        if not self._is_valid_email(email):
            self._log(f"Failed to create user {username}: Invalid email")
            raise ValueError("Invalid email format")
        
        if username in self.users:
            self._log(f"Failed to create user {username}: User already exists")
            raise ValueError("User already exists")
        
        user_data = {
            'username': username,
            'email': email,
            'created_at': datetime.now().isoformat(),
            'is_active': True
        }
        
        self.users[username] = user_data
        self._log(f"User {username} created successfully")
        
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
        
        # Update user data
        self.users[username].update(kwargs)
        self._log(f"User {username} updated successfully")
        
        return self.users[username]
    
    def delete_user(self, username):
        """Delete a user."""
        if username not in self.users:
            self._log(f"Failed to delete user {username}: User not found")
            raise ValueError("User not found")
        
        del self.users[username]
        self._log(f"User {username} deleted successfully")
        
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
    



# Example usage 
if __name__ == "__main__":
    user_manager = UserManager()
    
    # Creating users (involves validation and logging)
    try:
        user1 = user_manager.create_user("john_doe", "john@example.com")
        user2 = user_manager.create_user("jane_smith", "jane@example.com")
        print("Users created successfully")
    except ValueError as e:
        print(f"Error creating user: {e}")
    
    # List users
    users = user_manager.list_users()
    print(f"Total users: {len(users)}")
    
    # Update user (involves validation)
    try:
        user_manager.update_user("john_doe", email="john.doe@newdomain.com")
        print("User updated successfully")
    except ValueError as e:
        print(f"Error updating user: {e}")
    
    # View logs
    logs = user_manager.get_logs()
    print(f"Total log entries: {len(logs)}")
    
    # Delete user
    try:
        user_manager.delete_user("jane_smith")
        print("User deleted successfully")
    except ValueError as e:
        print(f"Error deleting user: {e}")
