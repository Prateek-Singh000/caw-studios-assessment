# SkillSwap - Vertical Slices

## Slice 1: Browse and Book (Demand MVP - Hardcoded Supply)
**Scope:** User visits a landing page displaying 3 hardcoded provider cards. User clicks a provider, views a single service, selects a hardcoded time slot, clicks "Book," and sees an on-screen confirmation with a unique booking ID. Booking is persisted to the database.
**Anti-Scope:** No user authentication. No payment processing. No email/SMS confirmations. No search or filtering. No provider dashboard or dynamic registration. No cancellation flow. No reviews. No calendar integrations.
**Dependencies:** None.
**Acceptance Criteria:**
1. Load homepage, verify 3 static provider cards appear.
2. Click provider, verify 1 service and 3 time slots appear.
3. Select slot, click "Book", verify success screen shows Booking ID.
**Estimated Complexity:** S (2-4 hours)

## Slice 2: Provider Onboarding (Supply MVP)
**Scope:** A provider can sign up (basic email/password auth), create a profile, and list one service with static weekly availability (e.g., "Mondays 9-5"). The homepage from Slice 1 now dynamically reads from the database instead of hardcoded seeds.
**Anti-Scope:** No user (demand-side) authentication. No calendar syncing (Google/Outlook). No multiple services per provider. No variable weekly schedules (e.g., specific dates off). No profile picture uploads.
**Dependencies:** Slice 1 (Database schema for bookings/providers must exist).
**Acceptance Criteria:**
1. Provider registers, logs in, and fills out profile/service form.
2. Provider sets "Mondays 9-5" availability and clicks Save.
3. Visitor loads homepage, verifies the newly created provider is now visible.
**Estimated Complexity:** M (1-2 days)

## Slice 3: User Accounts & Booking Management
**Scope:** Users must now authenticate to book. Users get a "My Bookings" dashboard to see upcoming appointments and can click "Cancel" to free up the slot. Providers receive an in-app notification when a booking is created or canceled.
**Anti-Scope:** No payments. No email/push notifications (in-app only). No modifying bookings (must cancel and rebook). No provider ability to cancel user bookings.
**Dependencies:** Slice 1, Slice 2.
**Acceptance Criteria:**
1. User logs in, books a provider, sees it in "My Bookings".
2. User clicks cancel, status changes to "Canceled".
3. Provider logs in, views notifications, sees cancellation alert.
**Estimated Complexity:** M (1-2 days)

## Slice 4: Payments & Reviews
**Scope:** Integrates Stripe Checkout for booking. Users must pay to confirm a slot. After a booking's time elapses, users can leave a 1-5 star review which appears on the provider's profile.
**Anti-Scope:** No payout routing to providers (platform holds funds for now). No review moderation or replies. No partial refunds on cancellation. No subscription plans.
**Dependencies:** Slice 1, Slice 2, Slice 3.
**Acceptance Criteria:**
1. User attempts booking, is redirected to Stripe, completes test payment, returns to success screen.
2. User views past booking, clicks "Leave Review", submits 5 stars.
3. Provider profile displays the new 5-star rating.
**Estimated Complexity:** L (3-4 days)
