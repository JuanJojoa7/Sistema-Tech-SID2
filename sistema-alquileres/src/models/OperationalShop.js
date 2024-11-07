// models/OperationalShop.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const Shop = require('./Shop');
const City = require('./City');

const OperationalShop = sequelize.define('OperationalShop', {
  operational_shop_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  address: {
    type: DataTypes.TEXT,
  },
  shop_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Shop,
      key: 'shop_id',
    },
  },
  city_id: {
    type: DataTypes.INTEGER,
    references: {
      model: City,
      key: 'city_id',
    },
  },
}, {
  timestamps: true,
  createdAt: 'created_at',
  updatedAt: 'updated_at',
});

OperationalShop.belongsTo(Shop, { foreignKey: 'shop_id' });
Shop.hasMany(OperationalShop, { foreignKey: 'shop_id' });

OperationalShop.belongsTo(City, { foreignKey: 'city_id' });
City.hasMany(OperationalShop, { foreignKey: 'city_id' });

module.exports = OperationalShop;
