#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="${1:-roadsense-dev}"
LOCATION="${2:-australiaeast}"
ENVIRONMENT_NAME="${3:-dev}"

az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
az deployment group create \
  --resource-group "$RESOURCE_GROUP" \
  --template-file infra/main.bicep \
  --parameters location="$LOCATION" environmentName="$ENVIRONMENT_NAME"
