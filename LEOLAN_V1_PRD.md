# Leolan V1 Product Requirements Document

**Status:** Approved source of truth  
**Product owner:** Founding CTO  
**Version:** 1.0  
**Date:** 14 July 2026  
**Target release:** First paid customer pilot

---

# 1. Product Vision

## 1.1 Decision

Leolan V1 is **Cisco UC Daily Operational Assurance**.

It is a customer-hosted application that performs a small set of automated, read-only health checks against Cisco Unified Communications Manager environments and delivers one actionable daily exception report. It shows what is healthy, what requires attention, when each check last succeeded, and whether Leolan itself has stopped collecting.

Leolan V1 will initially be sold through a paid readiness and onboarding engagement. During that engagement, Leolan establishes a baseline, identifies existing risks, and remains installed as a recurring operational-assurance subscription.

The commercial sequence is:

1. Sell a fixed-scope paid readiness/onboarding engagement.
2. Install Leolan in the customer's environment.
3. Identify current operational risks.
4. Deliver daily assurance continuously.
5. Convert or continue under a recurring subscription.

The readiness engagement is the sales wedge. The recurring daily assurance service is the product.

## 1.2 V1 product outcome

Every morning, a Cisco UC operator receives one report answering:

- Did every configured CUCM node respond?
- Is database replication healthy?
- Is the latest DRS backup recent and successful?
- Are required Cisco services running?
- Are certificates approaching expiration?
- Are disk or log partitions approaching dangerous capacity?
- Are nodes synchronized to NTP?
- Did every Leolan check run successfully, or is monitoring stale?
- What requires action today?

## 1.3 What Leolan V1 is

- A narrow Cisco CUCM operational-assurance product.
- A read-only collector and interpretation layer.
- A daily exception report and minimal current-status console.
- A central record of current health and recent check execution.
- A customer-hosted, single-customer deployment.
- A founder-assisted product with white-glove onboarding.
- A recurring subscription following a paid setup/readiness engagement.

## 1.4 What Leolan V1 is not

Leolan V1 is not:

- A generic infrastructure-monitoring platform.
- A replacement for Cisco RTMT, Cisco TAC, or existing NMS tools.
- A real-time call-quality analytics product.
- A packet capture or voice-path analysis product.
- A topology-discovery platform.
- A configuration-management or automated-remediation system.
- A multi-tenant public SaaS control plane.
- A full incident-management or ticketing system.
- A full upgrade orchestration product.
- A system that changes CUCM configuration.
- A system that runs disruptive repair or reset commands.
- A full RBAC, audit, SLA, or compliance platform.
- A customer self-service provisioning portal.
- A polished dashboard suite.

If a proposed feature does not improve the daily report, the current-status console, safe collection, or paid onboarding, it is outside V1.

---

# 2. Target Customer

## 2.1 Primary initial customer

The primary Customer #1 profile is:

- A managed service provider or enterprise with a dedicated Cisco UC operational owner.
- Responsible for at least two CUCM clusters or approximately 10–100 CUCM nodes.
- Performs recurring manual checks or relies on fragmented RTMT/email monitoring.
- Has an upcoming upgrade, recent operational incident, audit requirement, or visible concern about backup and replication readiness.
- Can deploy a small customer-hosted application with outbound or internal access to PostgreSQL/InfluxDB as required.
- Can provide read-only or least-privilege CUCM platform access.

MSPs are preferred because one relationship can expose Leolan to multiple managed environments and the daily report supports an existing service-delivery workflow.

## 2.2 Buyer

The likely commercial buyer is one of:

- UC manager.
- Collaboration practice lead.
- MSP service-delivery manager.
- Infrastructure operations manager.
- Director responsible for enterprise communications availability.

The buyer purchases reduced operational risk, repeatable evidence, and lower manual effort. The buyer does not purchase collectors, parsers, or dashboards.

## 2.3 Primary users

- Cisco UC administrators.
- UC operations engineers.
- NOC engineers responsible for first-line review.
- MSP engineers responsible for multiple customer environments.

Their daily job is to review exceptions, validate evidence, and act using existing Cisco procedures.

## 2.4 Technical approvers

- Enterprise security or network security.
- Infrastructure/platform owner.
- Cisco UC technical lead.
- Database/virtualization team if hosting dependencies require approval.

## 2.5 Economic approver

- UC or infrastructure budget owner.
- MSP practice director or managed-services owner.
- Procurement for the paid pilot or subscription.

## 2.6 Typical company size

- Enterprise: 1,000–50,000 employees.
- MSP: manages at least five Cisco UC customer environments.

Smaller environments are not excluded, but they are less likely to experience enough operational repetition to justify the initial price.

## 2.7 Typical Cisco environment

V1 targets:

- Cisco Unified Communications Manager 12.5, 14, or 15, subject to validation during onboarding.
- One or more CUCM clusters.
- Publisher and subscriber nodes.
- Customer-managed or partner-managed deployment.
- SSH access to the CUCM platform CLI through a least-privilege account where supported.
- DRS configured for scheduled backup.
- Existing RTMT usage, often inconsistent or local to individual engineers.

Unity Connection, IM and Presence, UCCX, Expressway, gateways, and endpoints are future product scope unless explicitly contracted as a paid custom extension after V1 acceptance.

---

# 3. Customer Problem

## 3.1 Core problem

Cisco UC teams cannot quickly answer whether their CUCM estate is operationally healthy and recoverable without checking multiple tools, pages, reports, emails, and CLI commands.

Important degradation can remain silent until:

- A user reports an outage.
- An upgrade fails.
- A restore is required.
- A certificate expires.
- A partition fills.
- A subscriber contains stale database data.
- A critical service remains down.
- The team discovers that monitoring itself stopped.

The underlying data often exists. The operational answer does not.

## 3.2 Current customer workflow

Customers typically combine some of the following:

- Cisco RTMT alerts and counters.
- CUCM OS Administration.
- Cisco Unified Serviceability.
- DRS administration pages and email notifications.
- Cisco Unified Reporting.
- Manual SSH commands.
- Generic SNMP or infrastructure monitoring.
- Spreadsheets for certificate and upgrade tracking.
- Engineer memory and informal runbooks.
- Manual morning or weekly health checks.
- Cisco TAC evidence collection after an incident begins.

