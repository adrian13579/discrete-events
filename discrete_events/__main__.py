import typer

from .simulation import HappyComputing
from .random_variables import generate_client


def run_simulation(T=480, verbose=False):
    sim = HappyComputing(T)
    while sim.time_arrival <= sim.T or sim.n:
        sim.time_advance()
    if verbose:
        typer.echo(f"Total time: {sim.time}")
        typer.echo(f"Total profits: {sim.profits}")
    return sim


def main():

    typer.echo(
        typer.style(
            """
  _    _                          
 | |  | |                         
 | |__| | __ _ _ __  _ __  _   _  
 |  __  |/ _` | '_ \| '_ \| | | | 
 | |  | | (_| | |_) | |_) | |_| | 
 |_|  |_|\__,_| .__/| .__/ \__, | 
              | |   | |     __/ | 
              |_|   |_|    |___/  
  _____                            _   _             
 / ____|                          | | (_)            
| |     ___  _ __ ___  _ __  _   _| |_ _ _ __   __ _ 
| |    / _ \| '_ ` _ \| '_ \| | | | __| | '_ \ / _` |
| |___| (_) | | | | | | |_) | |_| | |_| | | | | (_| |
 \_____\___/|_| |_| |_| .__/ \__,_|\__|_|_| |_|\__, |
                      | |                       __/ |
                      |_|                      |___/ 

            """,
            fg=typer.colors.BLUE,
        )
    )
    typer.echo("In this simulation there are 2 sellers, 3 technicians and")
    typer.echo("1 specialized technician. Each simulation represent an 8 hours workday")
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    number_simulation = int(
        typer.prompt("How many times do you want to execute the simulation?")
    )
    avg_profits = 0
    avg_time = 0
    avg_exceeded_time = 0
    avg_clients = 0
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    with typer.progressbar(range(number_simulation)) as simulations:
        for _ in simulations:
            result = run_simulation()
            avg_time += result.time
            avg_exceeded_time += result.time - result.T
            avg_profits += result.profits
            avg_clients += result.arrivals_count

    avg_time /= number_simulation
    avg_profits /= number_simulation
    avg_exceeded_time /= number_simulation
    avg_clients /= number_simulation

    avg_time = round(avg_time, 2)
    avg_profits = round(avg_profits, 2)
    avg_exceeded_time = round(avg_exceeded_time, 2)
    avg_clients = round(avg_clients,2)

    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style(
            "--------------------------------------------------------------------------",
            fg=typer.colors.BRIGHT_BLUE,
        )
    )
    typer.echo(
        typer.style("Average of time:", fg=typer.colors.BRIGHT_GREEN)
        + f" {avg_time} minutes"
    )
    typer.echo(
        typer.style("Average of time exceeded:", fg=typer.colors.BRIGHT_RED)
        + f" {avg_exceeded_time} minutes"
    )
    typer.echo(
        typer.style("Average of profits: ", fg=typer.colors.BRIGHT_GREEN)
        + f" {avg_profits}$"
    )

    typer.echo(
        typer.style("Average of number of clients: ", fg=typer.colors.BRIGHT_GREEN)
        + f" {avg_clients}"
    )


if __name__ == "__main__":
    typer.run(main)
