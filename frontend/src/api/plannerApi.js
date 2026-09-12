import client from './client'

export const generateTrip = (payload) => client.post('/planner/generate', payload).then((response) => response.data)
export const modifyTrip = (id, instructions) => client.post(`/planner/${id}/modify`, { instructions }).then((response) => response.data)
export const regenerateTrip = (id) => client.post(`/planner/${id}/regenerate`).then((response) => response.data)
export const approveTrip = (id) => client.post(`/planner/${id}/approve`).then((response) => response.data)
