import axios from "axios";
import type {Job} from "../types/job";

const API_BASE_URL = "http://localhost:8000";

export async function getJobs(): Promise<Job[]> {
    const response = await axios.get(`${API_BASE_URL}/job`);
    return response.data;
}
export async function getJob(id: string):
Promise<Job>{
    const response = await axios.get(`${API_BASE_URL}/
    job/${id}`);
    return response.data;
}

export async function createJob(company: Job):
Promise<Job>{
    const response = await axios.post(`${API_BASE_URL}/job`, job);
    return response.data;
}

export async function updateJob(id: string,job: Job):
Promise<Job> {
    const response = await axios.put(`${API_BASE_URL}/job/${id}`, job);
    return response.data;
}

export async function deleteJob(id: string):
Promise<Job> {
    const response = await axios.delete(`${API_BASE_URL}/job/${id}`);
    return response.data;
}
