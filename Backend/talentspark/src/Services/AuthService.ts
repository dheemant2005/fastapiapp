import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

type TokenResponse = {
    access_token: string;
    token_type: string;
};

export async function login(email: string, password: string): Promise<string> {
    const form = new URLSearchParams({ username: email, password });
    const response = await axios.post<TokenResponse>(
        `${API_BASE_URL}/auth/login`,
        form,
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
    );
    return response.data.access_token;
}
