# Goddard

Web Scrapper.<br>
Websites list to scrap (can add more later):
1.  [jendela360]
2.  [travelio]

## Issues
- We can scrap websites using BeautifulSoup (library provided by Python)
- But I cant get the tags (the result is empty list: []) because of Javascript effects.(reference: https://towardsdatascience.com/data-science-skills-web-scraping-javascript-using-python-97a29738353f).
- Thus I am trying Selenium to scrap the website.
- I could get the scrap result on Jendela website using Selenium but not with Travelio, there are some issues while getting the elements. Thus, I tried using Go with `ferret` package. You may check [ferret] repo.

### Notes:

Selenium uses Chrome Driver (not Chrome Browser that we used daily).<br>

Here are the link to download https://sites.google.com/a/chromium.org/chromedriver/downloads/version-selection

### Installation
##### Goddard is using Python and Go.
The differences is explained below.
- Python is used to scrap jendela360 website
- Go is used to scrap Travelio website

Steps to use this projects will explained as below.
- Install go first (in case you didn't have it yet).
You may install go using following [golang] tutorial by novalagung

- Ensure that you have set `GOPATH` to your env by `echo $GOPATH`
- If it prints nothing, then you need to set `GOPATH` to `~/.bashrc` or `~/.profile` 
```sh
$ echo "export GOPATH=$HOME/Documents/go" >> ~/.bashrc
```
Those directory is just example. You may change the directory as you wish.
Or you may check [gopath] tutorial for details.
- Create 3 folders inside `GOPATH` . It consists of:
1. `src`
2. `bin`
3. `pkg`
- From any directory, pull the repository using this `go` command
```sh
$ go get github.com/SpaceStock/Goddard
```
After pulled the repo using `go get`. Follows guide below to install anything needs by `python`. First of all, let's call our project which located on `$GOPATH/src/github.com/SpaceStock/Goddard` with `project` directory.
- Install `python3-venv` first (in case you didn't have yet)

```sh
(On Debian/Ubuntu Based)
$ sudo apt-get install python3-venv
```
- Then, create virtual environment
```sh
project$ python3 -m venv venv
```
<b>Notes</b>: `python3` is pre-installed on Ubuntu so you won't need to install it. 

Before install the dependencies, make sure to activate the environment to <b>isolate</b> it with system dependencies.
```sh
project$ source venv/bin/activate
```
- Then, you may install the all libraries used on this project.
```sh
(venv) project$ pip install -r requirements.txt
```
- If you install some new libraries to the project, make sure to write it on `requirements.txt` by using:

```sh
project$ pip freeze > requirements.txt
```
### License
---
MIT

[//]: #  (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

[jendela360]: <https://jendela360.com>
[travelio]: <https://www.travelio.com/>
[ferret]: <https://github.com/MontFerret/ferret>
[golang]: <https://dasarpemrogramangolang.novalagung.com/2-instalasi-golang.html>
[gopath]: <https://dasarpemrogramangolang.novalagung.com/3-gopath-dan-workspace.html>