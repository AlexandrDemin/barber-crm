import axios from 'axios'

export const HTTP = axios.create({
  baseURL: `http://146.185.179.193/:5000/api/`
})
