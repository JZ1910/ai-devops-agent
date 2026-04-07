Write-Host "Starting full release pipeline..." -ForegroundColor Cyan

Write-Host "Running build script..." -ForegroundColor Yellow
& ".\build.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build step failed. Stopping release." -ForegroundColor Red
    exit 1
}

Set-Location $PSScriptRoot

Write-Host "Running deploy script..." -ForegroundColor Yellow
& ".\deploy.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Deploy step failed. Stopping release." -ForegroundColor Red
    exit 1
}

Write-Host "Full release pipeline completed successfully." -ForegroundColor Green