This workflow is fragmented and person-dependent. It is difficult to prove that checks occurred consistently and difficult for managers or MSP customers to consume.

## 3.3 Why existing tools are insufficient

Leolan does not claim that Cisco provides no monitoring. The problem is operational consolidation and interpretation:

- RTMT is broad but requires configuration, local expertise, and active attention.
- Native email alerts can be misconfigured, noisy, missed, or routed to former employees.
- Generic monitoring sees servers and metrics but often lacks Cisco UC-specific interpretation.
- DRS job configuration does not prove that a recent complete backup exists.
- Replication health requires interpretation of Cisco-specific states and timestamps.
- Individual product pages do not provide one estate-level exception report.
- MSPs repeat the same manual checks for each customer.
- Monitoring products rarely show clearly that their own data has become stale.

## 3.4 Business consequences

- Longer time to identify UC problems.
- Avoidable outages from predictable conditions.
- Failed or risky upgrades.
- False confidence in backups or monitoring.
- Repeated high-cost engineering work.
- Poor evidence for customer reviews and operational governance.
- Dependence on a small number of experienced UC engineers.

---

# 4. Product Promise

> **Every morning, Leolan tells your UC team which CUCM clusters are healthy, what requires action, and whether your monitoring evidence is current—without manually checking RTMT, CLI, DRS, certificates, and system pages.**

---

# 5. MVP Scope

## 5.1 Included monitoring checks

### A. Node collection status

For every configured CUCM node, Leolan must report:

- Reachable and authenticated.
- Collection succeeded.
- Collection failed.
- Collection stale.
- Monitoring disabled.
- Last attempt.
- Last success.
- Current error, without exposing credentials.

### B. Database replication assurance

For each configured CUCM cluster:

- Execute the supported read-only replication-status command on the publisher.
- Parse cluster and node replication state.
- Identify healthy, initializing, mismatched, failed, unknown, or stale state.
- Retain the relevant current evidence.
- Explain the affected nodes and observed state.
- Never execute replication repair, reset, stop, or mutation commands.

### C. DRS backup assurance

For each configured cluster, using the least risky supported data source available during implementation:

- Identify the latest attempted backup.
- Identify the latest successful backup.
- Identify failed, incomplete, or stale backup state.
- Report backup age.
- Report included or missing components where available.
- Report collection uncertainty as `UNKNOWN`, not healthy.

V1 does not perform restores or claim recoverability. It reports backup-job assurance only.

### D. Critical service assurance

- Collect current service status from each node.
- Compare against a Leolan-owned, versioned list of services required for the contracted deployment.
- Report stopped required services.
- Distinguish unreachable node from stopped service.
- Avoid automatically restarting services.

The required-service list is configured by Leolan during onboarding, not by a customer-facing rule builder.

### E. Certificate expiry assurance

- Inventory certificates accessible through the selected safe interface.
- Record subject/name, node, purpose where available, issuer, and expiry time.
- Classify expired, critical, warning, and acceptable.
- Default thresholds: expired, 0–14 days, 15–45 days, and over 45 days.
- Allow deployment-level threshold configuration.
- Avoid certificate renewal, upload, regeneration, or revocation.

### F. Disk and log-partition assurance

- Collect active, inactive, and logging partition use where supported.
- Report threshold breaches.
- Default thresholds: warning at 80%, critical at 90%.
- Allow deployment-level threshold configuration.
- Do not implement forecasting in V1.

### G. NTP assurance

- Collect NTP status from each node.
- Identify current synchronization state and active peer.
- Record peer, stratum, reach, offset, and jitter when available.
- Report no active peer, no synchronization, invalid output, and stale collection distinctly.

## 5.2 Included product interfaces

### Daily exception report

One scheduled report per deployment containing:

- Report generation time.
- Environment and cluster coverage.
- Total checks expected and completed.
- Critical findings.
- Warning findings.
- Unknown or stale findings.
- Healthy summary.
- Affected node/cluster.
- Human-readable reason.
- Last successful observation.
- Link to the current-status console where available.

Delivery order for V1:

1. Email.
2. Optional Microsoft Teams webhook only if required by Customer #1.

### Current-status console

One authenticated read-only page showing:

- Cluster and node.
- Check name.
- Current status: healthy, warning, critical, unknown, stale, or disabled.
- Current message.
- Last attempted collection.
- Last successful collection.
- Filter: all versus action required.

One simple node detail page may show current evidence for each check. No dashboard builder is included.

### Manual execution

An administrator may request a safe re-run of one check for one node or cluster. The request must respect the same lock and concurrency limits as scheduled monitoring.

## 5.3 Included onboarding

Onboarding is performed by Leolan personnel and includes:

- Environment questionnaire.
- Supported-version confirmation.
- Network and access validation.
- Secure credential installation.
- Customer, cluster, and node configuration.
- Required-service baseline configuration.
- Monitoring schedule configuration.
- Initial readiness/baseline report.
- Review workshop with the customer.

The customer does not require a self-service onboarding UI in V1.

## 5.4 Included history

- PostgreSQL stores current inventory, current check state, current health, and latest execution state.
- InfluxDB stores limited historical check status and duration required for evidence and trend display.
- The V1 UI does not expose a general historical analytics experience.
- Default historical retention is 90 days unless customer policy requires less.

## 5.5 Explicitly excluded from V1

- Phone registration monitoring.
- SIP trunk and gateway monitoring.
- Voice-quality or CDR/CMR analytics.
- Call-path analysis.
- Unity Connection, IM&P, UCCX, Expressway, and contact-center monitoring.
- Endpoint inventory and lifecycle management.
- Automated discovery.
- Topology visualization.
- Automated remediation.
- Replication repair or reset.
- Service restart.
- Certificate renewal or regeneration.
- Backup restore testing.
- Upgrade execution or orchestration.
- Incident correlation and root-cause analysis.
- Alert deduplication platform.
- Ticketing-system integration.
- SMS, PagerDuty, or broad notification integrations.
- Multi-tenant public SaaS.
- Customer-created collectors or plugins.
- Customer-editable health rules.
- Full customer CRUD UI.
- Full monitoring-profile administration UI.
- Fine-grained enterprise RBAC.
- SSO/SAML/OIDC unless Customer #1 makes it a paid deployment condition.
- Mobile application.
- Localization.
- AI-generated diagnosis.
- SLA calculation.
- Capacity forecasting.
- Compliance certification.
- Kubernetes.

