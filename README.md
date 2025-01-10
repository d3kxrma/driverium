[![PyPI Downloads](https://static.pepy.tech/badge/driverium)](https://pepy.tech/projects/driverium)
# Driverium

Driverium is a Python library that provides functionality for managing and downloading ChromeDriver for different Chrome versions.

## Installation

To install Driverium, simply use pip:

```shell
pip install driverium
```

## Usage

```python
from driverium import Driverium
from selenium import webdriver
# Create an instance of Driverium
driverium = Driverium()

# Get the path to the ChromeDriver
driver_path = driverium.get_driver()

# Use the ChromeDriver path in your Selenium code
driver = webdriver.Chrome(driver_path)
```
or you can use driverium like this:

```python
from driverium import Driverium
from selenium import webdriver

driver = webdriver.Chrome(Driverium().get_driver())
```

### Methods

#### `get_driver() -> str`

Retrieves the path to the ChromeDriver. If the driver is not found, it will download it first.

#### `get_driver_url() -> str`

Retrieves the URL of the ChromeDriver based on the specified Chrome version.

#### `get_new_driver() -> str`

Retrieves the path to the latest version of the ChromeDriver.

#### `get_old_driver() -> str`

Retrieves the path to an older version of the ChromeDriver.

#### `download_driver(url: str) -> str`

Downloads the ChromeDriver from the specified URL and returns the path to the downloaded driver.

#### `quiet_download(url: str) -> io.BytesIO`

Downloads the file from the specified URL without displaying progress.

#### `progress_download(url: str) -> io.BytesIO`

Downloads the file from the specified URL and displays progress using a progress bar.


## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the [GitHub repository](https://github.com/d3kxrma/driverium).


## License

Driverium is licensed under the MIT License. See the [LICENSE](https://github.com/d3kxrma/driverium/blob/main/LICENSE) file for more information.
