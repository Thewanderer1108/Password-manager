# this is a password manager Python script that will help users save and view their passwords
import mysql.connector      # used to connect to the MySQL database
import time     # use to generate data time values
import sys      # used to call the exit function to exit the application
import os       # used to clear the console
import getpass      # used to get the password from the user without echoing it to the screen


def console_clear():
    os.system("cls")


def current_time():
    cr_date = time.strftime("%Y-%m-%d %H:%M:%S")
    return cr_date


def connection():
    con = mysql.connector.connect(host='localhost', database='pa_manager', user='root', password='Test@123',
                                  connection_timeout=180)
    return con


def save_password(acc_id):
    """
    This function is used to save passwords into the database.

    :parameter
        n, acc_type, u_id, pw, these are variables that this functions uses to accordingly
        insert values in the database. We used getpass() function here to get the password
        from the user without echoing it on the screen for better security.
        cr, ch are variables that call the current time function to generate a datetime value
        as required in the database.

        The acc_id here is a variable that stores the id of the user logged in so that the
        program remembers the user throughout the entire operation of the program.

        Note: getpass() does not work with most IDE or editors. Hence, have to run the
        application from the CMD.

        we call the connection() function every time we need a connection to the database

    """

    s_con = connection()
    try:
        n = input("Enter your full name: ")
        acc_type = input("Enter account type(Gmail, Apple etc): ")
        u_id = input("Enter Account User ID: ")
        pw = getpass.getpass("Enter Account Password: ")
        cr = current_time()
        ch = current_time()
        insert_query = 'insert into info(name, account_type, user_ID, passwrd, creation_date, change_date, U_ID)' \
                       ' values(%s, %s, %s, %s, %s, %s, %s)'
        insert_cursor = s_con.cursor()
        insert_cursor.execute(insert_query, (n, acc_type, u_id, pw, cr, ch, acc_id))
        s_con.commit()
        print("{} record added successfully".format(insert_cursor.rowcount))
        print()
        print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password\n5.View All Password"
              "\n6.View All Account Types")
        print()
        print("Select option above to continue(or type exit to quit)")
        insert_cursor.close()
    except mysql.connector.Error as error:
        print("Problem saving record, {}".format(error))
        s_con.rollback()
        sys.exit()      # this exits the application
    finally:
        if s_con.is_connected():
            s_con.close()


def update_password(acc_id):
    """
    This function is used to update the password of a stored account in the database

    :parameter
        variables like acc_type, user_name, new_pw, ch_dt are variables that again is used
        to update the existing values in the database.

        The acc_id here is a variable that stores the id of the user logged in so that the
        program remembers the user throughout the entire operation of the program.

        Note: Here we used getpass() function as well. Just like the above note, getpass()
        works if we run the application in CMD and does not work in IDE and editors.

        we call the connection() function every time we need a connection to the database.
    """
    u_con = connection()
    try:
        acc_type = input("Enter Account type for which password needs to be changed: ")
        user_name = input("Enter Account user ID: ")
        new_pw = getpass.getpass("Enter new password: ")
        ch_dt = current_time()
        update_query = "update info set passwrd = %s, change_date = %s where user_ID = %s and account_type = %s and " \
                       "U_ID = %s"
        update_cursor = u_con.cursor()
        update_cursor.execute(update_query, (new_pw, ch_dt, user_name, acc_type, acc_id))
        u_con.commit()      # this commits the changes in the database
        print("{} account password successfully changed".format(update_cursor.rowcount))
        print()
        print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password\n5.View All Password"
              "\n6.View All Account Types")
        print()
        print("Select options to continue or type exit to quit")
        update_cursor.close()
    except mysql.connector.Error as error:
        print("Problem saving record, {}".format(error))
        u_con.rollback()
        sys.exit()      # this exits the application
    finally:
        if u_con.is_connected():
            u_con.close()


