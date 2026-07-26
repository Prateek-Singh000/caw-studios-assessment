const { Team, TeamMember } = require('../models');
exports.createTeam = async (req, res) => {
  try {
    const team = await Team.create({ ...req.body, ownerId: req.user.id });
    await TeamMember.create({ teamId: team.id, userId: req.user.id, role: 'admin' });
    res.status(201).json(team);
  } catch (err) {
    res.status(400).json({ error: { code: 'VALIDATION_ERROR', message: err.message }});
  }
};
