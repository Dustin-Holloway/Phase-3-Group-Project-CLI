#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from tabulate import tabulate
from db.users import User
from db.bikes import Bike, bike_locker
from db.lockers import Locker

noble_steed='''
██╗░░░██╗░█████╗░██╗░░░██╗██████╗░  ███╗░░██╗░█████╗░██████╗░██╗░░░░░███████╗
╚██╗░██╔╝██╔══██╗██║░░░██║██╔══██╗  ████╗░██║██╔══██╗██╔══██╗██║░░░░░██╔════╝
░╚████╔╝░██║░░██║██║░░░██║██████╔╝  ██╔██╗██║██║░░██║██████╦╝██║░░░░░█████╗░░
░░╚██╔╝░░██║░░██║██║░░░██║██╔══██╗  ██║╚████║██║░░██║██╔══██╗██║░░░░░██╔══╝░░
░░░██║░░░╚█████╔╝╚██████╔╝██║░░██║  ██║░╚███║╚█████╔╝██████╦╝███████╗███████╗
░░░╚═╝░░░░╚════╝░░╚═════╝░╚═╝░░╚═╝  ╚═╝░░╚══╝░╚════╝░╚═════╝░╚══════╝╚══════╝

░██████╗████████╗███████╗███████╗██████╗░
██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔══██╗
╚█████╗░░░░██║░░░█████╗░░█████╗░░██║░░██║
░╚═══██╗░░░██║░░░██╔══╝░░██╔══╝░░██║░░██║
██████╔╝░░░██║░░░███████╗███████╗██████╔╝
╚═════╝░░░░╚═╝░░░╚══════╝╚══════╝╚═════╝░
'''



bike_locker='''
████████╗██╗░░██╗███████╗  ██████╗░██╗██╗░░██╗███████╗  ██╗░░░░░░█████╗░░█████╗░██╗░░██╗███████╗██████╗░
╚══██╔══╝██║░░██║██╔════╝  ██╔══██╗██║██║░██╔╝██╔════╝  ██║░░░░░██╔══██╗██╔══██╗██║░██╔╝██╔════╝██╔══██╗
░░░██║░░░███████║█████╗░░  ██████╦╝██║█████═╝░█████╗░░  ██║░░░░░██║░░██║██║░░╚═╝█████═╝░█████╗░░██████╔╝
░░░██║░░░██╔══██║██╔══╝░░  ██╔══██╗██║██╔═██╗░██╔══╝░░  ██║░░░░░██║░░██║██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
░░░██║░░░██║░░██║███████╗  ██████╦╝██║██║░╚██╗███████╗  ███████╗╚█████╔╝╚█████╔╝██║░╚██╗███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚═════╝░╚═╝╚═╝░░╚═╝╚══════╝  ╚══════╝░╚════╝░░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
'''

wheels_up = '''
---------- __o       __o       __o       __o
-------- _`\<,_    _`\<,_    _`\<,_    _`\<,_
------- (*)/ (*)  (*)/ (*)  (*)/ (*)  (*)/ (*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
welcome_back='''
░██╗░░░░░░░██╗███████╗██╗░░░░░░█████╗░░█████╗░███╗░░░███╗███████╗░░░
░██║░░██╗░░██║██╔════╝██║░░░░░██╔══██╗██╔══██╗████╗░████║██╔════╝░░░
░╚██╗████╗██╔╝█████╗░░██║░░░░░██║░░╚═╝██║░░██║██╔████╔██║█████╗░░░░░
░░████╔═████║░██╔══╝░░██║░░░░░██║░░██╗██║░░██║██║╚██╔╝██║██╔══╝░░██╗
░░╚██╔╝░╚██╔╝░███████╗███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║███████╗╚█║
░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝░╚╝

                ██████╗░░█████╗░░█████╗░██╗░░██╗░░░
                ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝░░░
                ██████╦╝███████║██║░░╚═╝█████═╝░░░░
                ██╔══██╗██╔══██║██║░░██╗██╔═██╗░██╗
                ██████╦╝██║░░██║╚█████╔╝██║░╚██╗╚█║
                ╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚╝
'''

welcome_user='''

░██╗░░░░░░░██╗███████╗██╗░░░░░░█████╗░░█████╗░███╗░░░███╗███████╗░░░
░██║░░██╗░░██║██╔════╝██║░░░░░██╔══██╗██╔══██╗████╗░████║██╔════╝░░░
░╚██╗████╗██╔╝█████╗░░██║░░░░░██║░░╚═╝██║░░██║██╔████╔██║█████╗░░░░░
░░████╔═████║░██╔══╝░░██║░░░░░██║░░██╗██║░░██║██║╚██╔╝██║██╔══╝░░██╗
░░╚██╔╝░╚██╔╝░███████╗███████╗╚█████╔╝╚█████╔╝██║░╚═╝░██║███████╗╚█║
░░░╚═╝░░░╚═╝░░╚══════╝╚══════╝░╚════╝░░╚════╝░╚═╝░░░░░╚═╝╚══════╝░╚╝
'''


art='''

