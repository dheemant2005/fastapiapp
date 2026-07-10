import api from "./api";
import type { JobMatchResponse, SemanticSearchResponse, EmbedResult, ResumeAnalysis } from "../types/rag";

export async function embedJobs(): Promise<EmbedResult> {
    const response = await api.post<EmbedResult>("/rag/embed-jobs");
    return response.data;
}

export async function semanticSearch(query: string): Promise<SemanticSearchResponse> {
    const response = await api.post<SemanticSearchResponse>("/rag/search", { query });
    return response.data;
}

export async function matchJobs(skills: string, experience: string): Promise<JobMatchResponse> {
    const response = await api.post<JobMatchResponse>("/rag/job-match", { skills, experience });
    return response.data;
}

export async function analyseResume(resumeText: string): Promise<ResumeAnalysis> {
    const response = await api.post<ResumeAnalysis>("/rag/analyse-resume", { resume_text: resumeText });
    return response.data;
}
