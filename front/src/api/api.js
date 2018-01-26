import axios from 'axios'

export const HTTP = axios.create({
  baseURL: `http://192.168.4.158:8899/api/`
})
