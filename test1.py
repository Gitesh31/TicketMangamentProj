import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

try:
    shows = pd.read_csv("shows.csv")
    shows['Movie'] = shows['Movie'].str.strip().str.lower()
    shows['Timeslot'] = shows['Timeslot'].astype(str).str.strip().str.lower()
except FileNotFoundError:
    shows = pd.DataFrame(columns=['Movie', 'Timeslot', 'Available Seats', 'Total Seats','Ticket Price'])
    shows.to_csv("shows.csv", index=False)

try:
    customers = pd.read_csv("customers.csv")
except FileNotFoundError:
    customers = pd.DataFrame(columns=['Name', 'Movie', 'Timeslot', 'Seats Booked', 'Number of Seats'])
    customers.to_csv("customers.csv", index=False)

def timeslot_formatting(date_str,time_str):
    date_str = date_str.strip().replace("/", "-")
    time_str = time_str.strip()
    time_formats = ['%H:%M', '%H-%M']
    date_formats = ['%d-%m-%Y', '%Y-%m-%d']
    formatted_date = None
    for fmt in date_formats:
        try:
            date_obj = datetime.datetime.strptime(date_str, fmt)
            formatted_date = date_obj.strftime('%d-%m-%Y')
            break
        except ValueError:
            continue
    if not formatted_date:
        print("Invalid Date Format.\nCorrect Formats:\n1.DD-MM-YYYY\n2.YYYY-MM-DD\n")
        main()
    formatted_time = None
    for fmt in time_formats:
        try:
            time_obj = datetime.datetime.strptime(time_str, fmt)
            formatted_time = time_obj.strftime('%H:%M')
            break
        except ValueError:
            continue
    if not formatted_time:
        print('Invalid Time Format.\nCorrect Formats:\n1. HH:MM\n2. HH-MM\n')
        main()
    timeslot = f"{formatted_date} {formatted_time}"
    return timeslot

def show_init(movie, timeslot,rows = np.random.randint(4,10),columns = np.random.randint(4,10)):
    filename = f"{movie}_{timeslot}_seats".replace(' ','_').replace(':','-')
    try:
        seats_df = pd.read_csv(f"{filename}.csv")
    except FileNotFoundError:
        seats_df = pd.DataFrame(0,index=[chr(65 + row) for row in range(rows)],
                                columns=[str(col + 1) for col in range(columns)])
        seats_df.to_csv(f"{filename}.csv",index=False)

    return seats_df

def customer_booked_seat_countFn(cName, movie, timeslot):
    global customers
    customersSelectedShow = customers.loc[(customers['Name'] == cName) & (customers['Movie'] == movie)
                                          & (customers['Timeslot'] == timeslot)]
    customer_booked_seatsCount = sum(len(seat.split(",")) for seat in customersSelectedShow["Seats Booked"])
    return customer_booked_seatsCount


def bookSeats(movie,timeslot,row, column):
    seats_df = show_init(movie,timeslot)
    seats_df.index = [chr(65 + row) for row in range(len(seats_df.index))]
    filename = f"{movie}_{timeslot}_seats".replace(' ','_').replace(':','-')
    if seats_df.loc[row, column] == 0:
        seats_df.loc[row, column] = 1
        print(f"Seat is booked for seat number \'{row}{column}\'.")
        seats_df.to_csv(f"{filename}.csv", index=False)
    else:
        print(f"Seat is not available for seat number \'{row}{column}\'.")

def cancelSeats(movie,timeslot,row, column):
    seats_df = show_init(movie,timeslot)
    seats_df.index = [chr(65 + row) for row in range(len(seats_df.index))]
    filename = f"{movie}_{timeslot}_seats".replace(' ','_').replace(':','-')
    if seats_df.loc[row, column] == 1:
        seats_df.loc[row, column] = 0
        seats_df.to_csv(f"{filename}.csv", index=False)
    else:
        print(f"Seat \'{row}{column}\' is not booked..")

