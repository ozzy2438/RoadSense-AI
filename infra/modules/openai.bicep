param namePrefix string
param location string

resource account 'Microsoft.CognitiveServices/accounts@2024-04-01-preview' = {
  name: '${namePrefix}-openai'
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: '${namePrefix}-openai'
    publicNetworkAccess: 'Enabled'
  }
}

output openAiName string = account.name
