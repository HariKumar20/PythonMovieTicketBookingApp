import api 

def account_details(firstName,lastName,mobileNumber,password,ApiKeyData):
    account_dict= dict()
    account_dict["id"] = len(ApiKeyData)+1 
    account_dict["First_Name"] = firstName 
    account_dict["Last_Name"] = lastName 
    account_dict["Mobile_Number"] = mobileNumber 
    account_dict["Password"] = password 

    return account_dict  

def movie_tickets_data(movieName):
    venueName = input("Enter Venue Name to Add Booking:") 
    date = input("Enter Date(DD-MM-YYYY) to Add Booking:")
    noOfDays = int(input("Enter No.of Days to Add (Ex : 1 to 6):")) 
    noOfShows = int(input("Enter No of Shows to Add(Ex : 1 to 6):")) 
    noOfTicketClass = int(input("Enter No Of Classes:")) 
    ticketsDict = {} 
    for ticketclass in range(noOfTicketClass):
            ticketClassName = input("Enter Your Ticket Class Name:") 
            ticketClassPrice = int(input("Enter the Ticket Price of the Class:")) 
            ticketsDict[ticketClassName] ={}
            ticketsDict[ticketClassName]["Ticket Price"] = ticketClassPrice 
            seatsList = []
            noOfRows = int(input("Enter No Of Rows in Theatre:")) 
            noOfSeats = int(input("Enter No Of Seats Per Row:")) 
            for rowIndex in range(65,65+noOfRows+1):
                for seatNum in range(1,noOfSeats+1):
                    seatName = str(chr(rowIndex))+str(seatNum)
                    seatsList.append(seatName) 
            ticketsDict[ticketClassName]["Tickets Available"] = seatsList 
            ticketsDict[ticketClassName]["Tickets Booked"] =[] 
    movieDict = api.getAPIDataByKey("movies")
    movieDict[movieName] =movieDict[movieName]
    updateDate = date 
    for day in range(noOfDays+1):
        movieDict[movieName][updateDate] = {} 
        movieDict[movieName][updateDate][venueName] ={} 
        for showIndex in range(noOfShows):
            showTime = input("Enter Show Time:") 
            movieDict[movieName][updateDate][venueName][showTime] ={} 
            for ticketClassIndex in list(ticketsDict.keys()):
                movieDict[movieName][updateDate][venueName][showTime][ticketClassIndex] = ticketsDict[ticketClassIndex]
        try:
            updateDate = str(int(updateDate[:2])+1)+str(updateDate[2:])
        except ValueError:
            updateDate = str(int(updateDate[:1])+1)+str(updateDate[1:]) 
    
    apiMovieData = api.getAPIFullData() 
    apiMovieData["movies"] = movieDict 
    api.postApiData(apiMovieData) 
    return apiMovieData