def addShows():
    global shows
    movie = input("Enter the movie name: ").strip().lower()
    date_str = input("Enter the date of movie airing (DD-MM-YYYY or YYYY-MM-DD): ")
    time_str = input("Enter the time of movie airing (HH:MM or HH-MM): ")
    timeslot = timeslot_formatting(date_str,time_str)
    ticket_price = input("Enter Ticket Price: ")
    ticket_price = int(ticket_price)
    seats_df = show_init(movie, timeslot)
    totalSeats = seats_df.size
    availableSeats = totalSeats
    shows.loc[len(shows)] = [movie, timeslot, availableSeats, totalSeats,ticket_price]
    shows.to_csv("shows.csv", index=False)
    print(f"Show for {movie} at timeslot {timeslot} is added.")

def showData():
    global shows
    global customers
    if shows.empty:
        print("No Shows Available.")
    elif shows.empty == False and customers.empty == True:
        print(f"Available Shows:\n{shows}")
    else:
        print(f"Available Shows:\n{shows}")
        print(f"Customer Data:\n{customers}")


def bookShows():
    global shows
    global customers
    cName = input("Enter Name of Customer: ").strip().lower()
    movie = input("Which movie do you want to book tickets for: ").strip().lower()
    movieShows = shows.loc[shows['Movie'] == movie]
    if not movieShows.empty:
        print(f"Available Timeslots for {movie} are:")
        for i, row in movieShows[['Timeslot', 'Available Seats']].iterrows():
            print(f"-{i}. {row['Timeslot']} \t Available Seats: {row['Available Seats']} ")
        timeslot = input("Which timeslot do you want to book ticket for: ").strip().lower()
        timeslotSelected = movieShows.loc[shows['Timeslot'] == timeslot]
        customersSelectedShow = customers.loc[(customers['Name'] == cName) & (customers['Movie'] == movie)
                                              & (customers['Timeslot'] == timeslot)]
        if not timeslotSelected.empty:
            seats_df = show_init(movie, timeslot)
            seats_df.index = [chr(65 + row) for row in range(len(seats_df.index))]
            print(seats_df)
            bookedSeat = input("Enter Seat Number that you want to book: ").strip().upper()
            try:
                bookSeats(movie,timeslot,bookedSeat[0], bookedSeat[1])
            except KeyError:
                print(f"{bookedSeat} doesn't exit.")
                main()
            if not customersSelectedShow.empty:
                selectedShowIndex = customersSelectedShow.index[0]
                customer_booked_seat_count = customer_booked_seat_countFn(cName, movie, timeslot) + 1
                CustomerBookedSeats = customers.at[selectedShowIndex, "Seats Booked"]
                customers.at[selectedShowIndex, "Seats Booked"] = f"{CustomerBookedSeats},{bookedSeat}"
                customers.at[selectedShowIndex, "Number of Seats"] = customer_booked_seat_count
                customers.to_csv("customers.csv", index=False)
            else:
                customer_booked_seat_count = 1
                newCustomer = {"Name": cName, "Movie": movie, "Timeslot": timeslot, "Seats Booked": bookedSeat,
                               "Number of Seats": customer_booked_seat_count}
                customers = pd.concat([customers, pd.DataFrame([newCustomer])], ignore_index=True)
                customers.to_csv("customers.csv", index=False)
            seats_df = show_init(movie, timeslot)
            totalSeats = seats_df.size
            bookedSeats = seats_df.values.sum()
            availableSeats = totalSeats - bookedSeats
            shows.loc[(shows['Movie'] == movie) & (shows['Timeslot'] == timeslot), 'Available Seats'] = availableSeats
            shows.to_csv("shows.csv", index=False)
        else:
            print(f"Selected timeslot {timeslot} for {movie} is currently not available.")
    else:
        print(f"Sorry {movie} is currently not available.")


