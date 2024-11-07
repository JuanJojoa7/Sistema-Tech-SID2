const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ContactSchema = new Schema({
  contact_id: { type: Schema.Types.ObjectId, required: true },
  name: { type: String, required: true },
  phone: { type: String, required: true },
  email: { type: String, required: true },
  address: { type: String, required: true },
  city_id: { type: Schema.Types.ObjectId, ref: 'City', required: true },
  created_at: { type: Date, default: Date.now },
  updated_at: { type: Date, default: Date.now }
});

module.exports = {
    Contact: mongoose.model('Contact', ContactSchema)
};