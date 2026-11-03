#!/usr/bin/env node

/**
 * MetaFrontier NeuroTwin - Security & Credential Auditor
 * Scans the repository for sensitive keys, passwords, .pem certificates, and .env leaks.
 */

import fs from 'fs';
import path from 'path';

const ROOT_DIR = process.cwd();

const SENSITIVE_EXTENSIONS = [
  '.pem', '.key', '.pkcs12', '.p12', '.pfx', '.cert', '.crt',
  '.kdbx', '.keystore', '.dump', '.sql', '.sqlite'
];

const FORBIDDEN_FILE_PATTERNS = [
  /^\.env$/i,
  /^\.env\.local$/i,
  /^\.env\.production$/i,
  /password/i,
  /admin_credentials/i,
  /serial_keys/i,
  /service-account.*\.json$/i,
  /id_rsa/i
];

const SCAN_IGNORE_DIRS = new Set([
  'node_modules',
  '.git',
  'dist',
  'build',
  '__pycache__',
  '.venv',
  'env'
]);

const SECRET_PATTERNS = [
  { name: 'Private Key Header', regex: /-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/ },
  { name: 'Hardcoded API Key', regex: /sk-[a-zA-Z0-9_-]{24,}/ },
  { name: 'Meta Bearer Secret', regex: /META_SECRET_[A-Z0-9]{16,}/ },
  { name: 'Hardcoded Admin Password', regex: /admin_password\s*=\s*['"][^'"]{4,}['"]/i }
];

let leakCount = 0;
let scannedFiles = 0;

function scanDirectory(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    const relPath = path.relative(ROOT_DIR, fullPath);

    if (entry.isDirectory()) {
      if (!SCAN_IGNORE_DIRS.has(entry.name)) {
        scanDirectory(fullPath);
      }
      continue;
    }

    scannedFiles++;
    const ext = path.extname(entry.name).toLowerCase();

    // 1. Check for banned sensitive extensions
    if (SENSITIVE_EXTENSIONS.includes(ext)) {
      console.log(`\x1b[31m[CRITICAL LEAK]\x1b[0m Sensitive credential file found: ${relPath}`);
      leakCount++;
      continue;
    }

    // 2. Check for banned file patterns
    for (const pattern of FORBIDDEN_FILE_PATTERNS) {
      if (pattern.test(entry.name) && entry.name !== '.env.example') {
        console.log(`\x1b[31m[CRITICAL LEAK]\x1b[0m Unsafe secret file present in working tree: ${relPath}`);
        leakCount++;
        break;
      }
    }

    // 3. Scan file contents for exposed secrets
    try {
      const stats = fs.statSync(fullPath);
      if (stats.size > 2 * 1024 * 1024) continue; // Skip files > 2MB

      const content = fs.readFileSync(fullPath, 'utf8');
      for (const secret of SECRET_PATTERNS) {
        if (secret.regex.test(content)) {
          console.log(`\x1b[31m[SECRET DETECTED]\x1b[0m ${secret.name} found in: ${relPath}`);
          leakCount++;
        }
      }
    } catch {
      // Skip non-readable or binary files
    }
  }
}

console.log('\x1b[36m============================================================\x1b[0m');
console.log('\x1b[36m   MetaFrontier NeuroTwin - Security & Credential Audit     \x1b[0m');
console.log('\x1b[36m============================================================\x1b[0m\n');

console.log('[AUDIT] Scanning workspace for credential leaks, .pem keys, and secrets...');
scanDirectory(ROOT_DIR);

// Verify .gitignore exists and contains critical rules
const gitignorePath = path.join(ROOT_DIR, '.gitignore');
let gitignoreValid = false;
if (fs.existsSync(gitignorePath)) {
  const giContent = fs.readFileSync(gitignorePath, 'utf8');
  if (giContent.includes('*.pem') && giContent.includes('.env') && giContent.includes('*password*')) {
    gitignoreValid = true;
  }
}

if (!gitignoreValid) {
  console.log('\x1b[31m[WARNING]\x1b[0m .gitignore is missing critical credential protection rules!');
  leakCount++;
} else {
  console.log('  \x1b[32m✔ PASS\x1b[0m: .gitignore credential rules verified.');
}

console.log(`\nScanned: ${scannedFiles} files across project directories.`);

if (leakCount === 0) {
  console.log('\x1b[1m\x1b[32m✔ AUDIT PASSED: Zero exposed secrets, private keys, or passwords detected.\x1b[0m\n');
  process.exit(0);
} else {
  console.log(`\x1b[1m\x1b[31m✖ AUDIT FAILED: ${leakCount} potential credential vulnerability issue(s) detected.\x1b[0m\n`);
  process.exit(1);
}
