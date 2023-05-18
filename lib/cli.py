#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import ipdb
from db.models import Info
from db.bikes import Bike
import click
from tabulate import tabulate

database_path = "db/bikedatabase.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()

current_user = ""


@click.command()
def welcome():
    click.echo(
        click.style(
            "Welcome to the Sracket CLI!",
            underline=True,
            blink=True,
            bold=True,
            fg="green",
            bg="bright_white",
        )
    )
    username()


@click.command()
@click.option("--name", prompt="Please enter your Name")
def username(name):
    global current_user
    new_user = Info(name=name)
    current_user = new_user
    session.add(new_user)
    session.commit()
    display_table()


@click.command()
@click.option("--bike_id", prompt="Please enter bike ID", type=int)
def select_bike(bike_id):
    global current_user
    click.clear()
    selected_bike = session.query(Bike).filter(Bike.id == bike_id).first()
    user = session.query(Info).filter(Info.name == current_user.name).first()
    user.bike = selected_bike.id
    session.commit()
    selected_bike.user_info = user.id
    session.commit()
    selected_bike.available = 0
    session.commit()
    select_option()


def display_table():
    bikes = session.query(Bike).all()
    bike_list = [b.name for b in bikes]
    headers = [b.id for b in bikes]

    table = tabulate([bike_list], headers, tablefmt="mixed_grid")
    click.echo("Please browse our current collection of cool looking Bikes!")
    click.echo(click.style((table), bold=True, bg="bright_white"))
    select_bike()


@click.command()
def select_option():
    global current_user
    options = ["Return", "Rent"]
    prompt = "Please select an option"
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option(selected_option)


def handle_option(option):
    if option == "Return":
        click.echo("You selected Option 1")
    elif option == "Rent":
        click.echo("You selected Option 2")
    else:
        click.echo("Invalid option")


if __name__ == "__main__":
    welcome()
