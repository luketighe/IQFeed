# IQFeed
Python - IQ DTN Feed Historical Data Download &amp; Cache

IQ DTN Feed Historical Symbol Download.
Downloads the symbol data in CSV format and stores it in a local directroy.
If we already have the symbol data downloaded, it will not hit IQ DTN Feed again,
it will simple use the local data.
To flush the local CSV file, simply delete the directory.

Constructor enables you to specify a start and end date for the symbol data as well
as the frequency. Great for making sure data is consistent.

Simple usage example:

    from iqfeed import historicData

    dateStart = datetime.datetime(2014,10,1)
    dateEnd = datetime.datetime(2015,10,1)        
        
    iq = historicData(dateStart, dateEnd, 60)
    symbolOneData = iq.download_symbol(symbolOne)

