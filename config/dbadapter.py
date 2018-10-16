# Copyright 2012 Oracle Corporation.
# All Rights Reserved.
#
# Provided on an 'as is' basis, without warranties or conditions of any kind,
# either express or implied, including, without limitation, any warranties or
# conditions of title, non-infringement, merchantability, or fitness for a
# particular purpose. You are solely responsible for determining the
# appropriateness of using and assume any risks. You may not redistribute.
#
# Please refer to https://redstack.wordpress.com/continous-integration for details.
#
# This WLST script can be used as part of a continuous integration build process
# before deploying a SCA composite, to create any necessary Java EE data sources
# on the WebLogic Server.
#
# In addition to creating the data source, this script will also update the
# resource adapter and redeploy it.
#
# Parts of this script were adapted from Richard van den Berg's post at
# https://forums.oracle.com/forums/message.jspa?messageID=10131949#10131949
 
import time
 
#
# These are the parameters that you need to edit before running this script
#
 
# admin server url
url                  = 't3://localhost:7101'
# username to connect to the admin server
username             = 'weblogic'
# password to connect to the admin server
password             = 'welcome1'
# the name for the EIS - as defined in the DB Adapter wizard in JDEV
eisName              = 'eis/db/myDS4'
# the admin or managed server to target where the DbAdapter is deployed
serverName           = 'DefaultServer'
nmServerName         = 'DefaultServer'
# the name for the data source
dsName               = 'myDS4'
# the JNDI name for the data source
jndiName             = 'jdbc/myDS4'
# the database url for the data source
dbUrl                = 'jdbc:oracle:thin:@10.2.145.76:1699/hospitaldev'
# the database user
dbUser               = 'ERRORHOSPITAL'
# the database password
dbPassword           = 'err0r0r0sp1t4l16'
# the database driver to use
dbDriver             = 'oracle.jdbc.xa.client.OracleXADataSource'
# the host where node manager is running
nmHost               = 'localhost'
# the port to connect to node manager (5556 is default for plain mode)
nmPort               = '5556'
# the user to connect to node manager
nmUser               = 'weblogic'
# the password to connection to node manager
nmPassword           = 'welcome1'
# the name of the weblogic domain
domain               = 'base_domain'
 
# don't change these ones
uniqueString         = ''
appName              = 'DbAdapter'
moduleOverrideName   = appName
moduleDescriptorName = 'META-INF/weblogic-ra.xml'
 
#
# method definitions
#
 
def makeDeploymentPlanVariable(wlstPlan, name, value, xpath, origin='planbased'):
  """Create a varaible in the Plan.
  This method is used to create the variables that are needed in the Plan in order
  to add an entry for the outbound connection pool for the new data source.
  """
 
  try:
    variableAssignment = wlstPlan.createVariableAssignment(name, moduleOverrideName, moduleDescriptorName)
    variableAssignment.setXpath(xpath)
    variableAssignment.setOrigin(origin)
    wlstPlan.createVariable(name, value)
 
  except:
    print('--> was not able to create deployment plan variables successfully')
 
def main():
 
  print ' Copyright 2012 Oracle Corporation. '
  print ' All Rights Reserved. '
  print ''
  print ' Provided on an ''as is'' basis, without warranties or conditions of any kind, '
  print ' either express or implied, including, without limitation, any warranties or '
  print ' conditions of title, non-infringement, merchantability, or fitness for a '
  print ' particular purpose. You are solely responsible for determining the '
  print ' appropriateness of using and assume any risks. You may not redistribute.'
  print ''
  print ' Please refer to https://redstack.wordpress.com/continous-integration for details.'
  print ''
  print ' This WLST script can be used as part of a continuous integration build process'
  print ' before deploying a SCA composite, to create any necessary Java EE data sources'
  print ' on the WebLogic Server.'
  print ''
  print ' In addition to creating the data source, this script will also update the '
  print ' resource adapter and redeploy it.'
  print ''
  print ' !!! WARNING !!! WARNING !!! WARNING !!! WARNING !!! WARNING !!! WARNING !!!'
  print ''
  print ' This script will make changes to your WebLogic domain.  Make sure you know '
  print ' what you are doing.  There is no support for this script.  If something bad '
  print ' happens, you are on your own!  You have been warned.'
 
  #
  # generate a unique string to use in the names
  #
 
  uniqueString = str(int(time.time()))
 
  #
  # Create a JDBC Data Source.
  #
 
  try:
    print('--> about to connect to weblogic')
    connect(username, password, url)
    print('--> about to create a data source ' + dsName)
    edit()
    startEdit()
    cmo.createJDBCSystemResource(dsName)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
    cmo.setName(dsName)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    set('JNDINames',jarray.array([String(jndiName)], String))
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName)
    cmo.setUrl(dbUrl)
    cmo.setDriverName(dbDriver)
    cmo.setPassword(dbPassword)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName)
    cmo.setTestTableName('DUAL')
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName)
    cmo.createProperty('user')
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
    cmo.setValue(dbUser)
    cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName)
    cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
    cd('/JDBCSystemResources/' + dsName)
    set('Targets',jarray.array([ObjectName('com.bea:Name=' + serverName + ',Type=Server')], ObjectName))
    save()
    print('--> activating changes')
    activate()
    print('--> done')
 
#
# update the deployment plan
#
    print('--> about to update the deployment plan for the DbAdapter')
    startEdit()
    planPath = get('/AppDeployments/DbAdapter/PlanPath')
    appPath = get('/AppDeployments/DbAdapter/SourcePath')
    print('--> Using plan ' + planPath)
    plan = loadApplication(appPath, planPath)
    print('--> adding variables to plan')
    makeDeploymentPlanVariable(plan, 'ConnectionInstance_eis/DB/' + dsName + '_JNDIName_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/jndi-name')
    makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, jndiName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="xADataSourceName"]/value')
    print('--> saving plan')
    plan.save();
    save();
    print('--> activating changes')
    activate(block='true');
    cd('/AppDeployments/DbAdapter/Targets');
    print('--> redeploying the DbAdapter')
    redeploy(appName, planPath, targets=cmo.getTargets());
    print('--> done')
 
  except:
    print('--> something went wrong, bailing out')
    stopEdit('y')
    raise SystemExit
 
  #
  # disconnect from the admin server
  #
 
  print('--> disconnecting from admin server now')
  disconnect()
 
  #
  # Restart the managed server using the node manager.
  #
 
#
#  this is the main entry point
#
 
main()