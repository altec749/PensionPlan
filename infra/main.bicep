targetScope = 'subscription'

@description('Azure region for all resources.')
param location string = 'westeurope'

@description('Resource group name.')
param resourceGroupName string = 'rg-pension'

@description('Container Apps environment name.')
param containerAppEnvName string = 'pension-env'

@description('Container App name.')
param containerAppName string = 'pension-api'

@description('Container name within the app.')
param containerName string = 'pension-api'

@description('Container image to deploy (e.g. ghcr.io/owner/pension-api:latest).')
param containerImage string

@description('Log Analytics workspace name.')
param logAnalyticsName string = 'pension-logs'

@description('Tags applied to all resources.')
param tags object = {
  app: 'pension'
}

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module app 'app.bicep' = {
  name: 'pension-app'
  scope: rg
  params: {
    location: location
    containerAppEnvName: containerAppEnvName
    containerAppName: containerAppName
    containerName: containerName
    containerImage: containerImage
    logAnalyticsName: logAnalyticsName
    tags: tags
  }
}

output containerAppUrl string = app.outputs.containerAppUrl
