import click
import travelio
from jendela import scrap_link, scrap_each_page

@click.command()
@click.option('--web', default='jendela', help='website name to scrap')
def scrap(web):
    if web == 'jendela':
        list_urls = scrap_link()
        rmq = scrap_each_page.delay(list_urls)
        rmq.ready()
        rmq.get()
    elif web == 'travelio':
        travelio.scrap()


if __name__ == "__main__":
    scrap()