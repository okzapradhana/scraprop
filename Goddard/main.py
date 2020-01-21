import jendela
import click

@click.command()
@click.option('--web', default='jendela', help='website name to scrap')
def scrap(web):
    if web == 'jendela':
        jendela.scrap()


if __name__ == "__main__":
    scrap()