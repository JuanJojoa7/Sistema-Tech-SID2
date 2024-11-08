const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ContractSchema = new Schema({
  contract_id: { type: Schema.Types.ObjectId, required: true },
  seller_id: { type: Schema.Types.ObjectId, ref: 'Contact', required: true },
  buyer_id: { type: Schema.Types.ObjectId, ref: 'Contact', required: true },
  currency_id: { type: Schema.Types.ObjectId, ref: 'Currency', required: true },
  total_amount: { type: Number, required: true },
  created_at: { type: Date, default: Date.now },
  updated_at: { type: Date, default: Date.now }
});

module.exports = {
    Contract: mongoose.model('Contract', ContractSchema)
};