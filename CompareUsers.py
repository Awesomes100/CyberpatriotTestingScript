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

def main():
    file_path = 'users.txt'
    file_users = read_users_from_file(file_path)
    linux_users = get_linux_users()

    # Compare the users
    new_users = file_users - linux_users
    removed_users = linux_users - file_users

    print("Users in the file but not on the system:")
    for user in new_users:
        print(f" - {user}")

    print("\nUsers on the system but not in the file:")
    for user in removed_users:
        print(f" - {user}")

    print("\nComparison complete.")

if __name__ == "__main__":
    main()
