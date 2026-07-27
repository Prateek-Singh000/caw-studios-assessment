# Technical Explanation: REST-to-GraphQL Migration

## Decision Summary
The backend team is migrating our public-facing API from REST to GraphQL over the next 8 weeks to eliminate redundant endpoints and significantly speed up frontend development. By allowing client applications to request exactly the data they need, this architectural shift will reduce frontend API calls by 40% and reclaim the 30% of sprint capacity we currently waste building custom data aggregation logic.

## Why We Chose This
Our current API uses REST (a traditional architecture where the server decides exactly what data to return—like a restaurant with a fixed menu). We currently maintain 47 REST endpoints (specific URLs where the API is accessed). Fifteen of these exist solely because our mobile app and web app require different data shapes for the exact same UI screen. 

To solve this, frontend developers spend 30% of their time building single-purpose "aggregation endpoints" to stitch data together. 

We chose GraphQL (a query language that lets the client ask for exactly the data it needs—like a buffet where you pick only what you want) because it completely eliminates this bottleneck. A single GraphQL endpoint can serve both the web and mobile apps perfectly.

We also evaluated and rejected two alternatives:
*   **Backend-for-Frontend (BFF):** A dedicated translation service between the API and each frontend. We rejected this because deploying and monitoring another service adds too much operational complexity.
*   **Standardized REST Schemas:** We rejected this because standardizing the data shape does not solve the fundamental problem of different clients requiring different data points.

## Risks and Mitigations
*   **Learning Curve:** GraphQL has a steeper learning curve than REST. Because two of the three engineers dedicated to this migration are new to GraphQL, we are factoring dedicated learning time into the sprint capacity.
*   **Query Performance:** GraphQL allows clients to request deeply nested, resource-heavy data. The backend team will mitigate this by implementing query depth limits to protect the database from overloads.
*   **Caching Complexity:** REST is easy to cache because it uses fixed URLs. GraphQL uses dynamic POST request bodies, which bypass traditional HTTP caching. We will mitigate this by shifting our caching strategy to the application and database layers.

## What This Means for Priya
You are joining just as this 8-week migration kicks off. During the migration window, the backend team will run both the legacy REST endpoints and the new GraphQL endpoint simultaneously to ensure zero downtime. 

Because you are new to the team, you will not be expected to write GraphQL mutations on day one. You will spend your first two weeks pairing with the migration team to learn our GraphQL schema and how we handle data fetching.

## Next Steps
*   Set up your local GraphQL playground by following the environment setup guide in `api/README.md`.
*   Review the "GraphQL Basics" internal wiki page by the end of the day on Wednesday.
*   Attend the API architecture sync at 10:00 AM on Thursday to meet the three engineers leading the migration.
