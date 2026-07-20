// --- Layer 3: Database Service ---
const db = {
    1: { name: "Alice", status: "active" },
    2: { name: "Bob" } // Bob is missing a status
};

function getUserStatus(userId) {
    const user = db[userId];
    if (!user) throw new Error("User not found");
    
    // THE FIX: Provide a safe fallback before applying string methods
    return (user.status || "unknown").toUpperCase();
}

// --- Layer 2: Business Logic ---
function processUser(userId) {
    console.log(`[Service] Processing user ${userId}`);
    try {
        const status = getUserStatus(userId);
        return `User is ${status}`;
    } catch (error) {
        console.error(`[Service] Error processing user ${userId}`);
        throw error;
    }
}

// --- Layer 1: API Router ---
function handleRequest(req) {
    console.log(`[Router] GET /api/users/${req.userId}`);
    try {
        const result = processUser(req.userId);
        console.log(`[Router] 200 OK: ${result}`);
    } catch (error) {
        console.error(`[Router] 500 Internal Server Error`);
        console.error(error); 
    }
}

// --- Simulate Traffic ---
console.log("--- Request 1 (Alice) ---");
handleRequest({ userId: 1 });

console.log("\n--- Request 2 (Bob) ---");
handleRequest({ userId: 2 });
