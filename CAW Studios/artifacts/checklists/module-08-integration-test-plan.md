# Module 08: Cross-Component Integration Test Plan

## Test 1: Full Booking Propagation (Happy Path)
* **Components:** Providers API, Bookings API, Database.
* **Setup:** Seed 1 Provider with 1 'available' slot. Generate User JWT.
* **Steps:** 
  1. Call `GET /providers/1/slots` -> Extract `time_slot_id`.
  2. Call `POST /bookings` using the extracted ID.
  3. Call `GET /providers/1/slots` again.
* **Expected Result:** Step 2 returns 201. Step 3 confirms the slot is missing or marked 'booked'. (Validates API-01 <-> API-02 contract).

## Test 2: RBAC Delegation Rejection (Security Boundary)
* **Components:** Auth System, Bookings API.
* **Setup:** Generate 'employee' role JWT.
* **Steps:** 
  1. Call `POST /bookings` with `booked_for_email="boss@company.com"`.
* **Expected Result:** Returns `403 Forbidden`. The booking is NOT created. (Validates Auth <-> Bookings contract).

## Test 3: Concurrent Booking Race Condition (Edge Case)
* **Components:** Bookings API, Database Transactions.
* **Setup:** Identify 1 'available' slot.
* **Steps:** 
  1. Fire two `POST /bookings` requests simultaneously for the exact same `time_slot_id`.
* **Expected Result:** One request returns 201. The other returns 400 or 409 (Conflict). DB shows exactly 1 booking.
