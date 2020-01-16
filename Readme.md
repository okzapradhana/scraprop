# Goddard

Web Scrapper using Python.
Websites list to scrap (can add more later):
1. [jendela360]
2. [travelio]

## Issues
  - We can scrap websites using BeautifulSoup (library provided by Python)
  - But I cant get the tags (the result is empty list: []) because of Javascript effects (reference: https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f).
  - Thus I am trying Selenium to scrap the website.

### Notes:
Selenium uses Chrome Driver (not Chrome Browser that we used daily). 
Here are the link to download https://sites.google.com/a/chromium.org/chromedriver/downloads/version-selection)

Mine uses: https://chromedriver.storage.googleapis.com/index.html?path=79.0.3945.36/

### Installation

##### Goddard is using Python 3.6.0.
Install the all libraries used on this project using command:

```sh
> pip install requirements.txt
```

If you install some new libraries to the project, make sure to write it on `requirements.txt` by using:

```sh
> pip freeze > requirements.txt
```


License
----

MIT


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
    
   [jendela360]: <https://jendela360.com>
   [travelio]: <https://www.travelio.com/>