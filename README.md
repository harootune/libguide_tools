LibGuide Tools
---

A set of Scrapy-based spiders which are intended to help the UIUC Library System identify broken and outdated links for
editing.

Further development will make these spiders generalizable to other LibGuides users (thanks to [Dynamic Spiders](https://github.com/harootune/scrapy_dynamic_spiders)).

### How to Use
*Requirements*

- [Python](https://www.python.org/) 3.6 and above
- [Pip](https://pip.pypa.io/en/stable/)

*Setup*

1. Clone this repository to the directory of your choice
2. Open the command line and navigate to that directory
3. Install Python package requirements
    - Make sure that you are in the same directory as "requirements.txt"
    - type the following command: 
    ```bash
    pip install -r requirements.txt
    ```

*Spiders*

This project offers two spiders:

- **bl-spider** - Checks for broken links
- **sv-spider** - Checks for SFX and Vufind links

Each spider will output a csv file containing its report. The name of this file is either automatically generated or
provided by the user.

*Usage*

1. Open the command line and navigate to the libguide_spiders directory
2. The general pattern for commands is:
    ```bash
    scrapy crawl [SPIDERNAME] -a [OPTION1]=[VALUE1] -a [OPTION2]=[VALUE2] etc...
    ```
   - Replace \[SPIDERNAME\] with the name of the spider you would like to use
   - Replace \[OPTION#\] with the name of an option
   - Replace \[VALUE#\] with a value for an option. Non-numeric options should be in **double quotes**
       - Every option **must** be prepended with "-a"

*Options*  
  
A number of options are available to customize the functionality of your Spiders.

```start_urls``` - a single URL or list of URLs to scan. Only one URL is necessary for each guide. If a list is passed,
each entry in the list should be separated with a comma "," with no spaces around it   
```from_file``` - the name of .csv file that you would like to read guide URLs from. This .csv file must have a header
called "URLs", like the .csv files created automatically by LibGuides. If provided, any urls provided to ```start_urls```
will be ignored  
```csv_path``` - the path to the .csv file (new or existing) that you would like to write results to. **If it is an existing
.csv file, it will be overwritten**

*Examples*  
  
Check all URLs in a .csv file for broken links, and output results to a file named "results.csv":
```bash
scrapy crawl bl-spider -a from_file="guides.csv" -a csv_path="results.csv"
```   
Check a pair of provided URLs for vufind and sfx links, output results to the default filename:
```bash
scrapy crawl sv-spider -a start_urls="https://www.urlone.com,https://www.urltwo.com"
```
