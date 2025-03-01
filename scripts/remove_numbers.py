def remove_numbers_from_authors_file(filepath):
    """
    Removes numbers and leading/trailing whitespace from each line of a file,
    assuming each line represents an author's name prefixed with a number.

    Args:
        filepath: The path to the file containing the author names.
    """
    try:
        with open(filepath, "r") as f_in:
            lines = f_in.readlines()

        with open(filepath, "w") as f_out:
            for line in lines:
                # Remove leading digits and the following dot and space if any
                line = line.strip()
                if line:
                    parts = line.split(". ", 1)
                    if len(parts) > 1 and parts[0].isdigit():
                        line = parts[1].strip()
                    elif line.startswith(tuple(str(n) + ". " for n in range(1000))):
                        line = line[len(parts[0]) + 2 :].strip()

                # Write the cleaned line back to the file
                if line:
                    f_out.write(line + "\n")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage (assuming the file is named authors.txt in the current directory)
filepath = "/home/hamed/dev/libro/data/authors.txt"
remove_numbers_from_authors_file(filepath)
print(f"Finished processing: {filepath}")