---

# 6. User Workflow

## 6.1 Commercial and readiness workflow

1. Leolan qualifies the prospect's CUCM estate and operational pain.
2. Customer and Leolan agree on a paid onboarding/readiness engagement and recurring subscription terms.
3. Customer identifies the UC technical owner, infrastructure owner, and security approver.
4. Leolan provides the deployment and access requirements.
5. Customer approves a customer-hosted deployment and least-privilege access.
6. Leolan installs and configures V1.
7. Leolan runs an initial baseline assessment.
8. Leolan and the customer review findings and correct configuration false positives.
9. Daily assurance begins.

## 6.2 Installation workflow

1. Provision one supported Windows or Linux host/VM according to the agreed deployment package.
2. Provision PostgreSQL and InfluxDB using the documented supported topology.
3. Configure TLS termination and network access.
4. Install the pinned Leolan release.
5. Install deployment secrets outside source control.
6. Run schema migration/bootstrap.
7. Run readiness validation.
8. Create the initial Leolan administrator.
9. Start exactly one scheduler instance.
10. Confirm application, scheduler, PostgreSQL, and InfluxDB health.

V1 may use Docker Compose if it is the fastest reliable deployment path, but Kubernetes is prohibited.

## 6.3 Configuration workflow

1. Customer supplies an approved inventory template containing clusters and nodes.
2. Leolan personnel import or enter the configuration using an internal administrative command or narrowly scoped setup endpoint.
3. Credentials are installed securely and associated with nodes.
4. Leolan tests reachability and authentication.
5. Leolan identifies the publisher for cluster-level checks.
6. Leolan applies the fixed V1 check set and default schedule.
7. Leolan configures expected services and customer-approved thresholds.
8. Leolan runs all checks once.
9. Customer validates representative results directly against CUCM.
10. Leolan activates the daily report.

## 6.4 Monitoring workflow

1. Scheduler loads enabled nodes and their fixed V1 check assignments.
2. Scheduler determines which checks are due.
3. Scheduler refuses to overlap the same node/cluster and check.
4. Worker starts an execution-state record.
5. Collector performs a read-only operation with a hard deadline.
6. Parser validates and structures the response.
7. Evaluator assigns health status and explanation.
8. PostgreSQL current state is updated.
9. InfluxDB receives historical status/duration where configured.
10. Execution is marked successful or failed exactly once.
11. Stale-state evaluation occurs independently of successful collection.

## 6.5 Daily user workflow

1. Operator receives the daily report.
2. Operator reviews `CRITICAL`, then `WARNING`, then `UNKNOWN/STALE` findings.
3. Operator opens the status console for evidence.
4. Operator confirms or investigates using existing Cisco procedures.
5. Operator may request one manual recheck.
6. Operator handles remediation outside Leolan.

Leolan V1 does not manage acknowledgement, assignment, or incident closure.

## 6.6 Incident workflow

During an incident:

1. Operator opens Leolan to determine whether the latest assurance evidence is current.
2. Operator reviews node reachability, last successful checks, replication, services, disk, certificates, backup, and NTP state.
3. Operator manually re-runs a safe relevant check if the cluster can tolerate it.
4. Operator copies or exports the current evidence for internal escalation or TAC.
5. Troubleshooting and remediation continue in the customer's existing tools.

Leolan provides context; it does not claim automated root cause.

---

# 7. Functional Requirements

## 7.1 Must Have

### Product and inventory

- **M-001:** Support one customer per deployment.
- **M-002:** Store clusters and CUCM nodes with stable IDs, hostname, IP address, role, version, enabled state, and publisher designation.
- **M-003:** Provide a founder-operated import or setup mechanism; a customer-facing CRUD UI is not required.
- **M-004:** Store or reference credentials without hardcoding or displaying passwords.

### Collection safety

- **M-005:** Execute only an allowlisted set of read-only commands or API operations.
- **M-006:** Apply connection, authentication, and command deadlines.
- **M-007:** Close every connection on success, failure, and timeout.
- **M-008:** Prevent simultaneous execution of the same check against the same target.
- **M-009:** Enforce conservative global concurrency and per-node concurrency.
- **M-010:** Never accept unknown SSH host keys silently in production.
- **M-011:** Distinguish authentication, connectivity, timeout, parser, configuration, and storage errors.

### Checks

- **M-012:** Implement node collection-state assurance.
- **M-013:** Implement database-replication assurance.
- **M-014:** Implement DRS backup-job assurance using a source validated for Customer #1.
- **M-015:** Implement critical-service assurance.
- **M-016:** Implement certificate-expiry assurance.
- **M-017:** Implement disk/log-partition assurance.
- **M-018:** Implement NTP assurance.
- **M-019:** Return `UNKNOWN` for missing, unsupported, or unparseable evidence; never infer healthy.
- **M-020:** Validate all parsers against captured output from the customer's supported CUCM versions.

### State and health

- **M-021:** Maintain one current result per target and check.
- **M-022:** Maintain last attempt, last success, last failure, duration, status, and error summary.
- **M-023:** Mark a result stale after a configurable number of missed expected intervals.
- **M-024:** Record each execution outcome exactly once.
- **M-025:** Preserve enough evidence to explain every non-healthy result without storing credentials.
- **M-026:** Use the statuses `HEALTHY`, `WARNING`, `CRITICAL`, `UNKNOWN`, `STALE`, and `DISABLED` consistently.

### Reporting and UI

- **M-027:** Generate one daily exception report at a configured local time.
- **M-028:** Deliver the report by email.
- **M-029:** Report expected checks, completed checks, and missing/stale checks.
- **M-030:** Provide one authenticated current-status page.
- **M-031:** Filter the status page between all results and action-required results.
- **M-032:** Provide current evidence and timestamps for a selected node/check.
- **M-033:** Permit an administrator to request one safe manual recheck.

