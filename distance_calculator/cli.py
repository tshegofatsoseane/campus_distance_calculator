import click
from .calculator import calculate_distance_and_time_to_campuses

@click.command()
@click.argument('street_address')
def calculate_distances(street_address):
    """
    Calculate distances and durations from the provided street address to each campus.
    """
    results = calculate_distance_and_time_to_campuses(street_address)
    
    if not results:
        click.echo("Could not get geocode location for the provided address.")
        return

    for campus, modes in results.items():
        click.echo(f"\n{campus} Campus:")
        for mode, info in modes.items():
            click.echo(f"  {mode.capitalize()}:")
            click.echo(f"    Distance: {info['distance']}")
            click.echo(f"    Duration: {info['duration']}")

if __name__ == '__main__':
    calculate_distances()
