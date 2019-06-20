import axios from 'axios'

export const HTTP = axios.create({
  baseURL: `http://client.ingate.ru/Offers/FilterRivals/api/`,
  auth: {
    username: 'offeruser',
    password: 'D_f$7u-SVX9v"h;j'
  }
})
