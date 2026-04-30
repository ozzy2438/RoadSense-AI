targetScope = 'resourceGroup'

@description('Location for all resources.')
param location string = resourceGroup().location

@description('Environment suffix, for example dev or prod.')
param environmentName string = 'dev'

var namePrefix = 'roadsense-${environmentName}'

module storage './modules/storage.bicep' = {
  name: 'storage'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module search './modules/search.bicep' = {
  name: 'search'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module cosmos './modules/cosmos.bicep' = {
  name: 'cosmos'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module openai './modules/openai.bicep' = {
  name: 'openai'
  params: {
    namePrefix: namePrefix
    location: location
  }
}

module functions './modules/functions.bicep' = {
  name: 'functions'
  params: {
    namePrefix: namePrefix
    location: location
    storageAccountName: storage.outputs.storageAccountName
  }
}

module aks './modules/aks.bicep' = {
  name: 'aks'
  params: {
    namePrefix: namePrefix
    location: location
  }
}
