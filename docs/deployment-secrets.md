# Deployment secrets for PR 1

Leolan's current NTP collector uses one temporary deployment-level CUCM SSH
credential. Configure both of these environment variables:

```text
CUCM_SSH_USERNAME
CUCM_SSH_PASSWORD
```

Do not place real values in source code, `.env.example`, logs, documentation,
or issue trackers.

## Production

Inject both values into the Leolan process environment using the deployment
system's secret mechanism. A process environment value takes precedence over
a local `.env` value.

The account should be a dedicated, least-privilege monitoring account. Rotate
it according to the customer's credential policy.

## Local development

Copy the empty variable names from `.env.example` into the ignored local
`.env` file and supply rotated development-only values. Never commit `.env` or
an environment-specific `.env.*` file.

If either variable is missing or blank, the NTP collection fails with a safe
configuration error. Leolan has no default or fallback CUCM credential.

## V1 limitation

PR 1 deliberately supplies one shared credential pair to all CUCM NTP checks
in a deployment. It does not store credentials in PostgreSQL, encrypt database
credentials, provide credential-management UI, or select credentials per
node. Those capabilities are deferred to PR 15 in the frozen V1 PRD.
