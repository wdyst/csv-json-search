import os
import datetime


def search_directory(directory_path):
    # Ask user for search text
    search_text = input("Enter text to search for: ")
    print(f"Searching for files containing \"{search_text}\" in {directory_path}...\n")

    # Get all files in directory and subdirectories
    file_list = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".txt") or file.endswith(".csv"):
                file_list.append(os.path.join(root, file))

    # Search through files for text
    output_file = None
    found_files = []
    for file in file_list:
        with open(file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f):
                if search_text in line:
                    if not output_file:
                        output_file = f"outputs/{search_text}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
                        found_files.append(output_file)
                    with open(output_file, 'a', encoding='utf-8') as f2:
                        f2.write(f"{file} ({line_num + 1}): {line}\n")

    # Output found files
    if found_files:
        print(f"\nFound files containing \"{search_text}\":")
        for file in found_files:
            print(file)

        copy_lines = input(
            "\nDo you want to copy the lines where the search text was found to a new file? (y/n): ").lower() == "y"
        if copy_lines:
            new_file_name = f"{search_text}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
            new_file_path = os.path.join(directory_path, new_file_name)
            with open(new_file_path, 'w', encoding='utf-8') as f:
                with open(output_file, 'r', encoding='utf-8') as f2:
                    lines = f2.readlines()
                    for line in lines:
                        f.write(line)
            print(f"\nCopied lines to {new_file_path}.")
    else:
        print(f"No files found containing \"{search_text}\".")


def main():
    # Check if there is a saved directory path
    if os.path.isfile('last_directory.txt'):
        with open('last_directory.txt', 'r') as f:
            last_directory = f.read()
    else:
        last_directory = None

    # Ask user for directory path
    directory_path = input(f"Enter directory path (default={last_directory}): ") or last_directory
    while not os.path.isdir(directory_path):
        directory_path = input(
            f"Directory does not exist. Enter directory path again (default={last_directory}): ") or last_directory

    # Save directory path for next time
    with open('last_directory.txt', 'w') as f:
        f.write(directory_path)

    search_directory(directory_path)


if __name__ == "__main__":
    main()
