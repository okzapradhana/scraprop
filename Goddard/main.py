import click
import travelio
from jendela import scrap_link, scrap_each_page
from celery import group

@click.command()
@click.option('--web', default='jendela', help='website name to scrap')
def scrap(web):
    if web == 'jendela':
        list_urls = scrap_link()
        rmq = group(scrap_each_page.s(url) for url in list_urls)
        result = rmq.apply_async()
    elif web == 'travelio':
        travelio.scrap()


if __name__ == "__main__":
    scrap()