def delete_account(acc_id):
    """
    This function is used to delete the record from the database.

    :parameter
        variables like acc_type, pw is used to delete an existing record from the database.
        Here, we ask the user to input the password of the given account again and ask the
        question as to he/she is sure to delete it, for security purposes and to prevent any
        incorrect selection of options.

       The acc_id here is a variable that stores the id of the user logged in so that the
       program remembers the user throughout the entire operation of the program.

       Note: Here we used getpass() function as well. Just like the above note, getpass()
       works if we run the application in CMD and does not work in IDE and editors.

       we call the connection() function every time we need a connection to the database.
    """
    d_con = connection()
    try:
        acc_type = input("Enter account type: ")
        pw = getpass.getpass("Enter account password: ")
        answer = input("Are you sure you want to delete the account(y/n): ")
        if answer == 'y' or answer == 'Y':
            delete_query = 'delete from info where account_type = %s and passwrd = %s and U_ID = %s'
            delete_cursor = d_con.cursor()
            delete_cursor.execute(delete_query, (acc_type, pw, acc_id))
            d_con.commit()      # this commits the changes in the database
            print("{} record deleted successfully".format(delete_cursor.rowcount))
            print()
            print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password"
                  "\n5.View All Password\n6.View All Account Types")
            print()
            print("Select options to continue or type exit to quit")
            delete_cursor.close()
        else:
            print("No changes made, no account deleted")
            print()
            print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password"
                  "\n5.View All Password\n6.View All Account Types")
            print()
            print("Select options to continue or type exit to quit")
    except mysql.connector.Error as error:
        print("Problem deleting record, {}".format(error))
        d_con.rollback()
        sys.exit()  # this exits the application
    finally:
        if d_con.is_connected():
            d_con.close()


def view_password(acc_id):
    """
    This function is used to view the existing passwords the user has saved in the database.

    :parameter
        If a user has 2 gmail account passwords store in the database. Both the 2 accounts will
        be printed out if the account type was entered as gmail(for example).

        The acc_id here is a variable that stores the id of the user logged in so that the
        program remembers the user throughout the entire operation of the program.

        we call the connection() function every time we need a connection to the database

    """
    v_con = connection()
    try:
        a_type = input("Enter account type: ")
        print()
        select_query = 'select name, account_type, user_ID, passwrd from info where account_type = %s and U_ID = %s'
        select_cursor = v_con.cursor()
        select_cursor.execute(select_query, (a_type, acc_id))
        for name, account_type, user_ID, passwrd in select_cursor:
            print("\t Name: {}\n\t Account: {} \n\t User ID: {} \n\t Password: {}".format(name, account_type, user_ID,
                                                                                          passwrd))
            # print("\t *" * 11)
            print()
        select_cursor.close()
        print()
        print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password\n5.View All Password"
              "\n6.View All Account Types")
        print()
        print("Select options to continue or type exit to quit")
    except mysql.connector.Error as error:
        print("Problem retrieving record, {}".format(error))
        sys.exit()      # this exits the application
    finally:
        if v_con.is_connected():
            v_con.close()


def view_all_passwords(acc_id):
    """
    This function simply prints out all the account passwords from the database to the console in a
    table user friendly way.

        The acc_id here is a variable that stores the id of the user logged in so that the
        program remembers the user throughout the entire operation of the program.

        we call the connection() function every time we need a connection to the database.

    """
    v1_con = connection()
    try:
        select_query = "select name, account_type, passwrd, creation_date, change_date, U_ID from info where U_ID = %s"
        select_cursor = v1_con.cursor()
        select_cursor.execute(select_query, (acc_id,))    # the cursor takes in value in the form of a tuple
        # hence, we have a comma(,) after the acc_id variable
        print("Name\t\t\tAccount\t\t\tPassword\t\tCreation Date\t\t\tChange Date\t\t\tUser ID")
        for name, account_type, passwrd, creation_date, change_date, U_ID in select_cursor:
            print(name + "\t\t" + account_type + "\t\t\t" + passwrd + "\t\t" + str(creation_date) + "\t\t"
                  + str(change_date) + "\t\t" + U_ID)

        select_cursor.close()
        # print("*\t" * 19)
        print()
        print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password\n5.View All Password"
              "\n6.View All Account Types")
        print()
        print("Select options to continue or type exit to quit")
    except mysql.connector.Error as error:
        print("Problem retrieving data, {}".format(error))
        sys.exit()      # this again exits the application
    finally:
        if v1_con.is_connected():
            v1_con.close()