### Administration and access

- **M-034:** Require authentication for all UI and API access, unless the deployment contract explicitly places all access behind an approved identity-aware proxy.
- **M-035:** Support one administrator role and one read-only operator role, or delegate those roles to the approved proxy.
- **M-036:** Reject unrestricted mass assignment and accept explicit request fields only.
- **M-037:** Provide clear validation and not-found responses on active endpoints.

### Platform operation

- **M-038:** Expose application readiness, scheduler heartbeat, last completed check, PostgreSQL connectivity, and InfluxDB connectivity.
- **M-039:** Refuse startup or mark not-ready when required configuration is invalid.
- **M-040:** Ensure only one active scheduler per deployment.
- **M-041:** Support graceful shutdown without accepting new work.
- **M-042:** Provide a repeatable fresh installation and upgrade procedure.

## 7.2 Should Have

- **S-001:** Microsoft Teams webhook delivery if Customer #1 uses Teams operationally.
- **S-002:** CSV export of the current report.
- **S-003:** Basic report branding with customer name and Leolan support contact.
- **S-004:** Manual suppression of one known finding until a specified time, only if report noise blocks acceptance.
- **S-005:** A deployment-level override for report thresholds and check intervals.
- **S-006:** A simple historical status view for the previous seven days.
- **S-007:** A machine-readable JSON endpoint for current assurance status.
- **S-008:** A clear `monitoring disabled` state rather than omitting disabled targets.

Should-Have work may enter V1 only after all Must-Have acceptance criteria pass or when Customer #1 makes it a condition of payment.

## 7.3 Could Have

- **C-001:** PDF report export.
- **C-002:** Customer logo.
- **C-003:** Simple acknowledgement note attached to a finding.
- **C-004:** One additional Cisco product check funded by Customer #1.
- **C-005:** Seven- or thirty-day sparkline charts.
- **C-006:** Scheduled weekly management summary.

Could-Have items are not release requirements.

## 7.4 Won't Have in V1

- **W-001:** Public multi-tenant SaaS.
- **W-002:** Automatic discovery.
- **W-003:** Topology maps.
- **W-004:** Automated remediation.
- **W-005:** Phone registration, trunks, gateways, or call quality.
- **W-006:** Incident/ticket workflow.
- **W-007:** Customer rule builder.
- **W-008:** Plugin marketplace or dynamic collector loading.
- **W-009:** AI diagnosis.
- **W-010:** Full upgrade orchestration.
- **W-011:** Restore testing.
- **W-012:** Full enterprise RBAC or SSO unless contractually required.
- **W-013:** Mobile application.
- **W-014:** Kubernetes support.
- **W-015:** General-purpose observability features.

---

# 8. Non-functional Requirements

## 8.1 Performance

- V1 must support the contracted Customer #1 environment up to 100 CUCM nodes.
- Default global worker concurrency must not exceed 10 without an explicit deployment override.
- Per-node concurrent collection must be 1.
- The current-status page should load within 3 seconds for 100 nodes under normal conditions.
- The daily report should generate within 5 minutes after the reporting schedule.
- Collection intervals must default to operationally conservative values; no V1 check requires sub-minute polling.
- A slow target must not prevent other targets from executing.

## 8.2 Security

- No credentials in source code, logs, reports, URLs, or API responses.
- Rotate all credentials previously present in development artifacts before customer deployment.
- Store secrets outside source control.
- Encrypt stored reversible secrets using a deployment key outside PostgreSQL, or use an approved external secret store.
- Use least-privilege CUCM access and document required permissions.
- Pin and verify SSH host keys after explicit enrollment.
- Use TLS for user access.
- Restrict network access to approved sources and destinations.
- Protect all mutation endpoints from unauthorized access and CSRF where browser forms are used.
- Use explicit schemas and field allowlists.
- Avoid collecting unnecessary customer data.
- Provide a documented secret-rotation procedure.

V1 is not required to achieve a formal compliance certification.

## 8.3 Reliability

- A check failure must never crash the scheduler.
- A parser failure must never be reported as healthy.
- Execution success/failure must be recorded once.
- Every external operation must have a deadline.
- Connections and sessions must be released after every execution.
- Duplicate scheduler instances must be prevented operationally or technically.
- Stale monitoring must be visible independently of device health.
- PostgreSQL failure must produce an unhealthy application readiness state.
- InfluxDB history failure must be visible; it must not silently erase the current PostgreSQL result.
- Daily report generation failure must alert Leolan support through a deployment-specific channel.
- The release candidate must complete a 72-hour soak test at expected pilot scale.

## 8.4 Deployment

- Customer-hosted, single-customer deployment.
- One documented supported topology.
- One pinned release artifact.
- One schema migration/bootstrap command.
- One readiness command or endpoint.
- One rollback procedure to the previous release.
- Configuration separated from code.
- No Kubernetes requirement.
- Multiple web workers are allowed only if scheduler execution is isolated to one process; the default V1 deployment should use one application process.

## 8.5 Scalability

V1 is designed for 100 nodes, not internet scale.

- PostgreSQL stores current state, not unbounded execution history.
- InfluxDB stores bounded historical telemetry.
- No distributed queue is required.
- No configuration cache is required unless measurements show the Customer #1 deployment needs it.
- No horizontal scheduler scaling is required.
- Multi-customer tenancy is explicitly deferred.

## 8.6 Logging

Every execution log must include:

- Timestamp in UTC.
- Severity.
- Execution/correlation ID.
- Customer deployment identifier.
- Cluster ID where applicable.
- Node ID and hostname where applicable.
- Check key.
- Outcome.
- Duration.
- Safe error category and message.

Logs must not include passwords, tokens, private keys, full connection strings, or raw command output containing sensitive data.

Production Paramiko debug logging is disabled by default.

## 8.7 Backups

- Document PostgreSQL backup and restore.
- Back up application configuration and encrypted credential references.
- InfluxDB history may use the customer's standard backup/retention policy; loss of historical telemetry must not prevent current monitoring from restarting.
- Test PostgreSQL restore before Customer #1 acceptance.
- Document recovery order and expected recovery time.
- Leolan's backup procedure must not be confused with the CUCM DRS assurance feature.

