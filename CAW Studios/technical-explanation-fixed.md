# Decision: Migrating from REST to GraphQL

The backend team is migrating our public-facing API from REST to GraphQL to eliminate redundant endpoints and reduce frontend API calls by 40%. 

## The Problem
Our current REST API has 47 endpoints. The frontend (FE) and mobile teams spend significant sprint capacity creating and maintaining "aggregation endpoints" solely because mobile and web clients require different data shapes for the same screens. 

The Site Reliability Engineering (SRE) team also noted that the mobile app makes multiple sequential REST calls when one query should suffice. The SDK (Software Development Kit) team has struggled to maintain backward compatibility across this growing number of endpoints.

We considered building a Backend-for-Frontend (BFF)—a dedicated service to translate the API for specific clients—but rejected it due to the unacceptable deployment and monitoring overhead.

## The Solution
We are migrating to GraphQL, a query language that lets clients request exactly the data they need in a single call. This will eliminate 15 unnecessary aggregation endpoints.

Three backend engineers will work on this migration over the next 8 weeks. To ensure zero downtime, the team will run the REST and GraphQL endpoints simultaneously during the transition.

## Risks & Mitigations
*   **Learning Curve:** Two of the three engineers are new to GraphQL. The team will mitigate this through pair programming and dedicated learning time during the first two weeks.
*   **Performance & Caching:** Query unpredictability and caching complexity are known risks. The backend team will monitor query performance daily and address bottlenecks as they arise.
