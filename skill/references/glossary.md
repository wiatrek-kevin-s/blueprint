# Glossary

Introduce a term when a decision needs it, because a list up front is forgotten.

## Terms

- **Frontend**: runs on the visitor's device; anyone can read it.
- **Backend, server**: code on a machine you control; secrets go here.
- **API**: how one program asks another for data or actions.
- **API key, secret**: a program's password; anyone holding it can act as you.
- **Environment variable**: a setting kept outside the code.
- **Public prefix** (`NEXT_PUBLIC_`, `VITE_`): marks a setting every visitor sees.
- **Database**: organised storage for the app's records.
- **Row-level security**: database rules on which rows each user may touch.
- **Authentication**: proving who you are; signing in.
- **Authorisation**: what a signed-in person may do.
- **Two-step sign-in (2FA)**: a second proof, such as a phone code.
- **Framework**: a ready-built skeleton for one kind of app.
- **Package, dependency**: someone else's code the project relies on.
- **Lockfile**: fixes exact package versions so builds repeat.
- **Repository**: the project's folder and its change history.
- **Git, commit**: the tool that records changes; a commit is one snapshot.
- **Branch**: a separate line of work, merged when ready.
- **Pull request**: a proposed change awaiting checks and approval.
- **CI**: automatic checks that run on every change.
- **Automated test**: a program that checks a feature still works.
- **Acceptance check**: a test with a visible pass mark for one task.
- **Deploy**: putting a new version live.
- **Hosting**: the service that runs the site or app.
- **Static site**: same pages for everyone, no sign-in; cheap and safe.
- **Test and live setups**: separate copies for building and for real use.
- **Domain, DNS**: the web address, and the directory pointing it at the host.
- **HTTPS**: the padlock: traffic to the site is encrypted.
- **Webhook**: an automatic notice from another service, such as "paid".
- **Rate limit**: a ceiling on repeated actions, such as sign-in tries.
- **Logging, monitoring**: a record of events, with alerts on failure.
- **Backup, restore**: a spare copy of the data, and putting it back.
- **Vulnerability**: a weakness someone can exploit.
- **Injection**: text typed into a form that the app wrongly runs as code.
- **Security scanner**: finds known mistakes, leaked keys or bad packages.
- **Prompt injection**: text that smuggles orders to an AI feature.
- **Vendor lock-in**: a provider that is costly to leave.
- **Open-source licence**: terms for reusing code: permissive (MIT) or copyleft (GPL).
- **One-way door**: a choice costly to undo; a two-way door is cheap to undo.
- **Design token**: a named visual value, such as a colour, set once.
- **Subagent**: a helper agent with a fresh context that returns a summary.
