// --- Capstone: The Crash Loop ---
const uploadQueue = [
    { userId: 101, file: { name: "report.pdf", size: 2000 } },
    { userId: 102, file: null }, // Network dropped, file is null
    { userId: 103, file: { name: "data.csv", size: 3000 } }
];

function handleUpload(req) {
    console.log(`[INFO] Starting upload for User ${req.userId}`);
    
    // THE FIX: Guard clause. Fail fast, return early.
    if (!req.file) {
        console.error(`[ERROR] User ${req.userId} upload failed: file is missing.`);
        return; 
    }

    // It is now guaranteed safe to read .size
    const isOversized = req.file.size > 5000;
    
    if (isOversized) {
        console.error(`[WARN] User ${req.userId} file too large.`);
        return;
    }
    
    console.log(`[INFO] User ${req.userId} upload complete.`);
}

console.log("--- STARTING UPLOAD QUEUE ---");
for (const req of uploadQueue) {
    handleUpload(req);
}
console.log("--- QUEUE FINISHED ---");
