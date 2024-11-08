const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const OperationalShopSchema = new Schema({
  operational_shop_id: { type: Schema.Types.ObjectId, required: true },
  shop_id: { type: Schema.Types.ObjectId, ref: 'Shop', required: true },
  name: { type: String, required: true },
  address: { type: String, required: true },
  city_id: { type: Schema.Types.ObjectId, ref: 'City', required: true },
  created_at: { type: Date, default: Date.now },
  updated_at: { type: Date, default: Date.now }
});

module.exports = {
    OperationalShop: mongoose.model('OperationalShop', OperationalShopSchema)
};
