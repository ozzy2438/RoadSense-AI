param namePrefix string
param location string

var storageName = toLower(replace('${namePrefix}st', '-', ''))

resource account 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: take(storageName, 24)
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

resource rawDocuments 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${account.name}/default/raw-documents'
  properties: {
    publicAccess: 'None'
  }
}

output storageAccountName string = account.name
