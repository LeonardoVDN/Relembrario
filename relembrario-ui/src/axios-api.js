import axios from 'axios'

const getAPI = axios.create({

    baseURL: 'https://api.example.com',
    timeout: 5000,
})

export { getAPI }

