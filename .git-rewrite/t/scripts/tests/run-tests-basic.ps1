# PowerShell script to run basic tests

Write-Host "Running basic tests..."
python -m unittest discover -s scripts/tests -p "test_*.py"
Write-Host "Basic tests completed."
