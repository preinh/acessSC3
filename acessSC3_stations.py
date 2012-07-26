from seiscomp3 import Client, IO, Core, DataModel


dbDriverName="mysql"
dbAddress="sysop:sysop@localhost/seiscomp3"
dbPlugin = "dbmysql"

#dbDriverName="postgresql"
#dbAddress="sysop:sysop@seisDB.iag.usp.br/sc_master"
#dbPlugin = "dbpostgresql"


# Get global plugin registry
registry = Client.PluginRegistry.Instance()
# Add plugin dbmysql
registry.addPluginName(dbPlugin)
# Load all added plugins
registry.loadPlugins()

# Create dbDriver
dbDriver = IO.DatabaseInterface.Create(dbDriverName)

# Open Connection 
dbDriver.Open(dbAddress)
dbDriver.connect(dbAddress)

# Create query
dbQuery = DataModel.DatabaseQuery(dbDriver)

inventory = dbQuery.loadInventory()
                                                              
for i in range(inventory.networkCount()):
    net = inventory.network(i)
    for j in range(net.stationCount()):
        station = net.station(j)
        for k in range(station.sensorLocationCount()):
            location = station.sensorLocation(k)
            for l in range(location.streamCount()):
                stream = location.stream(l)
                print net.code() + "." + station.code() + "." + location.code() + "." + stream.code()

