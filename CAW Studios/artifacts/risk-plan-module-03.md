# SkillSwap Risk-First Build Plan (Revised for Business Blocker)

## BLOCKED ITEMS & PM ESCALATION
**BLOCKED:** Production Payment Integration (Stripe) & Real Refunds.
**PM Escalation Message:** *"Payment processing is blocked — the client has no Stripe account or merchant entity set up. We are stubbing the payment interface so development on Bookings continues, but real payment testing is blocked until the client resolves this. Can you get us a timeline?"*

---

## Ordered Build Plan (Pivoted)

**1. Listings Data Model (Risk: 3, Dependency, Scale)**
*Justification:* Foundational. Handle 5-city expansion schema early.

**2. User Authentication (Risk: 2, Dependency)**
*Justification:* Low technical risk, high dependency. Unblocks user workflows.

**3. SPIKE: Availability Concurrency (Risk: 4, Novelty)**
*Justification:* PIVOTED UP. With payments blocked, we tackle the next highest technical risk immediately (testing database locks for double-bookings).

**4. Payment Interface Contract & Stub (Risk: 1, Mitigation)**
*Justification:* We define `processPayment(...)` that always returns `{status: success}`. We build a fake endpoint so the rest of the system has something to talk to.

**5. Booking Flow (Risk: 3, Novelty)**
*Justification:* Built safely against the Payment Stub. Development continues seamlessly.

**6. Cancellation Flow (Risk: 4, Integration, Novelty)**
*Justification:* Built safely against the Payment Stub (using fake refund responses).

**7. Admin Review Tool (Minimal) (Risk: 1, None)**
*Justification:* Low risk, unblocks Provider Onboarding.

**8. Provider Onboarding (Risk: 3, Novelty)**
*Justification:* State machine for vetting.

**9. Search & Browse (Risk: 3, Scale)**
*Justification:* Built on top of the Listings model.

**10. Notification System (Risk: 2, Integration)**
*Justification:* Soft dependency. Can be added late.

**11. Review System & Admin Dashboard (Full)**
*Justification:* Standard CRUD. Zero risk, end of the pipeline.

**[ON HOLD] Payment Processing [Production] (Risk: 5, Integration)**
*Justification:* Will be swapped in to replace the Stub at Step 4 the moment the client provides a valid Stripe account.
