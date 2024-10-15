from sys import platform
from zipfile import ZipFile
import os
import io
import json

import chrome_version
import requests
from tqdm import tqdm

class Driverium:
    """
    A class that provides functionality for managing and downloading ChromeDriver for different Chrome versions.
    Args:
        browser_version (str, optional): The version of the Chrome browser. If not provided, it will use the current installed version. Defaults to None.
        download_path (str, optional): The path where the ChromeDriver will be downloaded. If not provided, it will use the current working directory. Defaults to None.
        logging (bool, optional): Flag indicating whether to enable logging. Defaults to False.
    Methods:
        get_driver_url() -> str:
            Retrieves the URL of the ChromeDriver based on the specified Chrome version.
        download_driver(url: str) -> str:
            Downloads the ChromeDriver from the specified URL and returns the path to the downloaded driver.
        get_driver() -> str:
            Retrieves the path to the ChromeDriver. If the driver is not found, it will download it first.
        quiet_download(url: str) -> io.BytesIO:
            Downloads the file from the specified URL without displaying progress.
        progress_download(url: str) -> io.BytesIO:
            Downloads the file from the specified URL and displays progress using a progress bar.
    """
    
    def __init__(self, browser_version:str = None, download_path:str = None, logging:bool = False):
        
        if browser_version is None:
            self.chrome_version = chrome_version.get_chrome_version().split(".")
        else:
            self.chrome_version = browser_version.split(".")
            
        if download_path is None:
            self.download_path = os.getcwd()
        else:
            self.download_path = download_path
            
        self.platf = "".join([x for x in platform if x.isalpha()]) + "64"
        self.logging = logging
    
    def get_new_driver(self) -> str:
        """
        Retrieves the URL of the appropriate driver based on the specified Chrome version and platform.
        Returns:
            str: The URL of the driver.
        Raises:
            Exception: If no driver is found for the specified Chrome version.
        """
        r = requests.get("https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
        drivers_data = r.json()["versions"][::-1]

        driver_versions = []
        
        for num, version in enumerate(self.chrome_version):
            temp_list = []
            for element in drivers_data:
                el_version = element["version"].split(".")
                if el_version[num] == version:
                    if num == 0:
                        if "chromedriver" in element["downloads"].keys():
                            temp_list.append(element)
                    else:
                        temp_list.append(element)
            if len(temp_list) > 0:
                driver_versions = temp_list
            else:
                break
            drivers_data = temp_list
            
        if len(driver_versions) == 0:
            raise Exception(f"No driver found for version {'.'.join(self.chrome_version)}")
        
        for driver in driver_versions:
            for dow in driver["downloads"]["chromedriver"]:
                if dow["platform"] == self.platf:
                    if self.logging:
                        print(f"Driver version: {driver['version']}")
                    return dow["url"]
    
    def get_old_driver(self) -> str:
        """
        Fetches the download URL for the old version of the ChromeDriver based on the current Chrome version.
        This method constructs the URL for the latest release of the ChromeDriver that matches the major version
        of the current Chrome browser.
        Returns:
            str: The URL to download the ChromeDriver zip file for the specified platform.
        """
        
        formatted_version = ".".join(self.chrome_version[:-1])
        r = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{formatted_version}")
        driver_version = r.text.strip()

        r = requests.get(f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{self.platf}.zip")
        
        if r.status_code == 404:
            return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{platform}.zip"
        else:
            return f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{self.platf}.zip"
    
    def get_driver_url(self) -> str:
        """
        Determines the appropriate driver URL based on the Chrome version.
        If the major version of Chrome is 113 or higher, it retrieves the new driver URL.
        Otherwise, it retrieves the old driver URL.
        Returns:
            str: The URL of the appropriate driver.
        """
        
        if int(self.chrome_version[0]) >= 113:
            return self.get_new_driver()
        
        return self.get_old_driver()
                
    def download_driver(self, url:str) -> str:
        """
        Downloads the driver from the given URL and returns the path to the downloaded driver.
        Parameters:
            url (str): The URL from which to download the driver.
        Returns:
            str: The path to the downloaded driver.
        """
        if self.logging:
            zip_bytes = self.progress_download(url)
        else:
            zip_bytes = self.quiet_download(url)

        with ZipFile(zip_bytes) as zip_ref:
            for file in zip_ref.namelist():
                if "/" in file:
                    file_condition = file.split("/")[-1]
                else:
                    file_condition = file
                if file_condition.startswith("chromedriver"):
                    if "/" not in file:
                        self.download_path = os.path.join(self.download_path, f"chromedriver-{self.platf}")
                    zip_ref.extract(file, self.download_path)
                    break
        
        driver_path = os.path.join(self.download_path, file)
        if "win" in self.platf:
            driver_path = driver_path.replace("/", "\\")
        
        data = {"version": ".".join(self.chrome_version),
                "path": driver_path}
        
        with open(os.path.join("\\".join(driver_path.split("\\")[:-1]), "data.json"), "w") as f:
            json.dump(data, f)
        
        if "linux" in self.platf:
            os.chmod(driver_path, 0o755)
    
        return driver_path
    
    def get_driver(self) -> str:
        """
        Retrieves the path to the ChromeDriver. If the driver is not found, it will download it first.
        Returns:
            str: The path to the Chrome driver.
        """
        if self.logging:
            print("Detected Chrome version:", ".".join(self.chrome_version))
        path_to_driver = os.path.join(self.download_path, f"chromedriver-{self.platf}")
        path_to_data = os.path.join(path_to_driver, "data.json")
        if os.path.exists(path_to_data):
            with open(os.path.join(path_to_driver, "data.json"), "r") as f:
                data = json.load(f)
                
            if data["version"] == ".".join(self.chrome_version):
                path_to_driver = data["path"]
            
            else:
                os.remove(os.path.join(path_to_driver, "data.json"))
                os.remove(data["path"])
                path_to_driver = self.download_driver(self.get_driver_url())
        else:
            path_to_driver = self.download_driver(self.get_driver_url())
            
        if self.logging:
            print("Driver path:", path_to_driver)
        return path_to_driver

    def quiet_download(self, url:str) -> io.BytesIO:
        """
        Downloads the content of the given URL and returns it as a BytesIO object.
        Parameters:
            url (str): The URL to download the content from.
        Returns:
            io.BytesIO: The content of the URL as a BytesIO object.
        """
        r = requests.get(url)
        return io.BytesIO(r.content)
    
    def progress_download(self, url:str) -> io.BytesIO:
        """
        Downloads a file from the given URL and tracks the progress using a progress bar.
        Args:
            url (str): The URL of the file to download.
        Returns:
            io.BytesIO: The downloaded file as a BytesIO object.
        """
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))

        zip_bytes = io.BytesIO()
        
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='driver download', initial=0, ascii=True) as pbar:
            for data in response.iter_content(1024):
                zip_bytes.write(data)
                pbar.update(len(data))

        zip_bytes.seek(0)
        
        return zip_bytes
if __name__ == "__main__":
    d = Driverium(logging=True)
    print(d.get_driver())