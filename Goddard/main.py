import jendela
import click
import travelio

@click.command()
@click.option('--web', default='jendela', help='website name to scrap')
def scrap(web):
    if web == 'jendela':
        jendela.scrap()
    elif web == 'travelio':
        travelio.scrap()


if __name__ == "__main__":
    scrap()