---

# 9. Architecture Mapping

## 9.1 Existing component disposition

| Existing component | V1 disposition | Required action |
|---|---|---|
| `main.py` | Needs modification | Keep FastAPI host. Replace deprecated startup event with controlled lifecycle if necessary. Ensure exactly one scheduler. Register only V1 routes. Fix template root. Add readiness and authentication boundary. |
| `app/core/config/settings.py` | Needs modification | Consolidate duplicate setting names, remove required unused OpenAI key, validate V1 settings, add report/security settings. |
| `app/core/logging/logger.py` | Needs modification | Add structured execution context and secret-safe logging. |
| `app/core/scheduler/scheduler.py` | Needs modification | Keep database-driven scheduling where useful. Use stable target IDs, add locks, stale evaluation, shutdown, conservative intervals, and single-scheduler enforcement. |
| `app/core/scheduler/worker_pool.py` | Needs modification | Reduce default concurrency and support graceful shutdown. |
| `app/core/scheduler/job_registry.py` | Needs modification | Keep a static allowlisted registry. Add only the six V1 assurance jobs. Do not implement dynamic loading. |
| `app/core/scheduler/scheduler_old.py` | Can be deleted | Obsolete architecture; not part of V1. |
| `app/core/dispatcher/metric_dispatcher.py` | Needs modification | Make lifecycle handling single-layer, prevent unbound state and double failure updates, categorize errors, enforce one final outcome. |
| `app/core/ssh/client.py` | Needs modification | Add host-key verification, hard deadlines, configured timeouts, safe cleanup, output limits, and allowlisted use. |
| `app/core/ssh/connection_pool.py` | Can be deleted or ignored | Connection pooling is not required for V1. Delete if unused to avoid false assumptions. |
| `app/core/ssh_client.py` | Can be deleted | Old duplicate SSH implementation and production debug-log source. |
| `app/core/ssh/exceptions.py` | Already useful | Keep and extend only if needed for explicit safe error categories. |
| `app/db/session.py` | Needs modification | Use the single canonical declarative Base and validated engine/session configuration. |
| `app/db/base.py` | Already implemented | Make this the only declarative Base. |
| `app/db/create_tables.py` | Replace | Replace ad hoc `create_all` deployment with a repeatable migration/bootstrap process. |
| `app/db/events/system_events.py` | Needs modification | Keep only if system-code generation remains necessary. Fix concurrency and constraint behavior; otherwise simplify IDs and remove customer-visible sequencing from V1. |
| `app/inventory/models/customer.py` | Needs modification | Retain single-customer deployment identity. Remove obsolete UI field assumptions. |
| `app/inventory/models/system.py` | Needs modification | Treat System as CUCM cluster. Fix overwritten constraints and clarify publisher relationship through nodes/configuration. |
| `app/inventory/models/node.py` | Needs modification | Retain NodeBase and CUCM details. Add enabled/publisher designation if absent. Remove unused node-level profile field if not used in V1. |
| `app/inventory/models/credential.py` | Needs modification | Do not store plaintext passwords. Integrate encrypted secret reference or deployment secret mechanism. |
| Monitoring capability/profile/implementation models | Simplify and retain | Keep only if they accelerate fixed check assignment. Seed fixed V1 definitions. Do not expose generic configuration to customers. |
| `NodeMonitoringOverride` | Needs modification | Support enable/disable and interval override internally. Register no broad customer UI. |
| `MonitoringExecutionState` | Needs modification | Keep current-state design. Correct UUID types, lifecycle semantics, stale state, and counters. Avoid historical rows in PostgreSQL. |
| `NodeMetricState` | Already useful | Keep current parsed evidence per check. Add safe evidence limits if needed. |
| `NodeHealthComponent` | Needs modification | Reuse as one current assurance result per node/check or replace with a clearer `AssuranceResult`; do not maintain overlapping representations. |
| `NodeHealth` | Needs modification | Optional cluster/node summary only. Do not use arbitrary averaged health scores as the primary V1 output. Worst actionable status wins. |
| `HealthScore` | Can be deleted | Redundant legacy model with no V1 business value. |
| Alert/Incident/IncidentAlert models | Can be deleted or excluded | V1 uses findings in current assurance state, not a full alert/incident platform. Do not expose these models. |
| MaintenanceEvent | Excluded from V1 | Do not build maintenance workflow. It may remain dormant if deletion complicates migrations. |
| User/AuditLog models | Needs modification / exclude | Use User only for minimal authentication if not delegated to proxy. Full audit-log product is excluded. |
| Service model | Needs modification | Existing generic service entity does not represent required Cisco process state cleanly. Use fixed expected-service configuration and current assurance results. |
| Inventory Pydantic schemas | Needs modification | Keep explicit schemas only for active setup/status endpoints. Remove duplicate `NodeCreate` definitions and generic dictionary updates. |
| Customer/System/Node APIs | Needs modification | Narrow to setup and read needs. Protect endpoints, validate missing records, fix route ordering, and remove obsolete behavior. |
| Monitoring configuration APIs | Exclude from public V1 | Internal setup only. Generic CRUD is not a customer feature. |
| Override API | Internal only | Register only if needed by founder setup. |
| Health API | Replace | Provide real readiness and assurance-status APIs. |
| Alert/Incident/Maintenance/Service APIs | Can be deleted or excluded | Empty or non-V1. |
| `app/inventory/services/execution_state_service.py` | Needs modification | Keep latest-state service; fix lifecycle fields and idempotent finalization. |
| `node_metric_state_service.py` | Needs modification | Remove debug print and make safe current-state upsert. |
| `node_health_component_service.py` | Needs modification | Align with explicit V1 statuses and avoid arbitrary score dependence. |
| `node_service.py` | Needs modification | Return only enabled, valid configured targets and avoid FastAPI concerns in domain services. |
| `app/monitoring/jobs/cucm/ntp_job.py` | Needs modification | Reuse the orchestration pattern after fixing collector, parser, writer, and health semantics. |
| NTP collector | Needs modification | Remove hardcoded credentials, guarantee cleanup, apply deadlines, use secret provider. |
| NTP parser | Needs modification | Validate unsupported output explicitly and retain parser fixtures. |
| NTP writer | Needs modification | Write every peer, handle empty values, and correct synchronization mapping. |
| NTP evaluator | Needs modification | Keep explicit status/reason; validate thresholds. Avoid unsupported numeric score semantics. |
| Health engine/registry | Simplify and retain | Static evaluator registry is adequate. Add V1 check evaluators only. |
| Node health aggregator | Needs modification | Use worst actionable state and stale/unknown semantics. Do not average unrelated checks into a misleading score. |
| Telemetry execution writer | Needs modification | Keep only bounded status/duration history. Ensure telemetry failure is visible and does not corrupt current state. |
| Old show-status collector | Can be deleted | Uses obsolete imports and node dictionaries. Replace with new V1 disk/service jobs. |
| Empty collector/parser/job modules | Can be deleted | Add implementations only when required by the six V1 checks. Empty placeholders are not architecture. |
| CPU/memory/system/disk legacy writers | Can be deleted or replaced | Reuse only code proven compatible with the V1 job architecture. Do not preserve obsolete interfaces. |
| Jinja templates | Replace selectively | Keep a minimal base, status list, detail page, login if required, and error page. Remove or hide obsolete CRUD and navigation. |
| Static CSS/JS | Simplify | Use minimal local assets. Do not depend on external CDN assets if customer policy forbids them. |
| Existing tests | Replace | Retain useful raw sample output. Build focused automated tests around V1 parsers, dispatcher, scheduler decisions, stale state, and report generation. |
| `requirements.txt` | Needs modification | Pin production versions, remove duplicate and unused packages including OpenAI unless explicitly required later. |
| `.env.example` | Needs modification | Document only V1 configuration; never include real values. |
| `.env`, logs, bytecode, local venv | Delete from release artifact | Never distribute customer secrets, development logs, virtual environment, or bytecode residue. |