def cancelTickets():
        global shows
        global customers
        cName = input("Enter Name of Customer: ").strip().lower()
        selectedCustomer = customers.loc[customers['Name'] == cName]
        if not selectedCustomer.empty:
            movie = input("Which movie do you want to cancel tickets for: ").strip().lower()
            timeslot = input(f"Which timeslot of {movie} do you want to cancel: ").strip().lower()
            showSelected = shows.loc[(shows['Movie'] == movie) & (shows['Timeslot'] == timeslot)]
            if not showSelected.empty:
                customersSelectedShow = customers.loc[(customers['Name'] == cName) & (customers['Movie'] == movie)
                                                      & (customers['Timeslot'] == timeslot)]
                if not customersSelectedShow.empty:
                    selectedShowIndex = customersSelectedShow.index[0]
                    seatsBooked = customers.at[selectedShowIndex, "Seats Booked"]
                    bookedSeatsList = seatsBooked.split(",") if seatsBooked else []
                    if bookedSeatsList:
                        print(f"Your booked seats are: {', '.join(bookedSeatsList)}")
                        bookedSeat = input("Enter Seat Number that you want to cancel: ").strip().upper()
                        if bookedSeat in bookedSeatsList:
                            cancelSeats(movie,timeslot,bookedSeat[0],bookedSeat[1])
                            bookedSeatsList.remove(bookedSeat)
                            updatedSeats = ",".join(bookedSeatsList)
                            customers.at[selectedShowIndex, "Seats Booked"] = updatedSeats
                            customers.at[selectedShowIndex, "Number of Seats"] = len(bookedSeatsList)
                            if len(bookedSeatsList) == 0:
                                customers = customers.drop(index=selectedShowIndex)
                            customers.to_csv("customers.csv", index=False)
                            seats_df = show_init(movie,timeslot)
                            totalSeats = seats_df.size
                            bookedSeats = seats_df.values.sum()
                            availableSeats = totalSeats - bookedSeats
                            shows.loc[(shows['Movie'] == movie) & (shows['Timeslot'] == timeslot), "Available Seats"] = availableSeats
                            shows.to_csv("shows.csv", index=False)
                            print(f"Seat {bookedSeat} has been canceled successfully.")
                        else:
                            print(f"You have not booked seat {bookedSeat}.")
                    else:
                        print("You have no seats booked for this show.")
                else:
                    print(f"No tickets found for {cName} for {movie} at {timeslot}.")
            else:
                print("Invalid Show.")
        else:
            print(f"{cName} not found.")


def deleteShows():
    global shows
    movie = input("Which movie do you want to delete: ").strip().lower()
    timeslot = input(f"For which timeslot do you want to delete the show {movie}: ").strip().lower()
    selectedShow = shows.loc[(shows['Movie'] == movie) & (shows['Timeslot'] == timeslot)]
    if not selectedShow.empty:
        filename = f"{movie}_{timeslot}_seats".replace(' ', '_').replace(':', '-')
        shows.drop(selectedShow.index,inplace=True)
        shows.to_csv("shows.csv",index=False)
        os.remove(f"{filename}.csv")
        print(f"Deleted Show for {movie} at timeslot {timeslot}.")
    else:
        print(f"Invalid Show \"{movie}\" for timeslot {timeslot}.")

