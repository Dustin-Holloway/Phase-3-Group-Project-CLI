#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import click
from tabulate import tabulate
from db.users import User
from db.bikes import Bike, bike_locker
from db.lockers import Locker
import time
from datetime import datetime

#################################### ARTWORK ########################################

ok_bye = '''
░█████╗░██╗░░██╗░█████╗░██╗░░░██╗░░░  ██████╗░██╗░░░██╗███████╗██╗██╗██╗
██╔══██╗██║░██╔╝██╔══██╗╚██╗░██╔╝░░░  ██╔══██╗╚██╗░██╔╝██╔════╝██║██║██║
██║░░██║█████═╝░███████║░╚████╔╝░░░░  ██████╦╝░╚████╔╝░█████╗░░██║██║██║
██║░░██║██╔═██╗░██╔══██║░░╚██╔╝░░██╗  ██╔══██╗░░╚██╔╝░░██╔══╝░░╚═╝╚═╝╚═╝
╚█████╔╝██║░╚██╗██║░░██║░░░██║░░░╚█║  ██████╦╝░░░██║░░░███████╗██╗██╗██╗
░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚╝  ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝╚═╝╚═╝
'''

returning='''

██╗░░░██╗░█████╗░██╗░░░██╗  ██████╗░███████╗████████╗██╗░░░██╗██████╗░███╗░░██╗███████╗██████╗░
╚██╗░██╔╝██╔══██╗██║░░░██║  ██╔══██╗██╔════╝╚══██╔══╝██║░░░██║██╔══██╗████╗░██║██╔════╝██╔══██╗
░╚████╔╝░██║░░██║██║░░░██║  ██████╔╝█████╗░░░░░██║░░░██║░░░██║██████╔╝██╔██╗██║█████╗░░██║░░██║
░░╚██╔╝░░██║░░██║██║░░░██║  ██╔══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔══██╗██║╚████║██╔══╝░░██║░░██║
░░░██║░░░╚█████╔╝╚██████╔╝  ██║░░██║███████╗░░░██║░░░╚██████╔╝██║░░██║██║░╚███║███████╗██████╔╝
░░░╚═╝░░░░╚════╝░░╚═════╝░  ╚═╝░░╚═╝╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚═════╝░
'''

