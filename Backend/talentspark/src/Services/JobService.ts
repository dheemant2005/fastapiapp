import axios from "axios";
import type {Job} from "../types/job";

const API_BASE_URL = "http://localhost:8000";

function authHeaders() {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getJobs(): Promise<Job[]> {
    const response = await axios.get(`${API_BASE_URL}/job/`, { headers: authHeaders() });
    return response.data;
}
export async function getJob(id: string):
Promise<Job>{
    const response = await axios.get(`${API_BASE_URL}/job/${id}`, { headers: authHeaders() });
    return response.data;
}

export async function createJob(job: Job):
Promise<Job>{
    const response = await axios.post(`${API_BASE_URL}/job/`, job, { headers: authHeaders() });
    return response.data;
}

export async function updateJob(id: string,job: Job):
Promise<Job> {
    const response = await axios.put(`${API_BASE_URL}/job/${id}`, job, { headers: authHeaders() });
    return response.data;
}

export async function deleteJob(id: string): Promise<void> {
    await axios.delete(`${API_BASE_URL}/job/${id}`, { headers: authHeaders() });
}
