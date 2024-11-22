import json 
import requests 
import api 
import utils 

class Password:
    def forgetPassword(self,acc_type,mobileNumberForPassword):
        self.acc_type = acc_type
        self.mobileNumberForPassword = mobileNumberForPassword
        self.newPassword = input("Enter New Password:")
        self.confirmNewPassword = input("Confirm New Password:") 
        if self.newPassword == self.confirmNewPassword :
            apiKeyData = api.getAPIDataByKey(self.acc_type) 
            for i in range(len(apiKeyData)):
                if apiKeyData[i]["Mobile_Number"] == mobileNumberForPassword:
                    apiFullData = api.getAPIFullData() 
                    apiFullData[self.acc_type][i]["Password"] = self.newPassword 
                    api.postApiData(apiFullData) 
                    print("Password Changed Successfully")
        else:
            print("Confirmation Password not matched with New Password")
            self.forgetPassword(self.acc_type,self.mobileNumberForPassword)

    def resetPassword(self,acc_type):
        pass 

class UserLoggedIn:
    def BookAMovieTicket(self,userId):
        self.userId = userId
        apiData = api.getAPIFullData()
        moviesList = list(apiData['movies'].keys()) 
        movieTicketsDateList= [] 
        movieVenueList =[] 
        print("Movies Avilable to Book")
        for i in range(len(moviesList)):
            print(i+1,". ",moviesList[i]) 
        movieNum = int(input("Enter the Movie Num to book Ticket:")) 
        print("Here are your Tickets for Your ",moviesList[movieNum-1]," Movie.")
        movieTicketsData = apiData['movies'][moviesList[movieNum-1]]
        movieTicketsDateList = list(movieTicketsData.keys())
        for ticketDate in range(len(movieTicketsDateList)): 
            print(ticketDate+1,".","Date:",movieTicketsDateList[ticketDate]) 
            movieVenueList = list(apiData['movies'][moviesList[movieNum-1]][movieTicketsDateList[ticketDate]].keys())
            for venueIndex in range(len(movieVenueList)): 
                print("   ",venueIndex+1,". ","Venue:",movieVenueList[venueIndex]) 
                print("      Shows: ",end=" ") 
                showsList = list(apiData['movies'][moviesList[movieNum-1]][movieTicketsDateList[ticketDate]][movieVenueList[venueIndex]].keys()) 
                for showIndex in range(len(showsList)):
                    print(showIndex+1,".",showsList[showIndex],end="  ")  
            print("\n")
        
        dateNum = int(input("Enter the Num of the Date to Book a Ticket: "))
        venueNum = int(input("Enter the Num of Venue to Booka Ticket: ")) 
        showNum = int(input("Enter the Num of Show to Book a Ticket: ")) 

        movieDate = movieTicketsDateList[dateNum-1] 
        venueList = list(apiData["movies"][moviesList[movieNum-1]][movieDate].keys()) 
        venueName = apiData["movies"][moviesList[movieNum-1]][movieDate][venueList[venueNum-1]]
        showsList = list(apiData["movies"][moviesList[movieNum-1]][movieDate][venueList[venueNum-1]].keys())
        showTime = apiData["movies"][moviesList[movieNum-1]][movieDate][venueList[venueNum-1]][showsList[showNum-1]] 
        print(showsList[showNum-1])
        ticketClasses = list(showTime.keys())
        for i in range(len(ticketClasses)):
            print("Ticket Class:",ticketClasses[i]) 
            print("Ticket Price:",showTime[ticketClasses[i]]["Ticket Price"])
            print("Tickets Available: ",showTime[ticketClasses[i]]["Tickets Available"])  

        classNum = int(input("Enter Class Name:"))
        bookedSeats = apiData["movies"][moviesList[movieNum-1]][movieDate][venueList[venueNum-1]][showsList[showNum-1]][ticketClasses[classNum-1]]["Tickets Booked"]
        selectedSeats = []
        noOfTickets = int(input("Enter No.Of Tickets you Want:")) 
        for i in range(noOfTickets):
            seatNum = input("Enter Seat Number:") 
            selectedSeats.append(seatNum) 
            bookedSeats.append(seatNum)
        
        print("Your Tickets Booked Successfully!!") 
        print("Here is Your Ticket")
        print("Ticket Class: ",ticketClasses[classNum -1])
        print("Ticket Price: ",showTime[ticketClasses[classNum-1]]["Ticket Price"]) 
        print("Your Seats: ",end=" ")
        for i in range(len(selectedSeats)):
            if i<len(selectedSeats)-1:
                print(selectedSeats[i],end=",") 
            else:
                print(selectedSeats[i])
        print("Total Price: ",len(selectedSeats)*showTime[ticketClasses[classNum-1]]["Ticket Price"])
        
        ticketsDict = {} 
        ticketsDict['MovieName'] = moviesList[movieNum-1] 
        ticketsDict["Venue"] = venueList[venueNum-1]
        ticketsDict["Date"] = movieDate 
        ticketsDict["ShowTime"] = showsList[showNum-1] 
        ticketsDict["Class"] = ticketClasses[classNum-1] 
        ticketsDict["Seats"] = selectedSeats
        ticketsDict["NoOfSeats"] = len(selectedSeats)
        ticketsDict["Total Price"] = len(selectedSeats)*showTime[ticketClasses[classNum-1]]["Ticket Price"]
        apiData['users'][self.userId]["TicketDetails"].append(ticketsDict)
        
        ticketsList = showTime[ticketClasses[classNum]]["Tickets Available"] 
        ticketId =[]
        for i in range(len(selectedSeats)):
            for j in range(len(ticketsList)):
                if selectedSeats[i] == ticketsList[j]:
                    ticketId.append(j) 
        
        for i in ticketId:
            del ticketsList[i] 

        apiData["movies"][moviesList[movieNum-1]][movieDate][venueList[venueNum-1]][showsList[showNum-1]][ticketClasses[classNum-1]]["Tickets Available"] = ticketsList
        apiData["movies"][moviesList[movieNum-1]][movieDate][venueList[venueNum-1]][showsList[showNum-1]][ticketClasses[classNum-1]]["Tickets Booked"] = bookedSeats
        updatedApiData = apiData 
        api.postApiData(updatedApiData)
        

    def getAccountDetails(self):
        pass 

    def TransactionHistory(self,userId):
        self.userId = userId 
        apiData = api.getAPIFullData() 
        transactionList = apiData['users'][self.userId]["TicketDetails"] 
        print("Here is your list of Transactions:")
        for i in range(len(transactionList)):
            print("--------------------------------")
            print("Movie Name",transactionList[i]["MovieName"]) 
            print("Venue:",transactionList[i]["Venue"]) 
            print("Date : ",transactionList[i]["Date"]) 
            print("Show Time:",transactionList[i]["ShowTime"]) 
            print("Class: ",transactionList[i]["Class"]) 
            print("Seat Numbers: ",transactionList[i]["Seats"]) 
            print("----------------------------------------")

