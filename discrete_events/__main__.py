import pandas as pd

# if __name__=='__main__':
#     print("Hello World!")
#     data = {'Name': ["Adrian"], 'Age':[ 22 ]}
#     df = pd.DataFrame(data)
#     print(df)

import typer


def main(good: bool = True):
    message_start = "everything is "
    if good:
        ending = typer.style("good", fg=typer.colors.GREEN, bold=True)
    else:
        ending = typer.style("bad", fg=typer.colors.WHITE, bg=typer.colors.RED)
    message = message_start + ending
    typer.echo(message)


if __name__ == "__main__":
    typer.run(main)

