import requests
import json
import pandas as pd


url = "https://www.alphavantage.co/query"
function = "TIME_SERIES_DAILY"
symbol = "MSFT"
apiKey = "PGQ2DSJEX55TF5H9"

#Get the data from AlphaVantage with a GET request
def getData(url, function, symbol, apiKey):

        data = {"function" : function,
                "symbol" : symbol,
                "apikey" : apiKey }

        try:
                time = requests.get(url).elapsed.total_seconds()
                request = requests.get(url, params = data)
                print("Time elapsed : " + str(time) + " sec")
        except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

        return request

#Gets the dailiy ticker data from the JSON and parses it

def handleData(inputData):

        outputData = pd.DataFrame(columns = ['Date', 'Open', 'Close', 'High', 'Low'])

        for key in inputData:
                open = dailyData[key]["1. open"]
                high = dailyData[key]["2. high"]
                low = dailyData[key]["3. low"]
                close = dailyData[key]["4. close"]

                outputData = outputData.append({'Date': key, 'Open' : open, 'High' : high, 'Low' : low, 'Close' : close}, ignore_index = True) 

        return(outputData)


rawData = getData(url, function, symbol, apiKey)

#Transforms the GET request data into JSON format
jsonData = json.loads(rawData.content)

dailyData = jsonData['Time Series (Daily)']

#print(dailyData)

columns = ['Date', 'Open', 'Close', 'High', 'Low']
index = dailyData.keys()

df = pd.DataFrame(index = index, columns = columns)
df = df.fillna(0)

#print(df)

dataFrame = handleData(dailyData)
dataFrame['Date'] = pd.to_datetime(dataFrame['Date'])
dataFrame = dataFrame.set_index('Date')
print(dataFrame)
