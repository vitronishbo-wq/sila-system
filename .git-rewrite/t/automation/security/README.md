# Security Scripts

Essential security tools for the SILA system.

## Available Tools

- **`security_audit.py`** - Comprehensive vulnerability scanner
- **`security_remediation.py`** - Automated vulnerability fixer
- **`check_credentials.py`** - Credential validation tool

## Usage

```bash
# Run full security audit
python security_audit.py

# Fix identified vulnerabilities
python security_remediation.py

# Validate credentials
python check_credentials.py
```

## Integration

These tools are integrated into the CI/CD pipeline and run automatically on:

- Pull requests
- Deployment to staging/production
- Security scans

## Reports

Security reports are generated in `../../docs/reports/` directory.
