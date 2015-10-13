"""
Credit: Michael Halls-Moore
Url:    https://www.quantstart.com/articles/Downloading-Historical-Intraday-US-
        Equities-From-DTN-IQFeed-with-Python
        
I simply wrapped the logic into a class. 
Will possibly extend for live feeds.

@author: Luke Patrick James Tighe
"""

import datetime
import socket
import os.path
import pandas as pd

"""
IQ DTN Feed Historical Symbol Download.
Downloads the symbol data in CSV format and stores it in a local directroy.
If we already have the symbol data downloaded, it will not hit IQ DTN Feed again,
it will simple use the local data.
To flush the local CSV file, simply delete the directory.

Constructor enables to specify a start and end date for the symbol data as well
as the frequency. Great for making sure data is consistent.

Simple usage example:

    from iqfeed import historicData

    dateStart = datetime.datetime(2014,10,1)
    dateEnd = datetime.datetime(2015,10,1)        
        
    iq = historicData(dateStart, dateEnd, 60)
    symbolOneData = iq.download_symbol(symbolOne)
    
"""
class historicData:

    # 
    def __init__(self, startDate, endDate, timeFrame=60):
        
        self.startDate = startDate.strftime("%Y%m%d %H%M%S")
        self.endDate = endDate.strftime("%Y%m%d %H%M%S")
        self.timeFrame = str(timeFrame)
        # We dont want the download directory to be in our source control
        self.downloadDir = "../../MarketData/"
        self.host = "127.0.0.1"  # Localhost
        self.port = 9100  # Historical data socket port

    def read_historical_data_socket(self, sock, recv_buffer=4096):
        """
        Read the information from the socket, in a buffered
        fashion, receiving only 4096 bytes at a time.
    
        Parameters:
        sock - The socket object
        recv_buffer - Amount in bytes to receive per read
        """
        buffer = ""
        data = ""
        while True:
            data = sock.recv(recv_buffer)
            buffer += data
    
            # Check if the end message string arrives
            if "!ENDMSG!" in buffer:
                break
       
        # Remove the end message string
        buffer = buffer[:-12]
        return buffer
        
    def download_symbol(self, symbol):
    
        # Construct the message needed by IQFeed to retrieve data
        #[bars in seconds],[beginning date: CCYYMMDD HHmmSS],[ending date: CCYYMMDD HHmmSS],[empty],[beginning time filter: HHmmSS],[ending time filter: HHmmSS],[old or new: 0 or 1],[empty],[queue data points per second]
        #message = "HIT,%s,%i,%s,%s,,093000,160000,1\n" % symbol, self.timeFrame, self.startDate, self.endDate
        #message = message = "HIT,%s,%s,20150101 075000,,,093000,160000,1\n" % symbol, self.timeFrame
    
        fileName = "{0}{1}-{2}-{3}-{4}.csv".format(self.downloadDir, symbol, self.timeFrame, self.startDate, self.endDate)
        exists = os.path.isfile(fileName)
        
        if exists == False:       
            
            message = "HIT,{0},'{1}',{2},{3},,093000,160000,1\n".format(symbol, self.timeFrame, self.startDate, self.endDate)
        
            # Open a streaming socket to the IQFeed server locally
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            
            sock.sendall(message)
            data = self.read_historical_data_socket(sock)
            sock.close
            
            # Remove all the endlines and line-ending
            # comma delimiter from each record
            data = "".join(data.split("\r"))
            data = data.replace(",\n","\n")[:-1]
    
            # Write the data stream to disk
            
            f = open(fileName, "w")
            f.write(data)
            f.close()
            
        return pd.io.parsers.read_csv(fileName, header=0, index_col=0, names=['datetime','open','low','high','close','volume','oi'], parse_dates=True)