class AdminLoggedIn:
    def AddNewMovieBooking(self):
        self.movieName = input("Enter Movie Name to Add Booking:")
        utils.movie_tickets_data(self.movieName) 
    
    def EditExistingMovieBooking(self):
        moviesList = api.getAPIDataByKey("movies") 
        moviesList = list(moviesList.keys()) 
        for i in range(len(moviesList)):
            print(i+1,". ",moviesList[i]) 
        movieNum = int(input("Enter the Movie Number to Edit the Tickets:"))
        utils.movie_tickets_data(moviesList[movieNum-1]) 
        


    def DeleteExistingMovieBooking(self):
        pass 

class Account:

    def CreateAccountType(self,acc_type):
        self.acc_type = acc_type
        self.firstName = input("Enter Your First Name :") 
        self.lastName = input("Enter Your Last Name :") 
        self.mobileNumber = int(input("Enter Your Mobile Number:")) 
        self.password = input("Create Your Password: ")
        self.confirmPassword = input("Confirm Your Password:") 
        if self.password == self.confirmPassword :
            if self.acc_type == "users":
                ApiData = api.getAPIFullData()
                ApiKeyData = api.getAPIDataByKey("users") 
                ApiKeyDict = utils.account_details(self.firstName,self.lastName,self.mobileNumber,self.password,ApiKeyData) 
                ApiKeyData.append(ApiKeyDict)
                ApiData["users"] = ApiKeyData
                api.postApiData(ApiData) 
                print("User Account Successfully Created")

            elif acc_type == 'admin':
                ApiData = api.getAPIFullData()
                ApiKeyData = api.getAPIDataByKey("admin") 
                ApiKeyDict = utils.account_details(self.firstName,self.lastName,self.mobileNumber,self.password,ApiKeyData)
                ApiKeyData.append(ApiKeyDict) 
                ApiData["admin"] = ApiKeyData
                api.postApiData(ApiData)
                
        else : 
            print("Enter Password Correctly")
            CreateAccountType(self.acc_type)  
    
    def LoginAccountType(self,acc_type):
        self.acc_type = acc_type 
        print("-------------------------------------------")
        print(self.acc_type,"Account Log In")
        print("--------------------------------------------")
        self.EnteredMobileNumber = int(input("Enter Your Mobile Number:")) 
        self.EnteredPassword = input("Enter Your Password: ")
        acc_type_key_data = api.getAPIDataByKey(self.acc_type)
        login = False
        for i in range(len(acc_type_key_data)):
            if acc_type_key_data[i]["Mobile_Number"] == self.EnteredMobileNumber and acc_type_key_data[i]["Password"] == self.EnteredPassword :
                print(self.acc_type," Account Log In Successful!!")
                print("Welcome ",acc_type_key_data[i]["First_Name"])
                if self.acc_type == 'admin':
                    print("1.Add New Movie to Book Tickets")
                    print("2.Edit Existing Movie Data.")
                    print("3.Delete Existing Movie Booking")
                    adminNum = int(input("Enter a Number:")) 
                    if adminNum == 1:
                        adminlog1.AddNewMovieBooking() 
                    elif adminNum == 2:
                        adminlog1.EditExistingMovieBooking()

                else:
                    print("1.Book a Movie Ticket")
                    print("2.Transaction History")
                    print("3.Get User Details") 
                    userNum = int(input("Enter a Number:")) 
                    if userNum == 1:
                        userlogin1.BookAMovieTicket(i) 
                    elif userNum == 2:
                        userlogin1.TransactionHistory(i) 
                    elif userNum == 3:
                        userlogin1.getAccountDetails() 
                login= True 
        if login == False:
            print("Entered Wrong Password")
            num = int(input(("Forget Password? Enter 1.To Change forget Password 2.To Re-LogIn the Account.")))
            if num == 1:
                mobileNumberForPassword = int(input("Enter Your Mobile Number to Change Your Password:")) 
                apiKeyData= api.getAPIDataByKey(self.acc_type) 
                mobileNumberDone = False
                while True:
                    for i in range(len(apiKeyData)):
                        if apiKeyData[i]["Mobile_Number"] == mobileNumberForPassword :
                            pass1.forgetPassword(self.acc_type,mobileNumberForPassword) 
                            mobileNumberDone = True
                            break 
                    else:
                        print("Enter Mobile Number Correctly")      
                    
                    if mobileNumberDone == True:
                        break
            else:
                self.LoginAccountType(self.acc_type) 
        
