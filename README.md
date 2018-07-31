# logAnalysis

**logAnalysis** is a simple python program that helps you to find answers for the following questions by checking your PostgreSQL database named *news*:
* Which articles are most viewed?
* What is the rank of most popular article authors of all time?
* Which days you observed more errors than a given threshold?

## Installation

You need following packages to be installed on your computer before using this program:
* [Python2.7.12](https://www.python.org/downloads/release/python-2712/)
* PostgreSQL command line program
	```sh
	$ sudo apt-get update
	$ sudo apt-get install postgresql postgresql-contrib
	```
* Log files to be checked (you can find a sample [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip))
	```sh
	$ psql -d news -f newsdata.sql
	```

## Usage

Once your environment is ready, you may call the program as following:
```sh
$ python logAnalysis.py
```

## Function Calls to Modify Requests

### getMostPopularArticles()

### getMostPopularAuthors()

### getErrorousDays()