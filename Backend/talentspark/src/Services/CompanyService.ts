import axios from "axios";
import type {Company} from "../types/company";

const API_BASE_URL = "http://localhost:8000";

function authHeaders() {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getCompanies(): Promise<Company[]> {
    const response = await axios.get(`${API_BASE_URL}/company/`, { headers: authHeaders() });
    return response.data;
}
export async function getCompany(id: string):
Promise<Company>{
    const response = await axios.get(`${API_BASE_URL}/company/${id}`, { headers: authHeaders() });
    return response.data;
}

export async function createCompany(company: Company):
Promise<Company>{
    const response = await axios.post(`${API_BASE_URL}/company/`, company, { headers: authHeaders() });
    return response.data;
}

export async function updateCompany(id: string,company: Company):
Promise<Company> {
    const response = await axios.put(`${API_BASE_URL}/company/${id}`, company, { headers: authHeaders() });
    return response.data;
}

export async function deleteCompany(id: string): Promise<void> {
    await axios.delete(`${API_BASE_URL}/company/${id}`, { headers: authHeaders() });
}
