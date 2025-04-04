# Inspiration CLI

A Python command-line tool to fetch and display inspirational quotes from [azquotes.com](https://www.azquotes.com/).

## Features

* Fetches quotes from a selection of notable authors.
* Provides a simple interactive command-line interface for the user to select an author.
* Allows users to either random quotes from a specific author.
* Incorporates a timed pause after displaying each quote to encourage reflection.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/rbmckinnie/inspiration  
    cd inspiration
    ```

2.  **Install the dependencies:**

    * Ensure you have Python 3.x installed.
    * It is recommended to create a virtual environment
    * Install the required packages using pip:


    ```bash
    pip install -r requirements.txt
    ```
    
## Usage

1.  Run the script:

    ```bash
    python inspiration.py
    ```

2.  The script will display a list of authors.

3.  Enter the number corresponding to the author you'd like to receive a quote from.

4.  If the input is invalid, the user will be prompted to try again, or given the option to exit

5.  The quote will be displayed, followed by a timed pause.

6.  You'll be prompted if you'd like to hear another quote.

## Code Explanation

The core functionality of the script is structured around these key functions:

* `pull_all_quotes_by_author(item, format="list", max_retries=10, initial_delay=0.5, backoff_factor=2)`: This function handles the web scraping from azquotes.com. It takes an author's identifier (`item`), handles pagination, and includes error handling and retry logic to ensure quotes are fetched successfully. It can return the data as a list or a DataFrame.
* `pull_all_quotes_for_random_author(main_list=default_author_list)`: This function retrieves quotes from a randomly selected author from a provided list of authors. It uses the `pull_all_quotes_by_author` function to fetch the quotes.
* `return_random_quote(author=None)`: This function is called by the main program loop. It takes an optional `author` parameter. If an author is provided, it fetches a random quote from that author. If no author is provided, it fetches a random quote from any author in the list.
* `create_link(extension)`: Constructs the URL for the author's quote page on azquotes.com.
* `return_soup_obj(url, max_retries=10, initial_delay=2, backoff_factor=2)`: Retrieves the HTML content from a given URL and parses it using BeautifulSoup. Includes retry logic for handling potential request errors.

## Author Selection

The following authors are available in the current selection:

```
1 Booker T Washington
2 Carol S Dweck
3 Howard Thurman
4 Kobe Bryant
5 Marshall B Rosenberg
6 Robert Greene
7 Tara Brach
8 Timothy Gallwey
```

## Data Structures

The script uses two dictionaries to manage author data:

* `author_dict`: Maps numerical keys (used for user input) to the author identifiers used in the URL.
* `name_dict`: Maps numerical keys to the full names of the authors.

## Error Handling

The script includes error handling to manage potential issues during web requests and user input. It uses `requests` library exceptions for handling HTTP errors and `ValueError` for invalid user input.

## Contributing

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them.
4.  Push your changes to your fork.
5.  Submit a pull request.

## License

This project is licensed under the MIT License - see the [License.md](license.md)  file for details.

## Acknowledgements

* [azquotes.com](https://www.azquotes.com/) for the source of the quotes.
* Libraries used:
    * `requests`
    * `beautifulsoup4`
    * `pandas`

```
