import search from './assets/search.svg'
import './App.scss'
import axios from 'axios'
import Product from './components/Product'
import {cardLoader} from './utils/cardLoader'
import {useState} from 'react'
import {ToastContainer} from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import {toaster} from './utils/Toaster'

const App = () => {
  const [cards, setCards] = useState([])
  const [input, setInput] = useState('')

  const handleSubmit = async e => {
    if (!input) {
      e.preventDefault()
      toaster('Введите поисковый запрос')
    } else {
      e.preventDefault()
      try {
        const response = await axios.post('http://localhost:4000/search', {
          product_title: input
        })

        if (response.data.length === 0) {
          toaster('Ничего не нашлось')
        } else {
          cardLoader(e)
        }

        setCards(response.data)
      } catch {
        toaster('Произошла ошибка')
      }
    }
  }

  return (
    <>
      <form className='form' id='form' onSubmit={e => handleSubmit(e)}>
        <input
          className='search'
          type='text'
          name='search'
          id='search'
          placeholder='Введите поисковый запрос'
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <button className='submit_button' type='submit' value='' id='submit'>
          <img src={search} alt='search' />
        </button>
      </form>
      <div className='container'>
        <div className='blocks'>
          {cards.map(data => (
            <Product
              key={data.id}
              link={data.product_url}
              img={data.images[0]}
              title={data.product_title}
              category={data.product_type}
              price={data.price}
              description={data.product_description}
            />
          ))}
        </div>
        <div className='foot'></div>
        <ToastContainer position='bottom-right' />
      </div>
    </>
  )
}

export default App
