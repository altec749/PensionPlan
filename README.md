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
