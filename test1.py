import numpy as np
import pandas as pd


try:
    shows = pd.read_csv("shows.csv")
    customers = pd.read_csv("customers.csv")
    seats = pd.read_csv("seats.csv")
    shows['Movies'] = shows['Movies'].str.strip().str.lower()
    shows['Timeslot'] = shows['Timeslot'].astype(str).str.strip().str.lower()
except FileNotFoundError:
    shows = pd.DataFrame(columns=['Movies', 'Timeslot', 'Available Seats', 'Total Seats'])
    shows.to_csv("shows.csv", index=False)
    customers = pd.DataFrame(columns=['Name', 'Movie', 'Timeslot', 'Seats Booked','Number of Seats'])
    customers.to_csv("customers.csv", index=False)
    seats = pd.DataFrame(index=['A', 'B', 'C', 'D'], columns=np.arange(1, 11))
    seats.loc[:] = 0
    seats.to_csv("seats.csv", index=False)

totalSeats = seats.size
availableSeats = totalSeats

def customer_booked_seat_countFn(customer):
    global customers
    customer_records = customers[customers["Name"] == customer]
    customer_booked_seatsCount = sum(len(seat.split(",")) for seat in customer_records["Seats Booked"])
    return customer_booked_seatsCount


def bookSeats(row,column):
    if seats.loc[row,column] == 0:
        seats.loc[row,column] = 1
        print(f"Seat is booked for seat number \'{row}{column}\'.")
        seats.to_csv("seats.csv", index=False)
    else:
        print(f"Seat is not available for seat number \'{row}{column}\'.")

def addShows():
    global shows
    global totalSeats
    global availableSeats
    movie = input("Enter the movie name: ").strip().lower()
    timeslot = input("Enter a timeslot: ").strip().lower()
    shows.loc[len(shows)] = [movie,timeslot,availableSeats,totalSeats]
    shows.to_csv("shows.csv",index=False)
    print(f"Show for {movie} at timeslot {timeslot} is added.")

def showData():
    if shows.empty == True:
        print("No Shows Available.")
    else:
        print(f"Available Shows:\n{shows}")
        print(customers)

# Unique seats Df for each movie and timeslot
# Cancelling Tickets

def bookShows():
    global shows
    global customers
    global seats
    global totalSeats
    global availableSeats
    seats.index = ['A','B','C','D']
    cName = input("Enter Name of Customer: ").strip().lower()
    movie = input("Which movie do you want to book tickets for: ").strip().lower()
    movieShows = shows.loc[shows['Movies'] == movie]
    if not movieShows.empty:
        print(f"Available Timeslots for {movie} are:")
        for i, row in movieShows[['Timeslot', 'Available Seats']].iterrows():
            print(f"-{i}. {row['Timeslot']} \t Available Seats: {row['Available Seats']} ")
        timeslot = input("Which timeslot do you want to book ticket for: ").strip().lower()
        timeslotSelected = movieShows.loc[shows['Timeslot'] == timeslot]
        customersSelectedShow = customers.loc[(customers['Name'] == cName) & (customers['Movie'] == movie)
                                              & (customers['Timeslot'] == timeslot)]
        if not timeslotSelected.empty:
            print(customersSelectedShow)
            print(customersSelectedShow.empty)
            print(seats)
            bookedSeat = input("Enter Seat Number that you want to book: ").strip().upper()
            bookedSeatLocation = list(bookedSeat)
            try:
                bookSeats(bookedSeatLocation[0], bookedSeatLocation[1])
            except KeyError:
                print(f"{bookedSeat} doesn't exit.")
                main()
            if not customersSelectedShow.empty:
                selectedShowIndex = customersSelectedShow.index[0]
                print(selectedShowIndex)
                customer_booked_seat_count = customer_booked_seat_countFn(cName)
                CustomerBookedSeats = customers.at[selectedShowIndex, "Seats Booked"]
                customers.at[selectedShowIndex, "Seats Booked"] = f"{CustomerBookedSeats},{bookedSeat}"
                customers.at[selectedShowIndex,"Number of Seats"] = customer_booked_seat_count
                customers.to_csv("customers.csv", index=False)
            else:
                customer_booked_seat_count = 1
                newCustomer = {"Name": cName, "Movie": movie, "Timeslot": timeslot, "Seats Booked":bookedSeat,
                               "Number of Seats": customer_booked_seat_count}
                customers = pd.concat([customers, pd.DataFrame([newCustomer])], ignore_index=True)
                customers.to_csv("customers.csv", index=False)
            availableSeats = totalSeats
            customer_booked_seats_total = seats.values.sum()
            availableSeats = availableSeats - customer_booked_seats_total
            shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot), 'Available Seats'] = availableSeats
        else:
            print(f"Selected timeslot {timeslot} for {movie} is currently not available.")
    else:
        print(f"Sorry {movie} is currently not available.")


def cancelTickets():
    global shows
    global availableSeats
    movie = input("Which movie do you want to cancel tickets for: ").strip().lower()
    timeslot = input(f"Which timeslot for {movie} you want to cancel ticket for: ").strip().lower()
    selectedShow = shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot)]
    cancelledSeats = int(input("How many Tickets do you want to cancel: "))
    if not selectedShow.empty and availableSeats > cancelledSeats:
        availableSeats = availableSeats + cancelledSeats
        shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot), 'Available Seats'] = availableSeats
        shows.to_csv("shows.csv", index=False)
        print(f"Cancelled {cancelledSeats} Ticket(s) for {movie} at timeslot {timeslot}.")
    elif cancelledSeats > availableSeats:
        print("Invalid Number of Tickets.")
    else:
        print(f"No ticket found booked for {movie} at timeslot {timeslot}.")

def deleteShows():
    global shows
    movie = input("Which movie do you want to delete: ").strip().lower()
    timeslot = input(f"For which timeslot do you want to delete the show {movie}: ").strip().lower()
    selectedShow = shows.loc[(shows['Movies'] == movie) & (shows['Timeslot'] == timeslot)]
    if not selectedShow.empty:
        shows = shows.drop(selectedShow.index)
        shows.to_csv("shows.csv", index=False)
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
            print("6. Exit")
            selectedChoice = input("Enter your choice: ").strip().lower()
            if selectedChoice == "1" or selectedChoice == "add shows":
                addShows()
            elif selectedChoice == "2" or selectedChoice == "show available shows":
                showData()
            elif selectedChoice == "3" or selectedChoice == "book tickets":
                bookShows()
            elif selectedChoice == "4" or selectedChoice == "cancel tickets":
                cancelTickets()
            elif selectedChoice == "5" or selectedChoice == "delete shows":
                deleteShows()
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
