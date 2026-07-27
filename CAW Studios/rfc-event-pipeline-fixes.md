### Alternatives Considered

*   **Alternative 1: Managed Queue Service (e.g., AWS SQS)**
    *   *What it is:* A fully managed message queuing service provided by our cloud vendor.
    *   *Pros:* Zero infrastructure to maintain (unlike a 3-broker Kafka cluster), auto-scales out of the box, and includes built-in dead-letter queues.
    *   *Cons:* Lacks Kafka's robust pub/sub fan-out capabilities if we want multiple independent services to read the same event stream later. It also introduces strict vendor lock-in and higher per-message costs at scale.
*   **Alternative 2: In-Process Background Workers (e.g., Redis + Celery)**
    *   *What it is:* Using our existing Redis cache to queue jobs for background worker processes.
    *   *Pros:* No new distributed systems to deploy. The engineering team is already highly familiar with Redis and Celery. 
    *   *Cons:* Limited by RAM. If a worker node crashes mid-process, or if Redis runs out of memory during a massive traffic spike, we permanently lose the event data.

### Open Questions (Validation Required)

*   **Database Write Capacity:** Can the analytics database actually sustain 10,000 writes/second under *production* conditions? 
    *   *Validation Plan:* The current benchmark of 10K was run under unknown conditions. Before Week 3, the database team must run a load test simulating our exact event schema, production indexing patterns, and concurrent read load. If it fails to sustain this, we will need to buffer writes or evaluate a dedicated time-series database.

### Revised Risk Mitigations (Replaces Vague Mitigations)

*   **Risk: Consumer Lag.** If consumers fall behind, event processing will be delayed.
    *   *Concrete Mitigation:* We will set a Datadog alert to trigger if consumer lag exceeds 50,000 messages across any topic for more than 3 minutes. The on-call engineer will be paged to manually scale consumer pods using the `scale-consumers.sh` runbook script. If the lag does not decrease within 15 minutes, the engineer will escalate to the Data Platform lead.
