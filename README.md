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

This version of the program currently answers the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

Functions created to answer these questions are designed in a generic manner. You may edit below function calls to get answers to different versions of these questions.

### getMostPopularArticles(theDB, theLimit)
* theDB	: connection to Postgre SQL database *news*
* theLimit : number of top articles to be viewed. Set this value to 0 (zero) to get the whole list

### getMostPopularAuthors(theDB, theLimit)
* theDB	: connection to Postgre SQL database *news*
* theLimit : number of top authors to be viewed. Set this value to 0 (zero) to get the whole list

### getErrorousDays(theDB, theErrorRatio)
* theDB	: connection to Postgre SQL database *news*
* theErrorRatio : Error ratio threshold that you want to see the days with more errors. Set this value to 0.01 to see days with more than 1% errors

## License
logAnalysis is Copyright © 2018-2020 . It is free software, and may be redistributed under the terms specified in the [LICENSE](LICENSE) file.