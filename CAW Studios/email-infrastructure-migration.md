**Subject:** Q3 Infrastructure Migration: Securing Our Checkout Reliability for Holiday Peak

Hi Sarah and David,

We are planning an 8-week infrastructure migration in Q3 to replace our aging API traffic gateway with a modern, higher-capacity system. This upgrade is critical to ensuring our checkout system remains stable and does not repeat the traffic bottlenecks we experienced during last year's Black Friday event.

### Why Now?
During peak traffic last November, our current gateway reached its limits, causing latency to spike and leaving checkout degraded for 47 minutes. Our current software version is outdated and lacks the modern reliability features needed to handle our projected growth. Furthermore, it prevents us from enforcing modern zero-trust security policies across our internal services.

### Proposed Changes & Timeline
*   **What we are doing:** Replacing our traffic routing and gateway layer with a modern, unified system (Envoy-based ingress) and modernizing our internal monitoring and security tooling. 
*   **Effort:** 2 engineers for 8 weeks during Q3.
*   **Customer Impact:** Zero. We will run both systems in parallel (blue-green deployment) to ensure no customer-facing downtime.

### Risks & Mitigations
*   **Performance Risk:** The new system relies on internal filters (WASM) that must match our previous throughput. *Mitigation:* We will run rigorous load tests in our staging environment at 2x peak traffic before cutting over. If it fails to meet benchmarks, we will fall back to the existing setup.
*   **Server Capacity Risk (Hidden Risk):** The new system requires additional server memory per server pod (roughly 42.5 GB total across the cluster). If we do not provision this headroom before launch, a sudden traffic spike could exhaust cluster memory and trigger unexpected outages. *Mitigation:* We are auditing our node pool capacity and will validate headroom requirements before production cutover.

### Decisions / Asks
1. **Resource Approval:** Approval to allocate 2 platform engineers for 8 weeks in Q3.
2. **Roadmap Alignment:** Confirmation that shifting these 2 engineers away from feature work for 8 weeks does not conflict with critical product commitments.
3. **Capacity Sign-off:** Infrastructure approval to provision additional node headroom to support the increased memory overhead of the new security sidecars.

Thanks,  
Marcus
