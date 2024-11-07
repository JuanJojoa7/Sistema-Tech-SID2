// models/Contact.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const City = require('./City');

const Contact = sequelize.define('Contact', {
  contact_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  name: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  phone: {
    type: DataTypes.STRING,
  },
  email: {
    type: DataTypes.STRING,
  },
  address: {
    type: DataTypes.TEXT,
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

Contact.belongsTo(City, { foreignKey: 'city_id' });
City.hasMany(Contact, { foreignKey: 'city_id' });

module.exports = Contact;