░██████╗██████╗░██████╗░░█████╗░░█████╗░██╗░░██╗███████╗████████╗    ██████╗░██╗██╗░░██╗███████╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██╔════╝╚══██╔══╝    ██╔══██╗██║██║░██╔╝██╔════╝
╚█████╗░██████╔╝██████╔╝███████║██║░░╚═╝█████═╝░█████╗░░░░░██║░░░    ██████╦╝██║█████═╝░█████╗░░
░╚═══██╗██╔═══╝░██╔══██╗██╔══██║██║░░██╗██╔═██╗░██╔══╝░░░░░██║░░░    ██╔══██╗██║██╔═██╗░██╔══╝░░
██████╔╝██║░░░░░██║░░██║██║░░██║╚█████╔╝██║░╚██╗███████╗░░░██║░░░    ██████╦╝██║██║░╚██╗███████╗
╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚══════╝░░░╚═╝░░░    ╚═════╝░╚═╝╚═╝░░╚═╝╚══════╝
'''

database_path = "db/bikedatabase.db"

engine = create_engine(f"sqlite:///{database_path}")
Session = sessionmaker(bind=engine)
session = Session()

current_user = ""


@click.command()
def welcome():
    click.clear()
    click.echo(click.style(
            "\n\n\n" + (art),
            blink=True,
            bold=True,
            fg="green",
        ))
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
@click.option("--name", prompt=click.style("\n\n\n" + "Please enter your name to begin", blink=True,
            bold=True,
            fg="green",
))

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
        select_option2()


def select_option1():
    global current_user
    click.clear()
    click.echo(click.style("\n\n\n" + (welcome_user), bold=True, fg="green"))

    click.echo(click.style("\n" + f"                             {current_user.name}!" + "\n\n", bold=True, fg="red",))

    options = ["Rent", "Return"]
    prompt = "\n\n\n" + "Would you like to rent a " + click.style("siq bike? ", blink=True,
            bold=True,
            fg="green",) + "or are you here to return one?" + "\n\n"
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option1(selected_option)




def select_option2():
    global current_user
    click.clear()
    click.echo(click.style("\n" + (welcome_back), bold=True, fg="green"))

    click.echo(click.style("\n" + f"                             {current_user.name}!" + "\n\n", bold=True, fg="red",))

    options = ["I'm done", "More shred"]
    prompt = "\n\n\n" + "Are you finished with your ride?, or did you still want to shred???" + "\n\n\n"
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option2(selected_option)


def handle_option1(option):
    if option == "Rent":
        click.echo("\n" + "Ok!")
        click.clear()
        display_locations()
        enter_locations()


    elif option == "Return":
        let_get_rad(current_user)

def handle_option2(option):
    if option == "I'm done":
        # click.clear()
        
        display_locations()

    elif option == "More shred":
        click.clear()
        click.echo("\n\n\n\n"+ "        We'll see you when you get back!")

        click.echo("\n\n\n" +   wheels_up)
        click.echo("\n" + "             Keep it on two wheels!"+ "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


        # let_get_rad(current_user)


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
    click.clear()
    lockers = session.query(Locker).all()
    headers = [l.id for l in lockers]
    locker = [l.locker_location for l in lockers]
    table = tabulate([locker], headers, tablefmt="mixed_grid")
    click.echo(click.style("\n\n\n\n" + (table), bg="bright_green", fg="black", bold=True))
    enter_locations()


@click.command()
@click.option("--bike_id", prompt="Please enter a bike ID to check out", type=int)
def select_bike(bike_id):
    global current_user

    selected_bike = session.query(Bike).filter(Bike.id == bike_id).first()
    user = session.query(User).filter(User.name == current_user.name).first()
    headers = [selected_bike.id]

    table = tabulate([[selected_bike.name]], headers, tablefmt="mixed_grid")
    click.clear()
    click.echo(noble_steed)
    click.echo(click.style((table), bg="bright_green", fg="black", bold=True) + "\n\n")

    selected_bike.locker_id = None
    session.commit()
    user.bike = selected_bike.id
    session.commit()
    selected_bike.user_id = user.id
    session.commit()
    # click.clear()
    click.echo("           Keep it on two wheels!!!" + "\n\n\n\n\n\n")
    click.echo(wheels_up + "\n\n\n\n\n")


@click.command()
@click.option(
    "--location_id", prompt="\n\n\n\n\n" + "Which location are you renting from today?  Please enter the hub ID", type=int
)
def enter_locations(location_id):
    lockers = session.query(Locker).all()
    headers = [l.id for l in lockers]
    locker = [l.locker_location for l in lockers]
    table = tabulate([locker], headers, tablefmt="mixed_grid")
    click.echo(click.style("\n\n" + (table), bg="bright_green", fg="black", bold=True))
    locker = session.query(Locker).filter(Locker.id == location_id).first()
    click.clear()
    display_table(locker)


def display_table(locker):
    click.echo(bike_locker)
    bikes = [bike.name for bike in locker.bikes if bike.locker_id]
    headers = [b.id for b in locker.bikes]
    table = tabulate([bikes], headers, tablefmt="mixed_grid")
    # click.echo("\n" "Take a look around!  See anything you like?" + "\n")
    click.echo(click.style((table), bg="bright_green", fg="black", bold=True) + "\n\n")
    select_bike()


if __name__ == "__main__":
    welcome()
