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
   retirement_age = 60
   annual_real_return = 0.04
   monthly_drawdown = 3725
   death_age = 100
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

Setup:

```powershell
# Create service principal for GitHub Actions (used by AZURE_CREDENTIALS)
$cred =az ad sp create-for-rbac `
  --name "pension-gha" `
  --role contributor `
  --scopes /subscriptions/<subscription-id> `
  --json-auth
```

Required GitHub secrets:

- `AZURE_CREDENTIALS`: $cred above
- `ACA_APP_NAME`: name of your Container App
- `ACA_ENVIRONMENT`: name of your Container Apps environment
- `GHCR_USERNAME`: your GitHub username or org
- `GHCR_TOKEN`: a GitHub token with `read:packages` (and `write:packages` if needed)

Then store the outputs as GitHub Secrets and push to `master`.

```powershell
az deployment sub create `
  --location westeurope `
  --template-file infra/main.bicep `
  --parameters `
    resourceGroupName=rg-pension `
    containerAppEnvName=pension-env `
    containerAppName=pension-api `
    containerName=pension-api `
    containerImage=ghcr.io/altec749/pension-api:latest
```
