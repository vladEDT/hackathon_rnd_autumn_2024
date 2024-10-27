const express = require('express')
const bodyParser = require('body-parser')
const cors = require('cors')
const connectDB = require('./config/db') // Импорт подключения к MongoDB
const Product = require('./models/Product') // Модель продукта

const app = express()
const PORT = 4000

app.use(
  cors({
    origin: 'http://localhost:5173',
    methods: ['GET', 'POST'],
    credentials: true
  })
)

app.use(bodyParser.json())

connectDB()

app.post('/search', async (req, res) => {
  const {product_title, product_type} = req.body
  if (!product_title) {
    return res.status(400).json({error: 'Title is required'})
  }

  const query = {}

  if (product_title) {
    query.product_title = {$regex: product_title, $options: 'i'}
  }

  if (product_type) {
    query.product_type = product_type
  }

  try {
    const products = await Product.find(query)
    res.json(products)
  } catch (error) {
    console.error(error)
    res.status(500).json({error: 'Something went wrong'})
  }
})

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`)
})
