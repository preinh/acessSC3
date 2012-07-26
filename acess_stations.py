from seiscomp3 import IO, DataModel, Logging, Core, Communication, Client

from seiscomp.db.seiscomp3.inventory import Inventory as SC3_Inventory
from seiscomp.db.seiscomp3.routing import Routing as SC3_Routing

import seiscomp.db.seiscomp3.sc3wrap as sc3wrap


from seiscomp.arclink.manager import *

from optparse import OptionParser
import datetime, time
import sys, os, shutil



#dbDriverName="mysql"
#dbAddress="sysop:sysop@localhost/seiscomp3"
#dbPlugin = "dbmysql"

dbDriverName="postgresql"
dbAddress="sysop:sysop@seisDB.iag.usp.br/sc_master"
dbPlugin = "dbpostgresql"

                           

class dbtools(object):

    def __init__(self):
        self.registry = Client.PluginRegistry.Instance()
        # Add plugin dbmysql
        self.registry.addPluginName(dbPlugin)
        # Load all added plugins
        self.registry.loadPlugins()
        #pass

    def open_SC3Db(self, dbUrl):
        m = re.match("(?P<dbDriverName>^.*):\/\/(?P<dbAddress>.+?:.+?@.+?\/.+$)", dbUrl)
        if not m:
            raise SystemExit, "error in parsing SC3 DB url"
        _dbUrl = m.groupdict()
        
        dbDriver = IO.DatabaseInterface.Create(_dbUrl["dbDriverName"])
        if dbDriver is None:
            Logging.error("Cannot find database driver " + _dbUrl["dbDriverName"])
            raise SystemExit, "driver not found"
        if not dbDriver.connect(_dbUrl["dbAddress"]):
            Logging.error("Cannot connect to database at " + _dbUrl["dbAddress"])
            raise SystemExit, "connection could not be established"
        print "opening destination Database: " + _dbUrl["dbAddress"]
        dbQuery = DataModel.DatabaseQuery(dbDriver)
        sc3wrap.dbQuery = dbQuery
        
        return dbQuery
        
#    def read_sc3Db(self, query, inventory_xml, routing_xml, inv=False, rtn=False, acc=False, ma=None):
    def read_sc3Db(self, query, inv=True, rtn=False, acc=False, ma=None):
        dbQuery = query
        if inv:
            print "loading inventory from SC3 DB ..."
            inv = SC3_Inventory(dbQuery.loadInventory())
            inv.load_stations("*", modified_after=ma)
            inv.load_stations("*", "*", modified_after=ma)
            inv.load_stations("*", "*", "*", modified_after=ma)
            inv.load_stations("*", "*", "*", "*", modified_after=ma)
            inv.load_instruments(modified_after=ma)
            #inv.save_xml(inventory_xml, instr=2)
            #print "saving to file: ", inventory_xml
            #inv.print_stations()
            for net in sum([i.values() for i in inv.network.itervalues()], []):
                #print net.code
                for station in sum([ i.values() for i in net.station.itervalues()], []):
                    print net.code +"."+ station.code

            
        if rtn or acc:
            routing = SC3_Routing(dbQuery.loadRouting())
            if rtn:
                print "loading routes from dest DB ..."
                routing.load_routes(modified_after=ma)
            if acc:
                print "loading access from dest DB ..."
                routing.load_access(modified_after=ma)
            #routing.save_xml(routing_xml, use_access=True)
            #print "saving to file: ", routing_xml
        return inv  

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
dbt = dbtools()    
    
query = dbt.open_SC3Db(dbDriverName+"://"+dbAddress)
inv = dbt.read_sc3Db(query, inv=True, rtn=False, acc=False, ma=None)
#dbtools.read_sc3Db(query, options.inventoryXML, options.routingXML, inv=True, rtn=False, acc=False, ma=None)
