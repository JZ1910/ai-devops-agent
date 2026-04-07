Write-Host "Starting deployment process..." -ForegroundColor Cyan

Write-Host "Moving to k8s folder..." -ForegroundColor Yellow
Set-Location "..\k8s"

Write-Host "Applying Kubernetes manifests..." -ForegroundColor Yellow
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

if ($LASTEXITCODE -ne 0) {
    Write-Host "Kubernetes apply failed." -ForegroundColor Red
    exit 1
}

Write-Host "Restarting deployment..." -ForegroundColor Yellow
kubectl rollout restart deployment ai-devops-app

Write-Host "Waiting for rollout status..." -ForegroundColor Yellow
kubectl rollout status deployment ai-devops-app

if ($LASTEXITCODE -ne 0) {
    Write-Host "Deployment rollout failed." -ForegroundColor Red
    exit 1
}

Write-Host "Deployment successful." -ForegroundColor Green
Write-Host ""
kubectl get pods
Write-Host ""
kubectl get svc