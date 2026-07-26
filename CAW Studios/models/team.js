const { Model, DataTypes } = require('sequelize');
module.exports = (sequelize) => {
  class Team extends Model {}
  Team.init({ 
    id: { type: DataTypes.UUID, defaultValue: DataTypes.UUIDV4, primaryKey: true },
    name: { type: DataTypes.STRING, allowNull: false },
    description: { type: DataTypes.STRING, allowNull: true },
    ownerId: { type: DataTypes.INTEGER, allowNull: false }
  }, { sequelize, modelName: 'Team' });
  Team.associate = (models) => {
    Team.belongsTo(models.User, { foreignKey: 'ownerId', as: 'owner' });
    Team.hasMany(models.TeamMember, { foreignKey: 'teamId' });
  };
  return Team;
};
