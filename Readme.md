# Goddard
Welcome to <b>Readme</b>! Which is the first thing you will see when visiting this Repo. In this <b>Readme</b>, you will see:
1. Overview
2. Project Structure
3. Code Structure
4. Quick Install

### Overview
<b>Goddard</b> is a Repo to do scrapping on several websites such as.
1. [Jendela360]
2. [Travelio]
3. [Rumah123]

### Project Structure
<b>Goddard</b> was developed with this project structure:
```
    ├── Goddard             # python scrap code goes here
		├── jendela.py		# scrap jendela website
		└── main.py			# main program to control which websites to scrap
		└── travelio.py		# scrap travelio website
    ├── venv                # virtual environment
    ├── .env                # environment variable
    ├── .gitignore			# directories and files to ignore
    ├── README.md			
    └── requirements.txt	# packages listed here
```

### Code Structure
Simpy run `python run main.py --web=jendela/travelio`. 
But before that, make sure you have installed all packages (explained in [here](#quick-install)) and locate your current directory at `Goddard/main.py` first.
```
#main.py
@click.command()
@click.option('--web', default='jendela', help='website name to scrap')

def scrap(web):
	if web == 'jendela':
		....
	elif web == 'travelio':
		....
```
From code above, it will check your `web` key command. If the value is `jendela` it will run scrap code for `jendela`, same goes for `travelio`.

### Quick Install
To run your program successfully. You need to do quick install in which the steps listed below (you may check wiki for installation details):
1. Install `python3-venv`
2. Create `venv` a.k.a `virtual environment` with `python3-venv`
3. Install dependencies that are listed on `requirements.txt`
4. Congrats! You're ready to scrap some websites!
###

[//]: #  (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

  

[Jendela360]: <https://jendela360.com>

[Travelio]: <https://www.travelio.com/>

[Rumah123]: <https://www.rumah123.com>