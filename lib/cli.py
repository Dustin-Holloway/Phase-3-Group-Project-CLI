#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from tabulate import tabulate
from db.users import User
from db.bikes import Bike, bike_locker
from db.lockers import Locker


database_path = "db/bikedatabase.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()

current_user = ""


@click.command()
def welcome():
    click.clear()
    click.echo(
        click.style(
            "\n\n\n" + "Welcome to the Sracket CLI!",
            blink=True,
            bold=True,
            fg="green",
        )
    )
    username()


@click.command()
@click.option("--name", prompt="\n\n" + "Please enter your Name")
def username(name):
    global current_user
    users = session.query(User).all()
    user_names = [n.name for n in users]

    if not name in user_names:
        new_user = User(name=name)
        current_user = new_user
        session.add(new_user)
        session.commit()
        select_option1()

    # elif name in user_names and name.bike == None:
    #     click.echo("Would you like to rent a bike?")

    else:
        click.echo("You already have a bike checked out!")
        user_to_get = session.query(User).filter(User.name == name).first()
        current_user = user_to_get
        select_option1()


def select_option1():
    global current_user
    options = ["Rent a bike", "Return a bike"]
    prompt = "What can I help you with today?"
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option1(selected_option)


def handle_option1(option):
    if option == "Rent a bike":
        # click.clear()
        click.echo("\n" + "Let's get rad!")
        display_locations()

    elif option == "Return a bike":
        let_get_rad(current_user)


def let_get_rad(current_user):
    returned_user = session.query(User).filter(User.name == current_user.name).first()
    returned_bike = session.query(Bike).filter(Bike.id == returned_user.bike).first()
    returned_user.bike = None
    session.commit()
    returned_bike.locker_id = 2
    session.commit()
    returned_bike.user_id = None
    session.commit()
    session.delete(returned_user)
    session.commit()
    click.clear()
    click.echo(
        click.style(
            "\n\n" + "Go home!",
            blink=True,
            bold=True,
            fg="green",
        )
    )


def display_locations():
    lockers = session.query(Locker).all()
    headers = [l.id for l in lockers]
    locker = [l.locker_location for l in lockers]
    table = tabulate([locker], headers, tablefmt="mixed_grid")
    click.echo(click.style("\n\n" + (table), bg="bright_yellow", fg="black", bold=True))
    enter_locations()


@click.command()
@click.option("--bike_id", prompt="\n\n" "Please enter bike ID", type=int)
def select_bike(bike_id):
    global current_user

    selected_bike = session.query(Bike).filter(Bike.id == bike_id).first()
    user = session.query(User).filter(User.name == current_user.name).first()
    selected_bike.locker_id = None
    session.commit()
    user.bike = selected_bike.id
    session.commit()
    selected_bike.user_id = user.id
    session.commit()
    click.clear()
    click.echo("You're all set, have a nice ride!!!" + "\n\n\n\n\n\n")


@click.command()
@click.option(
    "--location_id", prompt="\n\n" + "Select your current locker ID", type=int
)
def enter_locations(location_id):
    locker = session.query(Locker).filter(Locker.id == location_id).first()
    display_table(locker)


def display_table(locker):
    click.clear()
    bikes = [bike.name for bike in locker.bikes if bike.locker_id]
    headers = [b.id for b in locker.bikes]
    table = tabulate([bikes], headers, tablefmt="mixed_grid")
    click.echo("\n" "Take a look around!  See anything you like?" + "\n")
    click.echo(click.style((table), bg="bright_yellow", fg="black", bold=True) + "\n\n")
    select_bike()


if __name__ == "__main__":
    welcome()
