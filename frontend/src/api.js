const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
export function getTokens(){ return JSON.parse(localStorage.getItem("cv_tokens") || "null"); }
export function setTokens(tokens){ localStorage.setItem("cv_tokens", JSON.stringify(tokens)); }
export function clearTokens(){ localStorage.removeItem("cv_tokens"); }
export async function api(path, options={}) {
  const tokens=getTokens();
  const headers={...(options.body instanceof FormData?{}:{"Content-Type":"application/json"}), ...(options.headers||{})};
  if(tokens?.access) headers.Authorization=`Bearer ${tokens.access}`;
  let response=await fetch(`${BASE}${path}`,{...options,headers});
  if(response.status===401 && tokens?.refresh){
    const refresh=await fetch(`${BASE}/auth/token/refresh/`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({refresh:tokens.refresh})});
    if(refresh.ok){const next=await refresh.json();setTokens({...tokens,access:next.access});headers.Authorization=`Bearer ${next.access}`;response=await fetch(`${BASE}${path}`,{...options,headers});}
  }
  if(!response.ok){let msg="Request failed";try{const data=await response.json();msg=JSON.stringify(data);}catch{}throw new Error(msg);}
  return response;
}
export async function json(path, options={}) { const r=await api(path,{...options,body:options.body?JSON.stringify(options.body):undefined}); return r.status===204?null:r.json(); }
export async function download(path, filename){const r=await api(path);const blob=await r.blob();const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=filename;a.click();URL.revokeObjectURL(url);}
