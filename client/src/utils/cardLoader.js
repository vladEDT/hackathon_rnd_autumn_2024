export const cardLoader = () => {
  const form = document.querySelector('.form')
  const blocks = document.querySelector('.blocks')
  const bl_children = blocks.children
  if (form) {
    form.classList.add('maxheight')
  }

  setTimeout(() => {
    blocks.classList.add('displaygr')
    for (let i = 0; i < bl_children.length; i++) {
      bl_children[i].classList.add('displayb')
    }

    for (let i = 0; i < bl_children.length; i++) {
      setTimeout(() => {
        bl_children[i].classList.add('opacity')
      }, 100 * i)
    }
  }, 1000)
}
