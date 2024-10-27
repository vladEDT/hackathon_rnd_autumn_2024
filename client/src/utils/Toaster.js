import {toast} from 'react-toastify'

export const toaster = message => {
  return toast.error(
    message,
    {
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: 'dark'
    }
  )
}