class SignUp(Account):
    def CreateUserAccount(self):
        self.CreateAccountType("users")
    def CreateAdminAccount(self):
        self.CreateAccountType("admin")  

class Login(Account):
    def LogInUserAccount(self):
        self.LoginAccountType("users")

    def LogInAdminAccount(self):
        self.LoginAccountType("admin")
       
class Booking:
    def BookMovieTickets(self):
        pass 

    def BookShowTickets(self):
        pass  

class UserDetails:
    def UserTransactions(self):
        pass 

acc1 = Account()
log1 = Login() 
sign1 = SignUp() 
pass1 = Password() 
adminlog1 = AdminLoggedIn() 
userlogin1 = UserLoggedIn() 

print("1.Sign Up")
print("2.Log In") 
num = int(input("Enter the Number:")) 
if num == 1:
    print("1.Admin Account Sign Up") 
    print("2.User Account Sign Up") 
    num1 = int(input("Enter the Number:")) 
    if num1 == 1:
        sign1.CreateAdminAccount() 
    elif num1 == 2:
        sign1.CreateUserAccount()
elif num == 2:
    print("1.LogIn Account for User")
    print("2.LogIn Account for Admin")
    num2 = int(input("Enter the Number:")) 
    if num2 ==1 :
        log1.LogInUserAccount() 
    elif num2 == 2:
        log1.LogInAdminAccount()  