def view_all_accounts(acc_id):
    """
        This functions prints out all the accounts the user has as per the database records in
        an orderly fashion in the console.

        The acc_id here is a variable that stores the id of the user logged in so that the
        program remembers the user throughout the entire operation of the program.

        we call the connection() function every time we need a connection to the database.

    """
    v2_con = connection()
    try:
        count = 1
        select_query = "select distinct account_type from info where U_ID = %s"
        select_cursor = v2_con.cursor()
        select_cursor.execute(select_query, (acc_id,))  # the cursor takes in value in the form of a tuple
        # hence, we have a comma(,) after the acc_id variable
        for account_type in select_cursor:
            print("{}. {}".format(count, *account_type))    # the *(asterisk) is used to unpacked the tuple that is
            count += 1                                      # returned by the select_cursor.
        select_cursor.close()
        print()
        print("Options\n1.Save Password\n2.Update Password\n3.Delete Password\n4.View Password\n5.View All Password"
              "\n6.View All Account Types")
        print()
        print("Select options to continue or type exit to quit")
    except mysql.connector.Error as error:
        print("Problem retrieving data, {}".format(error))
        sys.exit()
    finally:
        if v2_con.is_connected():
            v2_con.close()


def pw_operations(au_id):
    """
        This function is the function that gives the user all the options of the operations that he/she can
        perform when login in the application.

        The acc_id here is a variable that stores the id of the user logged in so that the
        program remembers the user throughout the entire operation of the program.
    """

    print("Select option below for desired operation(or type exit to quit)")
    print("""\t\t1.Save Password
                2.Update Password
                3.Delete Password
                4.View Password
                5.View All Passwords
                6.View All Account Types""")
    while True:
        option = input(">> ")
        console_clear()
        print()
        if option == "1":
            save_password(au_id)

        elif option == "2":
            update_password(au_id)

        elif option == "3":
            delete_account(au_id)

        elif option == "4":
            view_password(au_id)

        elif option == "5":
            view_all_passwords(au_id)

        elif option == "6":
            view_all_accounts(au_id)

        else:
            if option == "EXIT" or option == "exit":
                console_clear()     # this clear the console of all the debris text in the screen
                sys.exit()


def login():
    """
        This is the login function that checks the number of incorrect attempts the user has tried and logins
        successfully if the user has entered correct information. The function will close the entire program
        if the user exhausts the 3 login attempts.

        If the user is logs in successfully, this then calls the pw_operations() function to give the user
        the different operation he can perform.

        Note: Here we used getpass() function as well. Just like the above note, getpass()
        works if we run the application in CMD and does not work in IDE and editors.

        we call the connection() function every time we need a connection to the database.
    """

    l_con = connection()
    try:
        print()
        print("Enter details to login")
        login_tries = 0
        while True:
            if login_tries < 3:
                u_id = input("User ID: ")
                # l_password = input("Password: ")
                l_password = getpass.getpass("Password: ")
                console_clear()
                select_query = "select * from users where U_ID = %s and u_password = %s"
                select_cursor = l_con.cursor()
                select_cursor.execute(select_query, (u_id, l_password))
                account = select_cursor.fetchone()
                if account:
                    print()
                    print("Login successful")
                    pw_operations(u_id)
                    select_cursor.close()
                else:
                    print()
                    print("Wrong username or password!")
                    print("Please try again")
                    print()
                    login_tries += 1
            else:
                print("Login limit exhausted today. Bye")
                sys.exit()      # this again exits the application

    except mysql.connector.Error as error:
        print("Problem with the server, {}".format(error))
    finally:
        if l_con.is_connected():
            l_con.close()


