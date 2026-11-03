# 🛡️ Security Policy & Data Privacy Guidelines

## 1. Zero-Leak Credential & Secrets Architecture

The **MetaFrontier NeuroTwin** project strictly enforces zero-exposure credential handling to protect developers, system administrators, and organizations from unauthorized access, intellectual property theft, or credential harvesting.

### Mandatory Rules for All Contributors & Developers:

1. **Never Hardcode Secrets**:
   - Private keys (`.pem`, `.key`, `id_rsa`), API keys (`META_MODEL_API_KEY`), passwords, admin tokens, and serial numbers must **never** be hardcoded in application logic, scripts, or commit history.
   
2. **Environment Variable Isolation**:
   - All secret variables must reside exclusively in `.env` or `.env.local` files on your local machine.
   - The `.gitignore` configuration in this repository strictly bans `.env`, `.env.*`, `*.pem`, `*.key`, `admin/`, `admin_panel/`, and credential files from being tracked by git.
   - Use `.env.example` as a sanitized schema template.

3. **In-Memory Credential Scrubbing**:
   - When entering an API token into the frontend UI Settings modal, the token is kept exclusively in browser `localStorage` or ephemeral memory session. It is never transmitted to unverified third-party endpoints or logged to disk.

4. **Automated Secret Auditing**:
   - Before committing or deploying changes, run the automated security verification script:
     ```bash
     npm run security:check
     # or: node cli/security-check.js
     ```

---

## 2. Protected File Patterns & Asset Classifications

The following extensions and directories are strictly classified as confidential and blocked from all public commits:

| Category | File Patterns & Targets | Policy Enforcement |
| :--- | :--- | :--- |
| **Cryptographic Keys** | `*.pem`, `*.key`, `*.cert`, `*.p12`, `*.pfx`, `id_rsa*` | **Strictly Blocked** via `.gitignore` |
| **API & Access Tokens** | `*api_key*`, `*secret*`, `*token*`, `client_secret*.json` | **Strictly Blocked** |
| **Passwords & Admin Data**| `*password*`, `admin/`, `admin_panel/`, `serial_keys.txt` | **Strictly Blocked** |
| **Database & Cache** | `*.db`, `*.sqlite`, `*.sql`, `*.dump`, `__pycache__/` | **Strictly Blocked** |
| **Cloud Credentials** | `.aws/`, `.gcp/`, `.azure/`, `service-account*.json` | **Strictly Blocked** |

---

## 3. Incident Response & Responsible Disclosure

If you discover a potential vulnerability or accidental credential leak:
- **Do not** file a public issue on GitHub.
- Immediately revoke/rotate the affected key or password through the model provider or cloud dashboard.
- Contact the development team through the verified developer profiles listed in the footer.
