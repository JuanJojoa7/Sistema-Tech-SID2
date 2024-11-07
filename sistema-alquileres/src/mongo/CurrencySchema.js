const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const CurrencySchema = new Schema({
  currency_id: { type: Schema.Types.ObjectId, required: true },
  name: { type: String, required: true },
  code: { type: String, required: true },
  symbol: { type: String, required: true }
});

module.exports = {
    Company: mongoose.model('Company', CompanySchema)
};