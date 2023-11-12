# Subtitle and MKV File Management Tool

## Project Overview

This tool is designed to simplify the management of MKV video files and their associated subtitle tracks. It provides a user-friendly interface for various operations such as extracting subtitles, updating subtitle tracks, and more. The application is built in Python, utilizing PyQt for the GUI and leveraging tools like FFmpeg and MKVToolNix for file manipulation.

## Features

- **Subtitle Extraction**: Extract subtitle tracks from MKV files.
- **Subtitle Track Management**: Selectively keep or remove subtitle tracks from MKV files.
- **Batch Processing**: Process multiple files at once for efficient management.

## Getting Started

### Prerequisites

- Python 3.x
- PyQt6
- FFmpeg (for certain functionalities)
- MKVToolNix (for handling MKV files)


### Installation

1. Clone the repository:
   ```bash
   git clone [repository URL]
   ```

2. Navigate to the project directory:
    ```bash
    cd Sub-Manager
    ```

3. Install dependencies (if any):
    ```bash
    pip install -r requirements.txt
    ```


### Running the Application

Execute the main script to launch the application:
    ```
    python src/main.py
    ```

## Adding Custom Commands

The application is designed to be extensible, allowing for the addition of custom commands for various operations.

### Command Interface

Each command should implement the `Command` interface, which includes the following method:

- `execute()`: The logic of the command.

### Creating a New Command

1. **Create the Command Class**: In the `commands` directory, create a new Python file for your command.

2. **Implement the Command Interface**:
    ```python
    from commands.command import Command

    class MyCustomCommand(Command):
    def init(self, selected_files):
    # Initialization code
    pass

    def execute(self):
    # Command execution logic
    pass
    ```

3. **Register the Command**: Use the `register_command` decorator to make your command available in the application.
    ```python
    from registry.register_command import register_command

    @register_command("My Custom Command")
    class MyCustomCommand(Command):
    # ...    
    ```


4. **Implement Command Logic**: Fill in the `__init__` and `execute` methods with the logic for your command.

### Testing Your Command

Ensure to test your command thoroughly to verify that it works as expected.

## Contributing

Contributions to the project are welcome! Please adhere to the following guidelines:

- **Code Style**: Follow PEP 8 guidelines.
- **Commit Messages**: Use clear and descriptive commit messages.
- **Pull Requests**: Submit pull requests for any new features or bug fixes.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
