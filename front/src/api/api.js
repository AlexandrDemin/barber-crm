import axios from 'axios'

export const HTTP = axios.create({
  baseURL: `api/`,
  auth: {
    username: 'demo.user',
    password: 'demo'
  }
})
