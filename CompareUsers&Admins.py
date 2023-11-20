import subprocess

def read_users_from_file(file_path):
    """Reads the list of users from a file."""
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def get_linux_users():
    """Gets the list of users on a Debian-based Linux system."""
    try:
        result = subprocess.run(['getent', 'passwd'], capture_output=True, text=True, check=True)
        user_lines = result.stdout.splitlines()
        return set(line.split(':')[0] for line in user_lines)
    except subprocess.CalledProcessError as e:
        print(f"Error getting Linux users: {e}")
        return set()

def get_sudo_users():
    """Gets the list of users in the sudo group."""
    try:
        result = subprocess.run(['getent', 'group', 'sudo'], capture_output=True, text=True, check=True)
        sudo_users = result.stdout.split(':')[3].split(',')
        return set(sudo_users)
    except subprocess.CalledProcessError as e:
        print(f"Error getting sudo users: {e}")
        return set()

def read_admins_from_file(file_path):
    """Reads the list of admin users from a file."""
    try:
        with open(file_path, 'r') as file:
            return set(line.strip() for line in file)
    except FileNotFoundError:
        print(f"Admins file '{file_path}' not found.")
        return set()

def main():
    file_path = 'users.txt'
    admins_file_path = 'admins.txt'
    
    file_users = read_users_from_file(file_path)
    linux_users = get_linux_users()
    
    sudo_users = get_sudo_users()
    admins_users = read_admins_from_file(admins_file_path)

    # Compare the users
    new_users = file_users - linux_users
    removed_users = linux_users - file_users

    sudo_not_in_admins = sudo_users - admins_users
    admins_not_in_sudo = admins_users - sudo_users

    print("Users in the file but not on the system:")
    for user in new_users:
        print(f" - {user}")

    print("\nUsers on the system but not in the file:")
    for user in removed_users:
        print(f" - {user}")

    print("\nUsers in the sudo group but not in admins.txt:")
    for user in sudo_not_in_admins:
        print(f" - {user}")

    print("\nUsers in admins.txt but not in the sudo group:")
    for user in admins_not_in_sudo:
        print(f" - {user}")

    print("\nComparison complete.")

if __name__ == "__main__":
    main()
