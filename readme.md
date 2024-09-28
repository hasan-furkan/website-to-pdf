# Website to pdf 

This Python script scrapes the website and generates a PDF containing the content from all pages.

## Features

- Extracts content including titles, paragraphs, images, and code blocks
- Removes sidebar elements from the scraped pages
- Generates a single PDF file containing all the extracted content

## Requirements

- Python 3.x
- Required Python packages:
  - requests
  - beautifulsoup4
  - lxml
  - pdfkit
  - tqdm

## Installation

1. Clone this repository or download the `main.py` file.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Install wkhtmltopdf (required by pdfkit):
   - For Windows: Download and install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
   - For macOS: `brew install wkhtmltopdf`
   - For Linux: `sudo apt-get install wkhtmltopdf`

## Usage

1. Open `main.py` and modify the `url` variable if you want to start from a different page of the Django documentation.
2. Run the script:

```bash
python main.py
```

3. The script will display progress as it scrapes the website and generates the PDF.
4. Once complete, you'll find a `output.pdf` file in the same directory as the script.

## Limitations

- The script may take a while to run, depending on the number of pages in the documentation.
- Some complex page layouts or dynamic content may not be captured perfectly in the PDF.
- The script doesn't handle pagination or create a table of contents for the PDF.

## Contributing

Feel free to fork this repository and submit pull requests to improve the functionality or add new features.

## License

This project is open-source and available under the MIT License.
