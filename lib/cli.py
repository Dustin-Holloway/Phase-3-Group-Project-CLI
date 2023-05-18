#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from tabulate import tabulate
from db.models import Info
from db.bikes import Bike
from db.locations import Locker

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
            blink=False,
            bold=True,
            fg="green",
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
    # display_table()
    enter_locations()


@click.command()
@click.option("--bike_id", prompt="Please enter bike ID", type=int)
def select_bike(bike_id):
    global current_user
    selected_bike = session.query(Bike).filter(Bike.id == bike_id).first()
    user = session.query(Info).filter(Info.name == current_user.name).first()
    user.bike = selected_bike.id
    session.commit()
    selected_bike.user_info = user.id
    session.commit()
    selected_bike.available = 0
    session.commit()
    select_option()


@click.command()
@click.option("--location_id", prompt="Please select current location ID", type=int)
def enter_locations(location_id):
    locker = session.query(Locker).filter(Locker.id == location_id).first()
    lock
    # print(locker)
    display_table(locker)


def display_table(locker):
    bikes = [bike.name for bike in locker.bikes]
    click.echo(locker)
    headers = [b.id for b in locker.bikes]
    table = tabulate([bikes], headers, tablefmt="mixed_grid")
    click.echo("Please browse our current collection of Spracket Bikes!")
    click.echo(click.style((table), bg="bright_yellow", fg="black", bold=True))
    # click.clear()
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
