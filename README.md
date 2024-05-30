# Web Scraping and Session Management Tool

## Description
This project provides a robust framework for web scraping and session management using Selenium WebDriver. Designed to interact with websites, maintain session states, and handle browser interactions efficiently, it offers dynamic configuration and comprehensive logging. Key differentiators include persistent session management, modular design, and robust error handling, making it adaptable and reliable for various scraping requirements.

### Key Features
- **Persistent Session Management**: Maintain authentication states across interactions, reducing the need for repeated logins.
- **Modular Design**: Organized into clear modules for configuration, services, utilities, interfaces, and models.
- **Custom Logging**: Detailed logging capabilities with configurable levels and custom log records.
- **Dynamic Configuration**: Easy setup using environment variables and `.env` files.
- **Remote Browser Support**: Supports running Selenium WebDriver in a remote server setup.
- **Specific Use Case Implementation**: Includes an implementation for the O'Reilly website, demonstrating extensibility.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation
To set up the project locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/pedroanisio/web-scraping.git
    cd web-scraping-session-management
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Create a `.env` file in the root directory and add the necessary environment variables:
    ```ini
    LOG_FILE=logs/logfile.log
    LOG_LEVEL=INFO
    REMOTE_URL=http://<selenium-grid-docker>:4444/wd/hub
    SESSIONS_DIR=data/
    BROWSER_OPTIONS=--headless --disable-gpu
    OREILLY_OPEN_URL=https://www.example.com
    OREILLY_LOGIN_URL=https://www.example.com/login
    OREILLY_AUTHED_URL=https://www.example.com/secure
    OREILLY_EMAIL=username@example.com
    OREILLY_PASSWORD=password
    ```

## Usage
To use the project, follow these steps:

1. **Initialize and Start the Application**:
    ```bash
    python app.py
    ```

2. **Example Interaction**:
    The `app.py` script initializes the logger, sets up the `ChromeRemote`, `SessionManager`, and `Browser`, and then uses the `OreillySite` model to check authentication and perform interactions.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to the contributors of Selenium WebDriver and related projects.
- Thanks to the open-source community for their invaluable resources and support.

---

Feel free to reach out with any questions or feedback. Happy scraping!
