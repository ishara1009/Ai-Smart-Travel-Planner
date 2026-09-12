import client from './client'

export const getTrips = (params = {}) => client.get('/trips', { params }).then((response) => response.data)
export const getTrip = (id) => client.get(`/trips/${id}`).then((response) => response.data)
export const deleteTrip = (id) => client.delete(`/trips/${id}`)
export const sendFeedback = (id, payload) => client.post(`/trips/${id}/feedback`, payload).then((response) => response.data)
