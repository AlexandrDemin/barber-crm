import axios from 'axios'

export const HTTP = axios.create({
  baseURL: `http://localhost:5000/api/`
})
HTTP.interceptors.response.use(response => {
  if (typeof response.data === 'string') {
    response.data = JSON.parse(response.data)
  }
  return response
})
