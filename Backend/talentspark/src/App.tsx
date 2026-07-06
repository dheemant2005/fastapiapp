import Welcome from "./components/Welcome";
import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import {useEffect,useState} from "react";
import {
  createCompany,
  deleteCompany,
  getCompanies,
  updateCompany,
} from "./Services/CompanyService";
import { login } from "./Services/AuthService";
import type {Company} from "./types/company"

function App(){
  const [token,setToken] = useState(() => localStorage.getItem("access_token"));
  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");
  const [loading,setLoading] = useState(Boolean(token));
  const [error,setError] = useState<Error | null>(null)
  const [companies,setCompanies] = useState<Company[]>([]);

  async function fetchCompanies() {
    setLoading(true);
    setError(null);
    try {
      const companies = await getCompanies();
      setCompanies(companies);
    } catch (error) {
      setError(error as Error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!token) return;

    let cancelled = false;
    getCompanies()
      .then((loadedCompanies) => {
        if (!cancelled) setCompanies(loadedCompanies);
      })
      .catch((requestError) => {
        if (!cancelled) setError(requestError as Error);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [token]);

  async function handleLogin(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const accessToken = await login(email, password);
      localStorage.setItem("access_token", accessToken);
      setToken(accessToken);
    } catch (loginError) {
      setError(loginError as Error);
      setLoading(false);
    }
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    setToken(null);
    setCompanies([]);
    setError(null);
  }

  async function handleAdd(company: Company) {
    try {
      const created = await createCompany(company);
      setCompanies((current) => [...current, created]);
    } catch (requestError) {
      setError(requestError as Error);
    }
  }

  async function handleEdit(company: Company) {
    try {
      await updateCompany(String(company.id), company);
      await fetchCompanies();
    } catch (requestError) {
      setError(requestError as Error);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteCompany(String(id));
      setCompanies((current) => current.filter((company) => company.id !== id));
    } catch (requestError) {
      setError(requestError as Error);
    }
  }

  if (!token) {
    return (
      <main>
        <h1>TalentSpark Login</h1>
        <form onSubmit={handleLogin}>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="Email"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Password"
            required
          />
          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
        {error && <p>Error: {error.message}</p>}
      </main>
    );
  }
  
  if(loading){
    return <div>Loading...</div>
  }

  if(error){
    return (
      <div>
        <p>Error: {error.message}</p>
        <button onClick={handleLogout}>Sign out</button>
      </div>
    )
  }
  
  return(
    <>
    <NavBar />
    <button onClick={handleLogout}>Sign out</button>
    <Welcome />
    <br />
    <CompanyCard
      companies={companies}
      onadd={handleAdd}
      onedit={handleEdit}
      ondelete={handleDelete}
    />
    <JobCard />
    <Footer />
    </>
  )
}
export default App
