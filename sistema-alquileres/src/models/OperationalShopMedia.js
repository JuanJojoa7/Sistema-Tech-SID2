// /models/Operational_Shop_Media.js
module.exports = (sequelize, DataTypes) => {
    const Operational_Shop_Media = sequelize.define('Operational_Shop_Media', {
      operational_shop_media_id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      operational_shop_id: DataTypes.INTEGER,
      media_url: DataTypes.STRING,
    });
  
    Operational_Shop_Media.associate = (models) => {
      Operational_Shop_Media.belongsTo(models.Operational_Shop, { foreignKey: 'operational_shop_id' });
    };
  
    return Operational_Shop_Media;
  };
  