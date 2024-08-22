while ($true) {
    git add .
    git commit -m "Auto-commit"
    git push origin main
    Start-Sleep -Seconds 3600  # Sleep for 1 hour
}
