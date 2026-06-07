const API = '/api'; const Storage = {
getUser: () =>
JSON.parse(localStorage.getItem('user')), setUser: (u) => localStorage.setItem('user', JSON.stringify(u)), logout: () => localStorage.removeItem('user')
};
const Auth = {
register: (data) => fetch(`${API}/auth/register`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(data)
}).then(r => r.json()),
Login: async (email, password) => { const r = await fetch(`${API}/auth/login`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify({email, password})
}); const res = await r.json(); if(res.success) Storage.setUser(res.user); return res;
}, isLogin: () => !!Storage.getUser()
};
const Chat = {
reply: (msg) => { msg = msg.toLowerCase(); if(msg.includes('payment')) return "Fee is ₹299"; if(msg.includes('exam')) return "Mock test available"; return "Ask about exam or payment"; }
}; const Payment = {
confirm: (email) => fetch(`${API}/pay`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email})
}).then(r => r.json())
};
function toast(msg){
alert(msg); } document.addEventListener('DOMContentLoaded', () => { if(!Auth.isLogin()){ console.log("Not Logged In");
}
});
