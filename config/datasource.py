import os, sys
from java.io import FileInputStream
print "Iniciando script de configuracion de datasources"
if len(sys.argv) > 1:
    datasource_dir = sys.argv[1]
    print "Buscando configuracion de datasources en: ",datasource_dir
    edited = False 
    for file in os.listdir(datasource_dir):
        if file.endswith(".properties"):            
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

    if edited:
        activate()
    
else:
    print "Se debe especificar el directorio raiz de datasources"

