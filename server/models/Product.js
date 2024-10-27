const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  product_title: {
    type: String,
    required: true,
  },
  product_description: {
    type: String,
  },
  product_type : {
    type: String,
  },
  price: {
    type: Number,
    required: true,
  },
  images: {
    type: Array
  },
  product_url: {
    type: String
  }, 
});

const Product = mongoose.model('Product', ProductSchema);

module.exports = Product;