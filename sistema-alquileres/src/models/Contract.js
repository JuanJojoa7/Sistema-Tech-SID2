// models/Contract.js
const { DataTypes } = require('sequelize');
const sequelize = require('../config/db');
const Contact = require('./Contact');
const Currency = require('./Currency');

const Contract = sequelize.define('Contract', {
  contract_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  total_amount: {
    type: DataTypes.DECIMAL,
    allowNull: false,
  },
  seller_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Contact,
      key: 'contact_id',
    },
  },
  buyer_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Contact,
      key: 'contact_id',
    },
  },
  currency_id: {
    type: DataTypes.INTEGER,
    references: {
      model: Currency,
      key: 'currency_id',
    },
  },
}, {
  timestamps: true,
  createdAt: 'created_at',
  updatedAt: 'updated_at',
});

Contract.belongsTo(Contact, { as: 'Seller', foreignKey: 'seller_id' });
Contract.belongsTo(Contact, { as: 'Buyer', foreignKey: 'buyer_id' });
Contract.belongsTo(Currency, { foreignKey: 'currency_id' });

Contact.hasMany(Contract, { foreignKey: 'seller_id', as: 'SoldContracts' });
Contact.hasMany(Contract, { foreignKey: 'buyer_id', as: 'BoughtContracts' });
Currency.hasMany(Contract, { foreignKey: 'currency_id' });

module.exports = Contract;
