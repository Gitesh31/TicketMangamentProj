import pandas as pd

shows = pd.DataFrame(columns=['Movies','Timeslot','Available Seats','Total Seats'])
totalSeats = 50
availableSeats = totalSeats

def addShows():
    global shows
    global totalSeats
    global availableSeats
    movie = input("Enter the movie name: ")
    timeslot = input("Enter a timeslot: ")
    shows.loc[len(shows)] = [movie,timeslot,availableSeats,totalSeats]
    print(f"Show for {movie} at timeslot {timeslot} is added.")

def showMovies():
    if shows.empty == True:
        print("No Shows Available.")
    else:
        print(f"Available Shows:\n{shows}")

def bookTickets():
    global shows
    global availableSeats
    movie = input("Which movie do you want to book tickets for: ")
    movieShows = shows.loc[shows['Movies'] == movie]
    if not movieShows.empty:
        print(f"Available Timeslots for {movie} are:")
        for i,row in movieShows[['Timeslot','Available Seats']].iterrows():
            print(f"-{i}. {row['Timeslot']} \t Available Seats: {row['Available Seats']} ")
        timeslot = input("Which timeslot do you want to book ticket for: ")
        timeslotSelected = shows.loc[shows['Timeslot'] == timeslot]
        if not timeslotSelected.empty:
            BookedSeats = int(input("How many Seats do you want to book ticket for: "))
            if not (timeslotSelected.loc[timeslotSelected['Available Seats'] > BookedSeats]).empty and availableSeats > BookedSeats:
                availableSeats = availableSeats - BookedSeats
                timeslotSelected.loc[:,'Available Seats'] = availableSeats
                shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot), 'Available Seats'] = availableSeats
                print(f"{BookedSeats} Ticket(s) has been successfully booked for movie \"{movie}\" at timeslot {timeslot}.")
            elif availableSeats == 0:
                print(f"No Tickets Available for {movie} at timeslot {timeslot}.")
            else:
                print(f"{BookedSeats} Seats are not Available for {movie} for selected timeslot {timeslot}.")
        else:
            print(f"Selected timeslot {timeslot} for {movie} is currently not available.")
    else:
        print(f"Sorry {movie} is currently not available.")

def cancelTickets():
    global shows
    global availableSeats
    movie = input("Which movie do you want to cancel tickets for: ")
    timeslot = input(f"Which timeslot for {movie} you want to cancel ticket for: ")
    selectedShow = shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot)]
    CancelledSeats = int(input("How many Tickets do you want to cancel: "))
    if not selectedShow.empty and availableSeats > CancelledSeats:
        availableSeats = availableSeats + CancelledSeats
        shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot), 'Available Seats'] = availableSeats
        print(f"Cancelled {CancelledSeats} Ticket(s) for {movie} at timeslot {timeslot}.")
    else:
        print(f"No ticket for {movie} at timeslot {timeslot}.")

def deleteShows():
    global shows
    movie = input("Which movie do you want to delete: ")
    timeslot = input(f"For which timeslot do you want to delete the show {movie}: ")
    selectedShow = shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot)]
    if not selectedShow.empty:
        shows = shows.drop(selectedShow.index)
        print(f"Deleted Show for {movie} at timeslot {timeslot}.")
    else:
        print(f"Invalid Show \"{movie}\" for timeslot {timeslot}.")

def main():
    try:
        while True:
            print("What do you want to do:")
            print("1. Add Shows")
            print("2. Show Available Shows")
            print("3. Book Tickets")
            print("4. Cancel Tickets")
            print("5. Delete Shows")
            print("6. Save DataFrame as CSV")
            print("7. Exit")
            selectedChoice = input("Enter your choice: ").strip().lower()
            if selectedChoice == "1" or selectedChoice == "add shows":
                addShows()
            elif selectedChoice == "2" or selectedChoice == "show available shows":
                showMovies()
            elif selectedChoice == "3" or selectedChoice == "book tickets":
                bookTickets()
            elif selectedChoice == "4" or selectedChoice == "cancel tickets":
                cancelTickets()
            elif selectedChoice == "5" or selectedChoice == "delete shows":
                deleteShows()
            elif selectedChoice == "6" or selectedChoice == "save dataframe ad csv":
                shows.to_csv("shows.csv",index=False)
            else:
                confirm = input("\n\nDo you want to exit the program: ").strip().lower()
                if confirm == 'yes' or confirm == 'y':
                    break
                else:
                    print('\n')
                    main()
    except KeyboardInterrupt:
        confirm = input("\n\nDo you want to exit the program: ").strip().lower()
        if confirm == 'yes' or confirm == 'y':
            exit()
        else:
            print('\n')
            main()

if __name__ == "__main__":
    main()