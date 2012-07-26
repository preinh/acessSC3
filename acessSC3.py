from seiscomp3 import Client, IO, Core, DataModel

dbDriverName="mysql"
dbAddress="sysop:sysop@localhost/seiscomp3"
dbPluginName = "dbmysql"

# Get global plugin registry
registry = Client.PluginRegistry.Instance()
# Add plugin dbmysql
registry.addPluginName(dbPluginName)
# Load all added plugins
registry.loadPlugins()

# Create dbDriver
dbDriver = IO.DatabaseInterface.Create(dbDriverName)

# Open Connection 
#dbDriver.Open(dbAddress)   
dbDriver.connect(dbAddress)

# set Query object
dbQuery = DataModel.DatabaseQuery(dbDriver)

s = Core.Time_FromString("2012-01-01 00:00:00", "%F %T")
e = Core.Time_FromString("2012-02-01 00:00:00", "%F %T")

qEvts = dbQuery.getEvents(s, e)

for obj in qEvts:
    evt = DataModel.Event.Cast(obj)
    if evt:
        print evt.publicID()
