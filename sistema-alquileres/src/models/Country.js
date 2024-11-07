// models/Country.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');

const Country = sequelize.define('Country', {
  country_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  code: {
    type: DataTypes.STRING,
    allowNull: false,
  },
}, {
  timestamps: false,
});

module.exports = Country;
