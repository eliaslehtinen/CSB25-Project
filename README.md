# CSB25-Project

## Project 1 for the MOOC Cyber Security Base 2025 course

Software where users can be created, users can create and search their personal notes which are stored in a database. The project contains following flaws and their fixes:

Flaws (OWASP 2021)

## 1. A01 - Broken Access Control

- Flaw: If a user is logged in, they can access other users' notes by changing the url
- Fix: Verify that the user requesting notes view matches the owner of said notes

## 2. A02 - Cryptographic Failures

- Flaw: Passwords are stored in the database hashed using outdated unsalted MD5 hash. If attackers gain access to these hashes, they can crack the passwords by referencing a list of precalculated MD5 hashes.
- Fix: Use a salted hash. It's also important to use a modern secure algorithm like PBKDF2 with SHA256, which is the default Django 5.2 uses.

## 3. A03 - Injection

- Flaw: Raw user input is used in an sql query without any sanitization or validation. This allows an attacker to craft inputs which return data from elsewhere in the database (for example passwords).
- Fix: Use query parameterization or other existing secure ways to create queries.

## 4. A07 - Identification and Authentication Failures

- Flaw: No protection against brute force attacks. Attackers can gain access to an account by trying lots of common passwords.
- Fix: Prevent brute force attacks by limiting how many login attempts can be made in a short time.

## 5. A09 - Security Logging and Monitoring Failures

- Flaw: Security events such as logins and failed logins are not logged anywhere.
- Fix: Implement logging of important events and errors.
