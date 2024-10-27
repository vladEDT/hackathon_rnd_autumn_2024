const Product = ({key, link, img, title, category, price, description}) => {
  return (
    <div key={key} className='block'>
      <a href={link}></a>
      <div className='block_img'>
        <img src={img} alt='' />
      </div>
      <div className='block_text'>
        <div className='block_title'>{title}</div>
        <div className='block_cat'>{category}</div>
        <div className='block_price'>{price} ₽</div>
        <div className='block_description'>{description}</div>
      </div>
    </div>
  )
}

export default Product
