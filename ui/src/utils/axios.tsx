import axios from "axios";


const api = axios.create({
  baseURL: import.meta.env.VITE_API_HOST || "http://localhost:8000",
});


export { api };