## 9.2 New V1 work

New components required:

- Canonical database migration baseline.
- Secure credential provider/encryption boundary.
- Per-target/check execution lock.
- Stale-result evaluator.
- Database replication collector/parser/evaluator/job.
- DRS backup collector/parser/evaluator/job.
- Critical-service collector/parser/evaluator/job.
- Certificate collector/parser/evaluator/job.
- Disk/log partition collector/parser/evaluator/job.
- Daily report generator.
- Email report delivery.
- Minimal status API and UI.
- Authentication or approved identity-aware proxy integration.
- Readiness and scheduler-heartbeat endpoints.
- Founder-operated inventory import/setup command.
- Production deployment and backup/restore runbooks.

## 9.3 Architecture rule

Each V1 assurance job must follow:

```text
schedule -> lock -> collect -> validate/parse -> evaluate -> persist current state
         -> optionally persist history -> finalize execution exactly once
```

Collectors communicate. Parsers structure and validate. Evaluators interpret. Persistence services store. Jobs orchestrate. The dispatcher owns execution lifecycle.

This separation is retained because it directly reduces false health results and supports adding future UC checks. No additional framework abstraction is required.

---

# 10. Release Plan

Every pull request must have one objective, be independently mergeable, preserve a deployable application, and take less than two working days. A PR may introduce a disabled feature flag until its end-to-end dependencies exist, but it must not break the current deployment.

## Phase A — Safe deployable baseline

### PR 1 — Remove exposed runtime secrets

**Objective:** Remove hardcoded CUCM credentials and production Paramiko debug logging.  
**Acceptance:** Runtime obtains credentials from a temporary deployment-secret interface; no password appears in source or logs.

### PR 2 — Canonical SQLAlchemy metadata

**Objective:** Make `app.db.base.Base` the single declarative Base.  
**Acceptance:** All active models register on one metadata object; application starts against development schema.

### PR 3 — Correct critical schema defects

**Objective:** Fix System constraints and execution-state foreign-key types.  
**Acceptance:** Fresh PostgreSQL schema can enforce active relationships and constraints.

### PR 4 — Establish migration baseline

**Objective:** Add one repeatable migration/bootstrap path for a clean database.  
**Acceptance:** Empty database can be created using one documented command.

### PR 5 — Pin the V1 runtime

**Objective:** Pin required dependencies and remove duplicate/unused requirements.  
**Acceptance:** Clean environment installs and starts without undeclared dependencies.

### PR 6 — Startup/readiness validation

**Objective:** Validate required settings, PostgreSQL, and InfluxDB.  
**Acceptance:** Invalid deployments fail clearly or report not-ready.

### PR 7 — Minimal access boundary

**Objective:** Protect all routes using the selected V1 authentication or proxy contract.  
**Acceptance:** Unauthenticated access is denied; admin and read-only behavior is demonstrated.

### PR 8 — Safe SSH transport

**Objective:** Add host-key verification, deadlines, cleanup, output limits, and safe errors.  
**Acceptance:** Connection, authentication, timeout, and command failures are distinct and bounded.

### PR 9 — Execution locking

**Objective:** Prevent duplicate target/check execution.  
**Acceptance:** A second concurrent execution is rejected or skipped safely.

### PR 10 — Dispatcher lifecycle correctness

**Objective:** Finalize every execution exactly once.  
**Acceptance:** Success and all failure paths update state once without unbound variables.

### PR 11 — Scheduler safety

**Objective:** Use stable IDs, conservative workers, stop event, and single scheduler.  
**Acceptance:** Scheduler starts once, shuts down gracefully, and isolates job failures.

## Phase B — Trustworthy current assurance state

### PR 12 — Explicit assurance statuses

**Objective:** Introduce consistent healthy/warning/critical/unknown/stale/disabled semantics.  
**Acceptance:** Current-state schemas and services support every V1 status.

### PR 13 — Stale-state evaluation

**Objective:** Detect missing expected results independently of device health.  
**Acceptance:** Missed intervals produce `STALE` after the configured threshold.

### PR 14 — Founder inventory import

**Objective:** Import one customer, clusters, nodes, roles, and enabled state from a controlled file.  
**Acceptance:** A clean deployment can be configured without direct SQL or customer CRUD UI.

