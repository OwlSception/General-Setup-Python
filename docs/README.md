# Your Project Title

## Description
A brief description of your project, its purpose, and what it aims to achieve.

## Installation Instructions
To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

* Note: Usage Guidelines for BLAST and other API Resources:
-- Do not contact the server more often than once every 10 seconds.
-- Do not poll for any single RID more often than once a minute.
-- Use the URL parameter email and tool, so that NCBI can contact you if there is a problem.
-- Run Scripts weekends or between 9pm and 5am Eastern time on weekdays if more than 50 searches will be submitted. 

* Efficiency:
-- BLAST often runs more efficiently if multiple queries are sent as one search rather than if each query is sent as an individual search (blastn, megablast, and tblastn). If your queries are short (less than a few hundred bases) we suggest you merge them into one search of up to 1000 bases. 

## Contributors


## License


## Contact Information
