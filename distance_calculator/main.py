import click
from .calculator import calculate_distance_and_time_to_campuses, determine_nearest_campus

@click.command()
@click.argument('street_address')
def calculate_distances(street_address):
    """
    Calculate distances and durations from the provided street address to each campus,
    and print the nearest campus for each university.
    """
    results = calculate_distance_and_time_to_campuses(street_address)
    
    if not results:
        click.echo("Could not get geocode location for the provided address.")
        return

    for university, campuses in results.items():
        click.echo(f"\n{university}:")

        for campus, modes in campuses.items():
            click.echo(f"\n  {campus} Campus:")
            for mode, info in modes.items():
                click.echo(f"    {mode.capitalize()}:")
                click.echo(f"      Distance: {info['distance']}")
                click.echo(f"      Duration: {info['duration']}")
        # Determine and print the nearest campus
        nearest_campus = determine_nearest_campus(campuses)
        if nearest_campus:
            click.echo(f"\n   Nearest Campus: {nearest_campus}")

if __name__ == '__main__':
    calculate_distances()
