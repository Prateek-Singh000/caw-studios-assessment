module.exports = (role) => async (req, res, next) => {
  try {
    const member = await TeamMember.findOne({ where: { userId: req.user.id, teamId: req.params.teamId }});
    
    if (!member || member.role !== role) {
      return res.status(403).json({ 
        error: { 
          code: 'FORBIDDEN', 
          message: 'Insufficient permissions' 
        } 
      });
    }
    next();
  } catch (err) {
    return res.status(500).json({ 
      error: { 
        code: 'INTERNAL_ERROR', 
        message: 'An unexpected error occurred' 
      } 
    });
  }
};
