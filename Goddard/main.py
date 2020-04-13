import click
import travelio
import rumah
import jendela
from celery import group

@click.command()
@click.option('--web', default='jendela', help='website name to scrap')
def scrap(web):
    if web == 'jendela':
        '''
        if using celery
        list_urls = jendela.scrap_link()
        rmq = group(jendela.scrap_each_page.s(url) for url in list_urls)
        result = rmq.apply_async()
        '''

        #not using celery
        links = jendela.scrap_link()
        jendela.scrap_each_page(links)
    elif web == 'travelio':
        links = travelio.scrap_href()
        travelio.scrap(links)
    elif web == 'rumah123':
        regions = rumah.scrap_region()
        properties = rumah.scrap_properties(regions)
        rumah.scrap(properties)

if __name__ == "__main__":
    scrap()