def plotGraphs():
    global shows
    global customers
    merged_df = shows.merge(customers, on=['Movie', 'Timeslot'])
    if not shows.empty:
        print("Select a Choice:")
        print("1. Revenue by Movie")
        print("2. Movie Popularity")
        print("3. Revenue Graph for a Particular Movie")
        print("4. Daily Revenue")
        ch = input("Enter Choice: ").strip().lower()
        if ch == '1' or ch == 'revenue by movie':
            merged_df['Revenue'] = merged_df['Number of Seats'] * merged_df['Ticket Price']
            merged_df['Normalized Revenue'] = merged_df.groupby('Movie')['Revenue'].transform(lambda x: x/x.sum())
            movie_revenue = merged_df.groupby('Movie')['Revenue'].sum()
            normalized_movie_revenue = merged_df.groupby('Movie')['Normalized Revenue'].sum()
            plt.figure(figsize=(10, 6))
            cmap = mpl.colormaps['Pastel1']
            ch2 = input("1. Raw Revenue Graph\n2. Normalized Revenue Graph\nEnter your Choice: ")
            if ch2 == '1' or ch == 'raw revenue graph':
                plt.bar(movie_revenue.index, movie_revenue.values, color=cmap(range(len(movie_revenue))))
            elif ch2 == '2' or ch == 'normalized revenue graph':
                plt.bar(normalized_movie_revenue.index, normalized_movie_revenue.values, color=cmap(range(len(movie_revenue))))
            else:
                print("Invalid Choice.")
                main()
            print("Revenue by Movie:")
            plt.xlabel('Movie', fontsize=12, color='#333333')
            plt.ylabel('Revenue', fontsize=12, color='#333333')
            plt.xticks(rotation=45, color='#333333')
            plt.yticks(color='#333333')
            plt.tight_layout()
            ch1 = input("Do you want to save Figure: ").strip().lower()
            if ch1 == 'y' or ch1 == 'yes':
                imgName = input("Enter Plot Name: ")
                plt.savefig(f"{imgName}.png")
            plt.show()

        elif ch == '2' or ch == 'movie popularity':
            tickets_sold = merged_df.groupby('Movie')['Number of Seats'].sum()
            plt.figure(figsize=(10, 6))
            cmap = mpl.colormaps['Set2']
            plt.bar(tickets_sold.index, tickets_sold.values, color=cmap(range(len(tickets_sold))))
            plt.xlabel('Movie', fontsize=12, color='#333333')
            plt.ylabel('Tickets Sold', fontsize=12, color='#333333')
            plt.title('Tickets Sold by Movie', fontsize=16, color='#333333')
            plt.xticks(rotation=45, color='#333333')
            plt.yticks(color='#333333')
            plt.tight_layout()
            ch1 = input("Do you want to save Figure: ").strip().lower()
            if ch1 == 'y' or ch1 == 'yes':
                imgName = input("Enter Plot Name: ")
                plt.savefig(f"{imgName}.png")
            plt.show()

        elif ch == '3' or ch == 'revenue graph for a particular movie':
            movie = input("Enter the movie you want to see data for: ")
            movie_data = merged_df[merged_df['Movie'] == movie].copy()
            if movie_data.empty:
                print(f"No data available for the movie: {movie}")
                return
            movie_data.loc[:, 'Revenue'] = movie_data['Number of Seats'] * movie_data['Ticket Price']
            plt.figure(figsize=(10, 6))
            movie_data.plot(x='Timeslot', y='Revenue', kind='line', marker='o',color = 'c')
            plt.title(f'Revenue for {movie}', fontsize=16, color='#333333')
            plt.xlabel('Timeslot', fontsize=12, color='#333333')
            plt.ylabel('Revenue', fontsize=12, color='#333333')
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            ch1 = input("Do you want to save Figure: ").strip().lower()
            if ch1 == 'y' or ch1 == 'yes':
                imgName = input("Enter Plot Name: ")
                plt.savefig(f"{imgName}.png")
            plt.show()

        elif ch == '4' or ch == 'daily revenue':
            timeslots = pd.to_datetime(merged_df['Timeslot'], format="%d-%m-%Y %H:%M")
            merged_df['Date'] = timeslots.dt.date
            merged_df['Revenue'] = merged_df['Number of Seats'] * merged_df['Ticket Price']
            dailyRevenue = merged_df.groupby('Date')['Revenue'].sum()
            plt.figure(figsize=(12, 6))
            plt.plot(dailyRevenue.index, dailyRevenue.values, color= 'lime',marker = 'o')
            plt.title('Daily Revenue', fontsize=16, color='#333333')
            plt.xlabel('Date', fontsize=12, color='#333333')
            plt.ylabel('Revenue', fontsize=12, color='#333333')
            plt.grid(True)
            plt.xticks(rotation=45, color='#333333')
            plt.yticks(color='#333333')
            plt.tight_layout()
            ch1 = input("Do you want to save Figure: ").strip().lower()
            if ch1 == 'y' or ch1 == 'yes':
                imgName = input("Enter Plot Name: ")
                plt.savefig(f"{imgName}.png")
            plt.show()
        else:
            print("Invalid choice.\nPlease select a valid option.")
    else:
        print("No Data Available to Plot.")

def main():
    try:
        while True:
            print("Select a Choice:")
            print("1. Add Shows")
            print("2. Show Data")
            print("3. Book Tickets")
            print("4. Cancel Tickets")
            print("5. Delete Shows")
            print("6. Show Graph")
            print("7. Exit")
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
            elif selectedChoice == "6" or selectedChoice == "show graph":
                plotGraphs()
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