### PR 15 — Encrypted credential references

**Objective:** Replace temporary secret access with the approved V1 secure credential mechanism.  
**Acceptance:** Stored database contents do not reveal usable device passwords.

## Phase C — V1 checks

### PR 16 — NTP parser fixtures

**Objective:** Validate NTP parsing against healthy, unhealthy, empty, and malformed samples.  
**Acceptance:** Unsupported evidence returns `UNKNOWN` and tests pass.

### PR 17 — NTP collection and persistence correction

**Objective:** Make NTP end-to-end safe and accurate.  
**Acceptance:** Every peer is stored, sync state is correct, empty peers do not crash, and execution state is correct.

### PR 18 — Disk/status parsing

**Objective:** Implement validated partition parsing from supported customer output.  
**Acceptance:** Active, inactive, and logging partitions produce structured results or `UNKNOWN`.

### PR 19 — Disk assurance job

**Objective:** Schedule, evaluate, and persist disk/log partition assurance.  
**Acceptance:** Thresholds produce correct current results.

### PR 20 — Critical-service parsing

**Objective:** Parse supported service-list output and distinguish service state.  
**Acceptance:** Captured customer fixtures cover running, stopped, and unsupported output.

### PR 21 — Critical-service assurance job

**Objective:** Compare observed services with the onboarding baseline.  
**Acceptance:** Required stopped services produce actionable findings; no restart occurs.

### PR 22 — Replication parser

**Objective:** Parse supported replication states and timestamps.  
**Acceptance:** Healthy, initializing, mismatch, failure, and incomplete samples are tested.

### PR 23 — Replication assurance job

**Objective:** Run the safe publisher check and persist cluster/node findings.  
**Acceptance:** One cluster result identifies affected nodes and never executes repair commands.

### PR 24 — Certificate inventory parser

**Objective:** Parse certificate identity and expiry from the selected supported interface.  
**Acceptance:** Expired, expiring, valid, and unknown evidence is tested.

### PR 25 — Certificate assurance job

**Objective:** Persist and classify certificate expiry findings.  
**Acceptance:** Configured thresholds produce actionable results without certificate mutation.

### PR 26 — DRS evidence adapter

**Objective:** Collect and parse the Customer #1-approved backup status source.  
**Acceptance:** Latest attempt, latest success, components, and error evidence are structured or unknown.

### PR 27 — DRS assurance job

**Objective:** Evaluate backup freshness and completeness.  
**Acceptance:** Failed, incomplete, stale, healthy, and unknown backup states are distinguishable.

## Phase D — Customer-facing value

### PR 28 — Current assurance API

**Objective:** Expose current results through one stable, authenticated endpoint.  
**Acceptance:** Results can be filtered by action-required status and target.

### PR 29 — Minimal status page

**Objective:** Show current assurance results in one server-rendered page.  
**Acceptance:** Operator sees target, check, status, message, last attempt, and last success.

### PR 30 — Assurance detail page

**Objective:** Show safe current evidence for one target/check.  
**Acceptance:** Non-healthy results are explainable without exposing secrets.

### PR 31 — Safe manual recheck

**Objective:** Allow an admin to trigger one allowlisted check.  
**Acceptance:** Recheck respects lock, authorization, timeout, and concurrency limits.

### PR 32 — Daily report model

**Objective:** Generate a deterministic report payload from current state.  
**Acceptance:** Report distinguishes critical, warning, unknown, stale, disabled, and healthy coverage.

### PR 33 — HTML email report

**Objective:** Render and deliver the daily assurance report by email.  
**Acceptance:** Test recipient receives an actionable report with coverage and timestamps.

### PR 34 — Report scheduling and failure alert

**Objective:** Schedule one daily report and expose delivery failure.  
**Acceptance:** Report runs once at configured local time and failures alert Leolan support.

### PR 35 — Platform health endpoint

**Objective:** Expose readiness, scheduler heartbeat, last completed execution, and storage health.  
**Acceptance:** Monitoring outage becomes visible within the agreed stale window.

## Phase E — Deployment and acceptance

### PR 36 — Production deployment package

**Objective:** Provide one supported customer-hosted deployment configuration.  
**Acceptance:** Clean VM installation succeeds from documented steps.

### PR 37 — Backup and restore runbook

**Objective:** Document and verify PostgreSQL/configuration recovery.  
**Acceptance:** Restore rehearsal succeeds in a nonproduction environment.

### PR 38 — Operational logging context

**Objective:** Make every execution traceable by deployment, target, and check.  
**Acceptance:** A support engineer can diagnose representative failures without sensitive log content.

### PR 39 — Customer acceptance fixtures

**Objective:** Add sanitized fixtures from every supported Customer #1 CUCM version.  
**Acceptance:** All V1 parsers pass fixtures captured during onboarding.

### PR 40 — Release-candidate hardening

**Objective:** Fix only defects discovered during the 72-hour soak and customer validation.  
**Acceptance:** No open production blocker; acceptance checklist passes.

PR numbers express delivery order, but independent check work may proceed in parallel after the baseline is stable. No PR may add an excluded V1 feature.

---

# 11. Production Readiness Checklist

## Commercial and scope

- [ ] Signed paid pilot/onboarding agreement.
- [ ] Recurring subscription price and conversion terms documented.
- [ ] Named economic buyer, technical owner, and security contact.
- [ ] Agreed Customer #1 node/cluster count.
- [ ] Agreed supported CUCM versions.
- [ ] Written V1 inclusions and exclusions accepted.
- [ ] Pilot success criteria accepted.
- [ ] Support hours and escalation path accepted.
- [ ] Customer understands that Leolan is read-only and does not remediate.

## Security

- [ ] All previously exposed credentials rotated.
- [ ] No hardcoded credentials.
- [ ] No real `.env`, debug log, local venv, or secrets in release artifact.
- [ ] Secret storage approved.
- [ ] Least-privilege CUCM account approved and tested.
- [ ] SSH host keys enrolled and pinned.
- [ ] TLS enabled.
- [ ] Network paths and firewall rules approved.
- [ ] Authentication/access boundary tested.
- [ ] Mutation authorization tested.
- [ ] Logs and reports reviewed for sensitive data.
- [ ] Secret-rotation procedure documented.

