import mysql.connector
# Establish connection to MySQL
mydb = mysql.connector.connect(
 host="localhost",
 user="root",
 password="shakeel@111",
 database="new1"
)
# Create a cursor object to execute SQL queries
cursor = mydb.cursor()
# Function to create electricity_bill table
def create_table():
    create_query = """
    CREATE TABLE IF NOT EXISTS electricity_bill (
    Tariff_Code VARCHAR(5) NOT NULL, 
    Customer_Name VARCHAR(255) NOT NULL,
    Meter_Number INT AUTO_INCREMENT PRIMARY KEY,
    Previous_Reading INT,
    Current_Reading INT, 
    Units_Consumed INT,
    Bill_Amount FLOAT
    )
    """
    cursor.execute(create_query)
    mydb.commit()
    print("Table electricity_bill created successfully")
# Function to insert customer details
def insert_customer_details(cursor, Tariff_Code, Customer_Name):
    query = """INSERT INTO electricity_bill (Tariff_Code, Customer_Name) 
    VALUES (%s, %s)""" #multi-line query
    val = (Tariff_Code, Customer_Name)
    cursor.execute(query, val)
    mydb.commit()
    print("Customer details inserted successfully")
# Function to display details of a specific customer
def display_customer_details(cursor, Meter_Number):
    query = "SELECT * FROM electricity_bill WHERE Meter_Number = %s"
    cursor.execute(query, (Meter_Number,)) 
    result = cursor.fetchone()
    if result:
        print("Customer Details:")
        print("-------------------------------")
        print("TariffCode : ", result[0])
        print("Customer-Name : ", result[1])
        print("Meter-Number : ", result[2])
        print("Previous-Reading: ", result[3])
        print("Current-Reading: ", result[4])
        print("-------------------------------")
    else:
        print("Customer not found!")
# Function to update customer details by Meter Number
def update_customer_details(cursor, Meter_Number, Previous_Reading, 
Current_Reading):
    query = """
    UPDATE electricity_bill
    SET Previous_Reading = %s, Current_Reading = %s
    WHERE Meter_Number = %s
    """
    val = (Previous_Reading, Current_Reading, Meter_Number)
    cursor.execute(query, val)
    mydb.commit()
    print("Customer details updated successfully")
# Function to display all employee details from the database
def display_all_customer_details(cursor):
    query = "select * from electricity_bill"
    cursor.execute(query)
    results = cursor.fetchall()
    if results:
        print("All Customers' details")
        print("-------------------------------")
        for result in results:
            print("TariffCode : ", result[0])
            print("Customer-Name : ", result[1])
            print("Meter-Number : ", result[2])
            print("Previous-Reading: ", result[3])
            print("Current-Reading: ", result[4])
            print("-------------------------------")
        else:
            print("No records found!")
#Function to delete all records from database
def delete_table(cursor):
    query = "drop table electricity_bill"
    cursor.execute(query)
    mydb.commit()
    print("All records successfully deleted")
#Function to calculate bill amount from database
def calculate_bill_amt(cursor, Meter_Number):
    query = "SELECT * FROM electricity_bill WHERE Meter_Number = %s"
    cursor.execute(query, (Meter_Number,)) 
    result = cursor.fetchone()
    if result:
        print("Customer Details:")
        print("-------------------------------")
        print("TariffCode: ", result[0])
        print("Customer-Name : ", result[1])
        print("Previous-Reading: ", result[3])
        print("Current-Reading: ", result[4])
        if(result[3]==None and result[4]==None):
            print("Previous and current readings not updated")
            return
        units_consumed=result[4]-result[3]
        print("Units-Consumed: ", units_consumed)
        if(result[0]=='LT1'):
            if(units_consumed>=0 and units_consumed<=30):
                bill_amt =units_consumed*2
            if (units_consumed >= 31 and units_consumed <= 100):
                bill_amt =units_consumed*3.5
            if (units_consumed >= 101 and units_consumed <= 200):
                bill_amt =units_consumed*4.5
            if (units_consumed >200):
                bill_amt =units_consumed*5
            print("Bill-Amount: Rs. ", bill_amt)
        elif (result[0] == 'LT2'):
            if (units_consumed >= 0 and units_consumed <= 30):
                bill_amt = units_consumed * 3.5
            if (units_consumed >= 31 and units_consumed <= 100):
                bill_amt = units_consumed * 5.0
            if (units_consumed >= 101 and units_consumed <= 200):
                bill_amt = units_consumed * 6.0
            if (units_consumed > 200):
                bill_amt = units_consumed * 7.5
            print("Bill-Amount: Rs. ", bill_amt)
        query = """
        UPDATE electricity_bill
        SET Units_Consumed = %s, Bill_Amount = %s
        WHERE Meter_Number = %s
        """
        val = (units_consumed, bill_amt, Meter_Number)
        cursor.execute(query, val)
        mydb.commit()
        print("Customer bill updated successfully")
    else:
        print("Customer not found!")
# Main function
def main():
    create_table()
 #menu; loops infintely till you choose to exit
    while True:
        print("\n1. Insert Customer-Details")
        print("2. Display Customer-Details by Meter-Number")
        print("3. Update Customer-Details by Meter-Number")
        print("4. Display all Customer Details")
        print("5. Calculate Bill for a customer")
        print("6. Delete table permanently")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            Customer_Name=input("Enter customer name: ")
            while True:
                Tariff_Code = input("Enter Tariff-Code(LT1/LT2): ")
                if (Tariff_Code == "LT1"):
                    insert_customer_details(cursor, Tariff_Code, Customer_Name)
                    break
                elif (Tariff_Code=="LT2"):
                    insert_customer_details(cursor, Tariff_Code, Customer_Name)
                    break
                else:
                    print("Invalid tariff code! Enter as LT1 or LT2")
        elif choice == '2':
            Meter_Number = int(input("Enter Meter-Number of the customer: "))
            display_customer_details(cursor, Meter_Number)
        elif choice == '3':
            Meter_Number = input("Enter Meter-Number: ")
            while True:
                Previous_Reading = int(input("Enter Previous Reading: "))
                Current_Reading = int(input("Enter Current Reading: "))
                if(Current_Reading<Previous_Reading):
                    print("Current reading needs to be greater than or equal to  previous reading") 
                else:
                    break
            update_customer_details(cursor, Meter_Number, Previous_Reading, 
Current_Reading)
        elif choice == '4':
            display_all_customer_details(cursor)
        elif choice == '5':
            Meter_Number = int(input("Enter Meter-Number of the customer: "))
            calculate_bill_amt(cursor, Meter_Number)
        elif choice == '6':
            ans=input("Are you absolutely sure? (y/n): ")
            if(ans=='y'):
                delete_table(cursor)
                quit = input("Terminating program.....(press any key)")
                break
            else:
                continue
        elif choice == '7':
            break
        else:
            print("Invalid choice! Please try again.")
 # Closing connection
cursor.close()
mydb.close()
if __name__== "main":
    main()