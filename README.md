# Meraki Search Networks by Name

For a given organization, loop through each network name and search it for
the specified search string. Return a list of networks where a match was 
found. Write the results to a file.

## Requirements

- Python 3.10
- Requests library
  - `pip install -r requirements.txt`

## Using the script

Before running the script, look under the main function for the following:

    # UPDATE THESE SETTINGS AS DESIRED
    search_string = 'abc'
    filename = "networks.csv"
    
The search_string variable is the text that you want to search for. The results
will be written to the variable filename.