noble_steed='''

░██████╗░██████╗░███████╗░█████╗░████████╗  ░█████╗░██╗░░██╗░█████╗░██╗░█████╗░███████╗
██╔════╝░██╔══██╗██╔════╝██╔══██╗╚══██╔══╝  ██╔══██╗██║░░██║██╔══██╗██║██╔══██╗██╔════╝
██║░░██╗░██████╔╝█████╗░░███████║░░░██║░░░  ██║░░╚═╝███████║██║░░██║██║██║░░╚═╝█████╗░░
██║░░╚██╗██╔══██╗██╔══╝░░██╔══██║░░░██║░░░  ██║░░██╗██╔══██║██║░░██║██║██║░░██╗██╔══╝░░
╚██████╔╝██║░░██║███████╗██║░░██║░░░██║░░░  ╚█████╔╝██║░░██║╚█████╔╝██║╚█████╔╝███████╗
░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░  ░╚════╝░╚═╝░░╚═╝░╚════╝░╚═╝░╚════╝░╚══════╝
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


#################################### Global variables ########################################


current_user = ""
end_time = None
start_time = None

#################################### Initial  ########################################


@click.command()
def welcome():
    click.clear()
    click.echo(click.style(
            "\n\n" + (art),
            blink=True,
            bold=True,
            fg="green",
        ))
    click.echo(
        click.style(
            "\n\n" + "                              Welcome to the Sracket CLI!", 
            blink=True,
            bold=True,
            fg="green",
        )
        
    )
    username()


@click.command()
@click.option("--name", prompt=click.style("\n\n\n" + "                         Please enter your name to begin", blink=True,
            bold=True,
            fg="green",
))
def username(name):
    global current_user
    users = session.query(User).all()
    user_names = [n.name for n in users]

#################################### Checks if user exists ########################################


    if not name in user_names:
        new_user = User(name=name)
        current_user = new_user
        session.add(new_user)
        session.commit()
        select_option1()
    elif name in user_names:
        current_user = session.query(User).filter(User.name == name).first()
        if current_user.bike == None:
                select_option3()
        else:
            select_option2()

        
#################################### If does not exist - option 1 ########################################

def select_option1():
    global current_user
    click.clear()
    click.echo(click.style("\n\n\n" + (welcome_user), bold=True, fg="green"))
    click.echo(click.style("\n" + f"                             {current_user.name}!" + "\n\n", bold=True, fg="red",))

    options = ["Rent", "Exit"]
    prompt = click.style("\n\n\n             Would you like to rent a siq bike?"+"\n\n\n" + "                   ", blink=True,
            bold=True,
            fg="green")
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option1(selected_option)


def handle_option1(option):
    if option == "Rent":
        click.clear()
        display_locations()
        enter_locations()
    elif option == "Exit":
        user = session.query(User).filter(User.name == current_user.name).first()
        session.delete(user)
        session.commit()
        click.clear()
        click.echo(click.style((ok_bye),fg="green"))
        # click.echo("\n\n\n" + "See you later!" +"\n\n\n\n")
        
#################################### If does exist and has bike - option 2 ########################################
        

def select_option2():
    global current_user
    click.clear()
    click.echo(click.style("\n" + (welcome_back), bold=True, fg="green"))
    click.echo(click.style("\n" + f"                             {current_user.name}!" + "\n\n", bold=True, fg="red",))
    options = ["I'm done", "More shred"]
    prompt = "\n" + "Are you finished with your ride?, or did you still want to shred???" + "\n\n\n" + "                    "
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option2(selected_option)



def handle_option2(option):
    if option == "I'm done":
        return_bike()
        # return_locations()

    elif option == "More shred":
        click.clear()
        click.echo("\n\n\n\n"+ "        We'll see you when you get back!")

        click.echo(click.style("\n\n\n" +   wheels_up, fg="green"))
        click.echo(click.style("\n" + "             Keep it on two wheels!"+ "\n\n\n", fg="green"))


#################################### If user does exist - option 3 ########################################

def select_option3():
    global current_user
    click.clear()
    click.echo(click.style("\n" + (welcome_back), bold=True, fg="green"))
    click.echo(click.style("\n" + f"                             {current_user.name}!" + "\n\n", bold=True, fg="red",))
    options =["Yes", "Exit"]
    prompt = click.style("\n\n" + "               Would you like to rent a bike today?" + "\n\n\n" + '                       ', fg="green", bold="true")
    selected_option = click.prompt(
        prompt, type=click.Choice(options, case_sensitive=False)
    )
    handle_option3(selected_option)

def handle_option3(option):
    if option == "Yes":
        click.clear()
        display_locations()
        enter_locations()
    elif option == "Exit":
        click.clear()
        click.echo(click.style(ok_bye,fg="green", blink=True))
        # click.echo("\n\n\n" + "See you later!" +"\n\n\n\n")

################## Display locker_locations, Displays Bike table, Handles selections ######################


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
    global start_time
    selected_bike = session.query(Bike).filter(Bike.id == bike_id).first()
    user = session.query(User).filter(User.name == current_user.name).first()
    headers = [selected_bike.id]
    table = tabulate([[selected_bike.name]], headers, tablefmt="mixed_grid")
      # Begin datatime

    start_time = time.ctime()
    datetime_obj = datetime.strptime(start_time, "%a %b %d %H:%M:%S %Y")
    user.start_time = datetime.now()
    session.commit()
    click.clear()
    click.echo(click.style(noble_steed, fg="green"))
    click.echo(click.style((table), bg="bright_green", fg="black", bold=True) + click.style(f"  Your START TIME is: {user.start_time}" + "\n\n\n\n" + "\n\n", fg="green"))
    selected_bike.locker_id = None
    session.commit()
    user.bike = selected_bike.id
    session.commit()
    selected_bike.user_id = user.id
    session.commit()
    click.echo(click.style("           Keep it on two wheels!!!" + "\n\n\n", fg="green"))
    click.echo(click.style(wheels_up + "\n\n\n\n\n", fg="green"))


@click.command()
@click.option(
    "--location_id", prompt="\n\n\n" + "Which location are you renting from today?  Please enter the hub ID", type=int)
def enter_locations(location_id):
    lockers = session.query(Locker).all()
    headers = [l.id for l in lockers]
    locker = [l.locker_location for l in lockers]
    table = tabulate([locker], headers, tablefmt="mixed_grid")
    click.echo(click.style("\n\n\n" + "         " + (table), bg="bright_green", fg="black", bold=True))
    locker = session.query(Locker).filter(Locker.id == location_id).first()
    click.clear()
    display_table(locker)


def display_table(locker):
    click.echo(click.style(bike_locker, fg="green"))
    bikes = [bike.name for bike in locker.bikes if bike.locker_id]
    headers = [b.id for b in locker.bikes]
    table = tabulate([bikes], headers, tablefmt="mixed_grid")
    click.echo(click.style((table), bg="bright_green", fg="black", bold=True) + "\n\n")
    select_bike()

################## Handles returning bike, selecting return locations and datetime end ######################


def return_bike():
    click.clear()
    lockers = session.query(Locker).all()
    headers = [l.id for l in lockers]
    locker = [l.locker_location for l in lockers]
    table = tabulate([locker], headers, tablefmt="mixed_grid")
    click.echo(click.style("\n\n\n\n" + (table), bg="bright_green", fg="black", bold=True))
    return_locations()


@click.command()
@click.option(
    "--location_id", prompt=click.style("\n\n\n" + "Which location are returning your bike to?  Please enter the hub ID",fg="green"), type=int
)
def return_locations(location_id):
    click.clear()
    lockers = session.query(Locker).all()
    headers = [l.id for l in lockers]
    locker = [l.locker_location for l in lockers]
    table = tabulate([locker], headers, tablefmt="mixed_grid")
    locker = session.query(Locker).filter(Locker.id == location_id).first()
    display_bike_to_return(locker)


def display_bike_to_return(locker):
    global end_time
    global start_time
    returned_bike = session.query(Bike).filter(Bike.id == current_user.bike).first()
    user = session.query(User).filter(User.name == current_user.name).first()
    headers = [returned_bike.id]
    table = tabulate([[returned_bike.name]], headers, tablefmt="mixed_grid")
    click.echo(click.style(returning + "\n",fg="green"))
    endtime = time.ctime()
    datetime_obj = datetime.strptime(endtime,"%a %b %d %H:%M:%S %Y" )
    current_user.end_time = datetime_obj
    session.commit()
    # click.echo(f"Start: {current_user.start_time} - End: {current_user.end_time}" + "\n\n" )
    start_datetime = current_user.start_time
    end_datetime = current_user.end_time
    elapsed_timedelta = end_datetime - start_datetime
    elapsed_minutes = elapsed_timedelta.total_seconds() / 60
    click.echo(click.style((table), bg="bright_green", fg="black", bold=True) + f"    YOU STARTED YOUR RIDE AT: {current_user.start_time} - YOU ENDED YOUR RIDE AT: {current_user.end_time}" + "\n\n")
    returned_bike.locker_id = locker.id
    returned_bike.user_id = None
    user.bike = None
    session.commit()

    # Handling datetime


    
    total = round(float(elapsed_minutes * 3.00), 2)
    minutes = round(float(elapsed_minutes), 3)
    click.echo(f"YOUR TOTAL WILL BE ${total} + FOR  {minutes} MINS OF SHREDDING!" + "\n\n\n")
    user.start_time = None
    session.commit()
    user.end_time = None
    session.commit()


if __name__ == "__main__":
    welcome()
