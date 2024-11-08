const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ShopSchema = new Schema({
  shop_id: { type: Schema.Types.ObjectId, required: true },
  company_id: { type: Schema.Types.ObjectId, ref: 'Company', required: true },
  name: { type: String, required: true },
  address: { type: String, required: true },
  created_at: { type: Date, default: Date.now },
  updated_at: { type: Date, default: Date.now }
});

module.exports = {
    Shop: mongoose.model('Shop', ShopSchema)
};