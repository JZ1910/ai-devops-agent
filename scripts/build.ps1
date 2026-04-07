Write-Host "Starting build process..." -ForegroundColor Cyan

Write-Host "Connecting Docker to Minikube..." -ForegroundColor Yellow
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Write-Host "Moving to app folder..." -ForegroundColor Yellow
Set-Location "..\app"

Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t ai-devops-app .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed." -ForegroundColor Red
    exit 1
}

Write-Host "Docker image built successfully." -ForegroundColor Green