def create_account():
    """
        This is a function that saves the login credentials of a new user.

        Note: Here we used getpass() function as well. Just like the above note, getpass()
        works if we run the application in CMD and does not work in IDE and editors.

        we call the connection() function every time we need a connection to the database.
    """
    c_con = connection()

    try:
        u_name = input("Enter User ID(must contain at least 1 number) : ")
        pw = getpass.getpass("Enter Password: ")
        con_pw = getpass.getpass("Re-enter password: ")
        if con_pw == pw:
            insert_query = 'insert into users(U_ID, u_password) values(%s, %s)'
            insert_cursor = c_con.cursor()
            insert_cursor.execute(insert_query, (u_name, pw))
            c_con.commit()      # this writes the data in the database
            print("{} user added successfully".format(insert_cursor.rowcount))
            insert_cursor.close()
            console_clear()
            login()
        else:
            try:
                print("Password do not match!")
                con_pw = getpass.getpass("Please enter the password again: ")
                if con_pw == pw:
                    insert_query = 'insert into users(U_ID, psswrd) values(%s, %s)'
                    insert_cursor = c_con.cursor()
                    insert_cursor.execute(insert_query, (u_name, pw))
                    c_con.commit()      # this writes the data in the database
                    print("{} user added successfully".format(insert_cursor.rowcount))
                    insert_cursor.close()
                    console_clear()
                    login()
            except mysql.connector.Error as error:
                print("Problem saving user, {}".format(error))
            finally:
                if c_con.is_connected():
                    c_con.close()
    except mysql.connector.Error as error:
        print("Problem saving user, {}".format(error))
        c_con.rollback()    # this rolls back the database to its previous state in case of any error.
    finally:
        if c_con.is_connected():
            c_con.close()


def change_password():
    """
    This function is basically to allow users change the password of their account.
    """
    c_con = connection()
    try:
        while True:
            print()
            user_id = input("Enter User ID: ")
            u_old_password = getpass.getpass("Enter old password: ")
            select_query = "select U_ID, u_password from users where U_ID = %s and u_password = %s"
            select_cursor = c_con.cursor()
            select_cursor.execute(select_query, (user_id, u_old_password))
            found = select_cursor.fetchone()
            select_cursor.close()
            if found:
                while True:
                    new_password = getpass.getpass("Enter new password: ")
                    if len(new_password) >= 8:
                        update_query = "update users set u_password = %s where U_ID = %s"
                        update_cursor = c_con.cursor()
                        update_cursor.execute(update_query, (new_password, user_id))
                        c_con.commit()
                        print("{} password changed successfully.".format(update_cursor.rowcount))
                        update_cursor.close()
                        login()
                    else:
                        print("Password length should be greater than 8 characters.")
                        print("Please enter a different password.")
                        print()
            else:
                print("Invalid User ID or Password!!")
                print("Please try again.")
                print()
                console_clear()
    except mysql.connector.Error as error:
        print("Problem saving record, {}".format(error))
    finally:
        if c_con.is_connected():
            c_con.close()


def main():
    """
    This is the main function that is responsible for execution of all the function in this program.

    The function itself is very self explanatory, since it has login, create account and exit option.
    """

    print("Please select option below that suits you(or type exit to quit): ")
    print("""\t\t1.Create Account
                2.Login
                3.Change Password""")
    while True:
        choice = input(">> ")
        console_clear()
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            change_password()
        elif choice == "exit" or choice == "EXIT":
            sys.exit()  # this exit the program
        else:
            print("Please enter valid option")


if __name__ == '__main__':
    main()
