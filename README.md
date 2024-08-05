# Company Contacts Scraper

This project is a web scraping tool designed to collect company contact information from google maps. The application features a graphical user interface (GUI) built with Tkinter, and it utilizes Selenium WebDriver for scraping. The collected data is saved in a CSV file for easy access and management.

## Features

- **Graphical User Interface (GUI):** Built with Tkinter to allow users to input name of company, and choose destination folder in your computer where we put the csv file.
- **Web Scraping:** Uses Selenium WebDriver to navigate web pages and extract contact information.
- **Data Storage:** Saves the extracted data in a CSV file for easy analysis and retrieval.

## Installation

### Prerequisites

- Python 3.x
- Google Chrome
- [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads/)

### Required Python Packages

To install the required Python packages, run:

```bash
pip install selenium
```
## Usage

- **Download the WebDriver:** Make sure you have the correct version of ChromeDriver installed on your system and that it matches your browser version.
- **Run the Application:** Execute the Python script to launch the Tkinter GUI.
- **Use the GUI:** Enter the name of company and choose destination folder in your computer where we put the csv file.
- **Output:** The extracted contact information will be saved in a CSV file in the specified output directory.

## Libraries Used

- **Tkinter:** Provides the graphical user interface for user interaction.
- **CSV:** Handles the reading and writing of CSV files.
- **Time:** Introduces delays in the scraping process.
- **Selenium:** Automates web browsers and extracts data from web pages.
- **WebDriver:** Interfaces with the web browser to control it programmatically.
