// models/City.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const Country = require('./Country');

const City = sequelize.define('City', {
  city_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  country_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Country,
      key: 'country_id',
    },
  },
}, {
  timestamps: false,
});

City.belongsTo(Country, { foreignKey: 'country_id' });
Country.hasMany(City, { foreignKey: 'country_id' });

module.exports = City;
