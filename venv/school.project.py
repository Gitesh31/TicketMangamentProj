import pandas as pd

while True:
    print("what do you want to do:")
    print("1.add electronic item")
    print("2.add customer details")
    print("3.update purchased items")
    print("4.show recent electronic item order")
    print("5.delete item")
    print("6.exit")
    select_choice=input("enter choice: ")
    if select_choice=="1":
        try:
            stock=pd.read_csv("stock.csv")
        except FileNotFoundError:
            stock=pd.DataFrame(columns=['Item','Quantity','Price per Item'])
            stock.to_csv("stock.csv",index=False)
        u_item=input('enter electronic item: ')
        stock_quantity=int(input('enter quantity: '))
        u_price=input('enter price: ')
        stock.loc[len(stock)]=[u_item,stock_quantity,u_price]
        stock.to_csv("stock.csv",index=False)
        print(f'{u_item} and details are added.')
    elif select_choice=="2":
        try:
            customers=pd.read_csv("customers.csv")
        except FileNotFoundError:
            customers=pd.DataFrame(columns=['Customer','Item','Quantity','City'])
            customers.to_csv("customers.csv",index=False)
        u_name=input("enter customer name: ")
        u_item=input('enter electronic item: ')
        u_city=input('enter city: ')
        customers_purchased_quantity=0
        customers.loc[len(customers)] = [u_name, u_item, customers_purchased_quantity, u_city]
        customers.to_csv("customers.csv",index=False)
        print(f'{u_name} and their order details are added.')
    elif select_choice=="3":
        try:
            stock=pd.read_csv("stock.csv")
            customers=pd.read_csv("customers.csv")
        except FileNotFoundError:
            customers=pd.DataFrame(columns=['Customer','Item','Quantity','City'])
            customers.to_csv("customers.csv",index=False)
            stock = pd.DataFrame(columns=['Item', 'Quantity', 'Price per Item'])
            stock.to_csv("stock.csv", index=False)
        u_item=input("enter item name: ")
        u_name=input("enter customer who purchased this item: ")
        u_quantity=int(input("enter quantity of items purchased: "))
        selected_item=stock.loc[stock['Item']==u_item]
        stock_quantity = stock.at[selected_item.index,'Quantity']
        customers_purchased_quantity=selected_item['Quantity']
        if selected_item.empty==False:
            if u_quantity<=stock_quantity:
                stock_quantity = stock_quantity - u_quantity
                customers_purchased_quantity = customers_purchased_quantity + u_quantity
                stock.loc[selected_item.index,'Quantity']=[stock_quantity]
                customers.loc[selected_item.index,'Quantity']=[customers_purchased_quantity]
                stock.to_csv("stock.csv",index=False)
                customers.to_csv("customers.csv",index=False)
                print("Data of Purchase has been added.")
            else:
                print(f"Not enough {u_item}s are available for purchase currently.")
        else:
            print(f"{u_item} is not available for purchase currently.")
    elif select_choice=="4":
        try:
            stock=pd.read_csv("stock.csv")
            customers=pd.read_csv("customers.csv")
        except FileNotFoundError:
            stock=pd.DataFrame(columns=['Item','Quantity','Price','City'])
            stock.to_csv("stock.csv",index=False)
            customers=pd.DataFrame(columns=['Customer','Item','Quantity','City'])
            customers.to_csv("customers.csv",index=False)
        if stock.empty==True:
            print('no items available.')
        else:
            print(stock,'\n')
            print(customers,'\n')
    elif select_choice=="5":
        try:
            stock=pd.read_csv("stock.csv")
            customers = pd.read_csv("customers.csv")
        except FileNotFoundError:
            stock=pd.DataFrame(columns=['Item','Quantity','Price','City'])
            stock.to_csv("stock.csv",index=False)
            customers = pd.DataFrame(columns=['Customer', 'Item', 'Quantity', 'City'])
            customers.to_csv("customers.csv", index=False)
        u_item=input('Name the item which is to be deleted:')
        selected_item=stock.loc[stock['Item']==u_item]
        if selected_item.empty==False:
            stock=stock.drop(selected_item.index)
            customers=customers.drop(selected_item.index)
            stock.to_csv("stock.csv",index=False)
            customers.to_csv("customers.csv",index=False)
            print(f"{u_item} and its details are deleted.")
        else:
            print(f"{u_item} doesn't exist in data.")
    else:
        break
