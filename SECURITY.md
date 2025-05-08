# Security Policy

## Supported Versions

Currently, the following versions of PIGAME are supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.7.x   | :white_check_mark: |
| 1.6.x   | :white_check_mark: |
| < 1.6   | :x:                |

## Reporting a Vulnerability

We take the security of PIGAME seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do Not** disclose the vulnerability publicly until it has been addressed.
2. Email your findings to security@example.com. If possible, encrypt your message using our PGP key.
3. Include as much information as possible, including:
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fixes (if any)

## Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours.
- We will provide a more detailed response within 7 days, including our assessment of the vulnerability and an expected timeline for a fix.
- We will keep you informed of our progress throughout the remediation process.
- Once the vulnerability is fixed, we will publicly acknowledge your responsible disclosure (unless you prefer to remain anonymous).

## Security Best Practices for Contributing

If you're contributing to PIGAME, please follow these security best practices:

1. **Input Validation**: Always validate user inputs before processing them.
2. **Dependencies**: Keep dependencies up-to-date and use known secure versions.
3. **Avoid Hardcoded Secrets**: Never commit API keys, passwords, or other sensitive data to the repository.
4. **Code Reviews**: All code changes should be reviewed for security implications.
5. **Static Analysis**: Use static analysis tools to detect common security issues.

## Threat Model

PIGAME is a tool for memorization of π and does not store or process sensitive user data. The primary security concerns are:

1. Input validation to prevent exploitation
2. Ensuring dependencies are kept up-to-date
3. Maintaining secure development practices

## Security Updates

Security updates will be released as part of our normal release cycle. Critical security issues may receive expedited releases.

Thank you for helping keep PIGAME secure!
