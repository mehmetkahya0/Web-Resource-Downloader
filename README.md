# Web Resource Downloader

This is a Python script that downloads all resources (images, scripts, stylesheets, etc.) from a given website.

## Features

- Downloads all resources from a given website
- Option to filter resources by file extension
- Saves a table of the download status of each resource in Markdown format
- Option to delete the download folder after downloading resources
- Logging: Messages are logged to a file for troubleshooting and record keeping

## Requirements

- Python 3
- `requests`
- `beautifulsoup4`
- `colorama`
- `prettytable`

## Usage

1. Install the required Python packages:

    ```bash
    pip install requests beautifulsoup4 colorama prettytable
    ```

2. Run the script with the URL of the website and the folder to download resources to:

    ```bash
    python main.py https://example.com resources
    ```

3. To filter resources by file extension, use the `--extensions` option followed by the extensions you want to download:

    ```bash
    python main.py https://example.com resources --extensions jpg png
    ```

4. To delete the download folder after downloading resources, use the `--delete` option:

    ```bash
    python main.py https://example.com resources --delete
    ```

5. To enable logging to a file, use the `--log` option followed by the name of the log file:

    ```bash
    python main.py https://example.com resources --log download.log
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
@mehmetkahya0