const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ContractStatusSchema = new Schema({
  contract_status_id: { type: Schema.Types.ObjectId, required: true },
  contract_id: { type: Schema.Types.ObjectId, ref: 'Contract', required: true },
  status: { type: String, required: true },
  updated_at: { type: Date, default: Date.now }
});

module.exports = {
    ContractStatus: mongoose.model('ContractStatus', ContractStatusSchema)
};