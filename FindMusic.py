import subprocess

def find_files(file_extensions):
    """Finds files with specified extensions using the find command."""
    found_files = set()

    for ext in file_extensions:
        try:
            result = subprocess.run(['find', '/', '-type', 'f', '-name', f'*.{ext}'], capture_output=True, text=True, check=True)
            files = result.stdout.splitlines()
            found_files.update(files)
        except subprocess.CalledProcessError as e:
            print(f"Error finding files with extension '{ext}': {e}")

    return found_files

def main():
    file_extensions = ['mp3', 'mp4', 'mov', 'zip', '7z']
    
    found_files = find_files(file_extensions)

    if found_files:
        print("Found files:")
        for file_path in found_files:
            print(f" - {file_path}")
    else:
        print("No files found.")

if __name__ == "__main__":
    main()
