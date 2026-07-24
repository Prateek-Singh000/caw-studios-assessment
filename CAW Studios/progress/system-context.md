# System-Level Context Document

## Architecture
- **Framework:** Express.js (Node.js)
- **Database ORM:** Sequelize

## Error Handling Convention (MANDATORY)
ALL error responses MUST follow this exact structure. 
Example:
return res.status(400).json({ 
  error: { 
    code: 'VALIDATION_ERROR', 
    message: 'Team name is required.' 
  } 
});

- Do NOT return plain strings or simplified objects.
- Do NOT omit the 'error' wrapper.
- Do NOT use custom fields like 'status' or 'statusCode' outside the wrapper.
- MUST use the format: { "error": { "code": "...", "message": "..." } }
