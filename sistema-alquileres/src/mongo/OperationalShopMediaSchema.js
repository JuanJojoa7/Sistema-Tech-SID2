const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const OperationalShopMediaSchema = new Schema({
  operational_shop_media_id: { type: Schema.Types.ObjectId, required: true },
  operational_shop_id: { type: Schema.Types.ObjectId, ref: 'OperationalShop', required: true },
  media_url: { type: String, required: true }
});

module.exports = {
    OperationalShopMedia: mongoose.model('OperationalShopMedia', OperationalShopMediaSchema)
};