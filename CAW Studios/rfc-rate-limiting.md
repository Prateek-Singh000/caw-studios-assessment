# RFC: Implementing API Rate Limiting

## 1. Problem Statement
Our public API currently lacks automated traffic control. Last month, a single customer accidentally sent 50,000 requests per minute, which degraded service response times for all other customers. Because we have no throttling mechanism, the on-call engineer had to manually block the customer's API key via a configuration redeploy at 2 AM. 

Beyond operational pain, this limitation blocks business growth. The product team plans to launch a paid tier with guaranteed capacity, but we cannot enforce tiered limits without underlying rate-limiting infrastructure.

## 2. Proposed Approach
We propose implementing a centralized **Token Bucket** rate limiter at the **API Gateway** layer, backed by **Redis**.

*   **Placement (API Gateway):** Throttling will happen at the front door. This protects our backend application servers from wasting compute resources on requests that will ultimately be rejected.
*   **Algorithm (Token Bucket):** Each client gets a "bucket" of tokens that refills at a steady rate. This algorithm handles sudden bursts of legitimate traffic smoothly, unlike fixed-window counters that abruptly cut off users.
*   **Storage (Redis):** Because we run multiple API gateway instances behind a load balancer, the rate limiter needs a shared, low-latency state. Redis provides extremely fast in-memory reads and writes across all instances.

## 3. Alternatives Considered
*   **Alternative A: In-memory limiting on application servers.** 
    *   *Pros:* Zero new infrastructure. Lowest possible latency since no external network call is made.
    *   *Cons:* Because traffic is load-balanced across multiple servers, a user's actual limit would multiply by the number of active servers. It is inaccurate and fails to enforce global limits.
*   **Alternative B: Fixed-window algorithm backed by PostgreSQL.**
    *   *Pros:* We already use PostgreSQL, avoiding the need to provision and monitor a new Redis cluster.
    *   *Cons:* The fixed-window algorithm allows 2x traffic bursts at the boundary of a minute. Furthermore, PostgreSQL is not optimized for thousands of rapid increment operations per second and could become a bottleneck.

## 4. Risks and Mitigations
*   **Risk:** Redis becomes a single point of failure (SPOF).
    *   *Mitigation:* The rate limiter will be configured to "fail open." If the gateway cannot reach Redis within a 5ms timeout, it will allow the request through. It is better to risk temporary overload than to cause a total API outage.
*   **Risk:** Added latency to every API call.
    *   *Mitigation:* Redis reads/writes typically complete in under 2ms. By keeping Redis in the same VPC as the gateway, network overhead is minimized.
*   **The Risk of Doing Nothing:** We remain vulnerable to cascading failures from noisy neighbors, and the product team cannot launch the new revenue-generating paid tier.

## 5. Open Questions
*   **Product:** What should the default request limit be for free/unauthenticated users versus paid users?
*   **Frontend/SDK:** When we return a `429 Too Many Requests` status, should we include a `Retry-After` header? Can our existing client SDKs handle 429s gracefully without infinite retry loops?
