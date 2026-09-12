import client from './client'

export const register = (payload) => client.post('/auth/register', payload).then((response) => response.data)
export const login = (payload) => client.post('/auth/login', payload).then((response) => response.data)
export const getCurrentUser = () => client.get('/users/me').then((response) => response.data)
export const updateCurrentUser = (payload) => client.patch('/users/me', payload).then((response) => response.data)
