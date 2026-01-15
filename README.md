# PensionPlan

## API usage (PowerShell)

Start locally:

```powershell
pip install -r requirements.txt
uvicorn app:app --reload
```

Example request:

```powershell
$body = @{
  retirement_age = 67
  annual_real_return = 0.03
  monthly_drawdown = 2000
  death_age = 90
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/calculate `
  -ContentType "application/json" `
  -Body $body
```

## Docker

```powershell
docker build -t pension-api .
docker run -p 8000:8000 pension-api
```

## Azure Container Apps deploy (GitHub Actions)

This repo includes a workflow at `.github/workflows/deploy-aca.yml` that builds the image,
deploys infrastructure via `infra/main.bicep`, and then updates the Container App on
pushes to `master`.

Required GitHub secrets:

- `AZURE_CREDENTIALS`: output of `az ad sp create-for-rbac` (JSON)
- `ACA_APP_NAME`: name of your Container App
- `ACA_ENVIRONMENT`: name of your Container Apps environment
- `GHCR_USERNAME`: your GitHub username or org
- `GHCR_TOKEN`: a GitHub token with `read:packages` (and `write:packages` if needed)

Typical setup (PowerShell):

```powershell
# Create service principal for GitHub Actions (used by AZURE_CREDENTIALS)
az ad sp create-for-rbac `
  --name "pension-gha" `
  --role contributor `
  --scopes /subscriptions/<subscription-id>/resourceGroups/rg-pension `
  --sdk-auth
```

Then store the outputs as GitHub Secrets and push to `master`.

## Infrastructure as Code (Bicep)

The Bicep setup is split into two files:

- `infra/main.bicep` (subscription-scope): creates the resource group and calls the module.
- `infra/app.bicep` (resource-group scope): creates Log Analytics, the Container Apps environment,
  and the Container App.

The deployment provisions the required resources in West Europe:

- Resource group
- Log Analytics workspace (required by Container Apps)
- Container Apps environment
- Container App with public ingress on port 8000

Deploy example (run from your PC):

```powershell
az deployment sub create `
  --location westeurope `
  --template-file infra/main.bicep `
  --parameters `
    resourceGroupName=rg-pension `
    containerAppEnvName=pension-env `
    containerAppName=pension-api `
    containerName=pension-api `
    containerImage=ghcr.io/<owner>/pension-api:latest
```
