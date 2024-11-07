// models/Shop.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const Company = require('./Company');

const Shop = sequelize.define('Shop', {
  shop_id: {
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
  company_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Company,
      key: 'company_id',
    },
  },
}, {
  timestamps: true,
  createdAt: 'created_at',
  updatedAt: 'updated_at',
});

Shop.belongsTo(Company, { foreignKey: 'company_id' });
Company.hasMany(Shop, { foreignKey: 'company_id' });

module.exports = Shop;
