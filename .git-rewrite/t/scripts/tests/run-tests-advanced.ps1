# PowerShell script to run advanced tests

Write-Host "Running advanced tests..."
python -m unittest discover -s scripts/tests -p "test_*.py"
Write-Host "Advanced tests completed."
