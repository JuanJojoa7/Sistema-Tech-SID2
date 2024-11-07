// /models/Operational_Shop_Hours.js
module.exports = (sequelize, DataTypes) => {
  const Operational_Shop_Hours = sequelize.define('Operational_Shop_Hours', {
    operational_shop_hours_id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true,
    },
    operational_shop_id: DataTypes.INTEGER,
    day_of_week: DataTypes.STRING,
    open_time: DataTypes.TIME,
    close_time: DataTypes.TIME,
  });

  Operational_Shop_Hours.associate = (models) => {
    Operational_Shop_Hours.belongsTo(models.Operational_Shop, { foreignKey: 'operational_shop_id' });
  };

  return Operational_Shop_Hours;
};
