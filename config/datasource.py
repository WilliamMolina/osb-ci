import os, sys, time as t
from java.io import FileInputStream
 
#
# These are the parameters that you need to edit before running this script
#

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
 
def updateDBAdapter(dsName):
  #
  # Initialize variables
  #
  jndiName             = 'jdbc/' + dsName 
  eisName              = 'eis/DB/' + dsName
  #
  # generate a unique string to use in the names
  # 
  uniqueString = str(int(t.time()))
  try: 
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
    plan.save()
    save()
    print('--> activating changes')
    activate(block='true')
    cd('/AppDeployments/DbAdapter/Targets')
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

print "Iniciando script de configuracion de datasources"
if len(sys.argv) > 1:
    datasource_dir = sys.argv[1]
    print "Buscando configuracion de datasources en: ",datasource_dir
    edited = False 
    added = False
    for file in os.listdir(datasource_dir):
        if file.endswith(".properties"):   
            added = False         
            propInputStream = FileInputStream(os.path.join(datasource_dir, file))
            print "Ejecutando configuracion para ", file
            configProps = Properties()
            configProps.load(propInputStream)

            domainName=configProps.get("domain.name")
            adminURL=configProps.get("admin.url")
            adminUserName=configProps.get("admin.userName")
            adminPassword=configProps.get("admin.password")

            dsName=configProps.get("datasource.name")
            dsDatabaseName=configProps.get("datasource.database.name")
            datasourceTarget=configProps.get("datasource.target")
            dsDriverName=configProps.get("datasource.driver.class")
            dsURL=configProps.get("datasource.url")
            dsUserName=configProps.get("datasource.username")
            dsPassword=configProps.get("datasource.password")
            dsTestQuery=configProps.get("datasource.test.query")
            if not edited:
                connect(adminUserName, adminPassword, adminURL)

            edit()
            startEdit()
            edited = True
            cd('/')
            try:
                cmo.createJDBCSystemResource(dsName)
                added = True
            except BeanAlreadyExistsException:
                print "El datasource ya existe, se actualizará la configuración"

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName)
            cmo.setName(dsName)

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
            set('JNDINames',jarray.array([String('jdbc/' + dsName )], String))

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName )
            cmo.setUrl(dsURL)
            cmo.setDriverName(dsDriverName)
            cmo.setPassword(dsPassword)

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCConnectionPoolParams/' + dsName )
            cmo.setTestTableName(dsTestQuery)
            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
            try:
                cmo.createProperty('user')
            except BeanAlreadyExistsException:
                print "Ya existe la propiedad user."

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/user')
            cmo.setValue(dsUserName)

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName )
            try:
                cmo.createProperty('databaseName')
            except BeanAlreadyExistsException:
                print "Ya existe la propiedad databaseName."

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDriverParams/' + dsName + '/Properties/' + dsName + '/Properties/databaseName')
            cmo.setValue(dsDatabaseName)

            cd('/JDBCSystemResources/' + dsName + '/JDBCResource/' + dsName + '/JDBCDataSourceParams/' + dsName )
            cmo.setGlobalTransactionsProtocol('OnePhaseCommit')

            cd('/SystemResources/' + dsName )
            set('Targets',jarray.array([ObjectName('com.bea:Name=' + datasourceTarget + ',Type=Server')], ObjectName))
        
            save()
            if added:
                updateDBAdapter(dsName)
            else:
                print "No se configurará el DBAdapter porque el datasource no es nuevo"

    if edited:
        activate()
    
else:
    print "Se debe especificar el directorio raiz de datasources"