## Installation and database

- [ ] Pinned release installs on a clean supported host.
- [ ] Fresh database migration succeeds.
- [ ] Upgrade from the previous pilot build succeeds.
- [ ] PostgreSQL types and constraints validated.
- [ ] InfluxDB bucket and retention configured.
- [ ] Startup configuration validation passes.
- [ ] Readiness endpoint passes.
- [ ] Exactly one scheduler is active.
- [ ] Rollback procedure rehearsed.

## Monitoring correctness

- [ ] NTP validated against customer output.
- [ ] Disk/log partitions validated against customer output.
- [ ] Critical services and expected-service baseline approved.
- [ ] Database replication validated against customer output.
- [ ] Certificates validated against customer inventory.
- [ ] DRS evidence source and interpretation approved.
- [ ] Healthy, warning, critical, unknown, stale, and disabled examples tested.
- [ ] Missing or malformed evidence never becomes healthy.
- [ ] Every execution finalizes once.
- [ ] No same-target/check overlap.
- [ ] Connection and command deadlines verified.
- [ ] Connections close after timeout and parser failure.
- [ ] Conservative concurrency validated with customer.
- [ ] No mutating Cisco command exists in the V1 allowlist.

## Customer experience

- [ ] Current-status page shows all contracted targets.
- [ ] Action-required filter works.
- [ ] Evidence explains every seeded failure scenario.
- [ ] Manual recheck respects access and locks.
- [ ] Daily report arrives at the agreed time.
- [ ] Daily report shows expected versus completed coverage.
- [ ] Report recipients approved.
- [ ] Stale monitoring is obvious.
- [ ] Customer validates representative results directly in Cisco tools.
- [ ] All broken or excluded navigation is removed or hidden.

## Reliability and support

- [ ] 72-hour soak completed at expected pilot scale.
- [ ] Application restart tested.
- [ ] Graceful shutdown tested.
- [ ] PostgreSQL outage behavior tested.
- [ ] InfluxDB outage behavior tested.
- [ ] Email delivery failure behavior tested.
- [ ] Scheduler failure/stale behavior tested.
- [ ] PostgreSQL/configuration backup completed.
- [ ] Restore rehearsal completed.
- [ ] Support logs include required correlation context.
- [ ] Leolan support receives platform failure notification.
- [ ] Known limitations documented.
- [ ] Installation, restart, recovery, and troubleshooting runbooks delivered.

## Release gate

Customer #1 may enter production only when:

- All security checklist items pass.
- All monitoring-correctness checklist items pass.
- The daily report and stale-state behavior pass.
- No open defect can expose secrets, harm CUCM, report false health, lose current state, or silently stop monitoring.

Cosmetic defects, unused internal modules, broad refactoring, and future-feature gaps do not block release.

---

# 12. Future Vision

## 12.1 Product direction

Leolan grows from daily CUCM assurance into a broader **UC Operational Assurance platform**.

Growth must follow paid customer evidence, not architectural ambition.

## 12.2 Expansion order

### V1.1 — Notification and workflow

- Teams integration.
- Finding acknowledgement and temporary suppression.
- Ticketing/webhook integrations.
- Weekly management report.
- Better historical evidence.

### V1.2 — Broader Cisco UC product coverage

- Unity Connection.
- IM and Presence.
- UCCX.
- Expressway.
- Product-specific backup, certificate, service, and replication checks.

### V1.3 — Real-time service assurance

- Phone registration anomalies.
- SIP trunk and gateway status.
- Media resource exhaustion.
- Route and location capacity.
- Customer-specific baselines and maintenance windows.

### V2 — Incident assurance

- One-click incident evidence capture.
- Alarm and execution timeline.
- TAC-ready evidence bundle.
- Cross-check correlation.
- Suggested diagnostic runbooks, clearly separated from confirmed facts.

### V2.5 — Upgrade assurance

- Repeatable pre-upgrade assessment.
- Version and compatibility inventory.
- Pre/post-upgrade evidence comparison.
- Upgrade blocker tracking.
- Partner/MSP assessment workflow.

### V3 — MSP platform

- Multi-customer tenancy.
- Role-based access.
- Customer-specific branding and reporting.
- Fleet-level status.
- Delegated administration.
- Commercial SLA and service-review reporting.

### V4 — Advanced operations

- Configuration change intelligence.
- Topology and dependency modeling.
- Voice-quality and CDR/CMR analytics.
- Capacity forecasting.
- Safe, approval-based remediation.
- Knowledge-assisted diagnosis.

## 12.3 Long-term architectural principles

- Preserve the collector/parser/evaluator/persistence separation.
- Add a check only when it has a buyer and a clear operational response.
- Keep current state separate from high-volume history.
- Prefer explicit, static supported integrations over premature plugin systems.
- Do not introduce distributed infrastructure before measured customer scale requires it.
- Never allow a collection error to appear as healthy.
- Default to read-only operation.
- Treat customer trust and evidence quality as product features.

## 12.4 Success metric

The primary V1 metric is not number of collectors, API endpoints, or dashboard pages.

It is:

> **One customer pays Leolan recurring revenue because the daily assurance report identifies actionable Cisco UC risk and replaces a manual or unreliable operational process.**

Secondary evidence:

- At least 95% of scheduled checks complete during the accepted pilot, excluding customer-controlled outages.
- Every missed check becomes visibly stale.
- Customer reviews the report at least weekly.
- At least one actionable condition is identified or one recurring manual workflow is eliminated.
- Customer agrees to continue, expand, or provide a commercial reference.

---

# Final Product Decision

Leolan V1 will ship only the smallest trustworthy path from CUCM evidence to a daily actionable report.

The team must reject work that primarily improves architectural elegance, generic platform capability, UI polish, or hypothetical scale. Work is accepted into V1 only when it is required to:

1. Close and onboard Customer #1.
2. Collect the six contracted assurance domains safely.
3. Prevent false health or silent monitoring failure.
4. Deliver one useful daily report and current-status view.
5. Operate the paid deployment securely and recoverably.

Everything else belongs after revenue.
