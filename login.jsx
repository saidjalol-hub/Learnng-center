import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/v1/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        setMessage("Неверный логин или пароль");
        return;
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token);

      const meRes = await fetch("http://localhost:8000/v1/users/me", {
        headers: { Authorization: `Bearer ${data.access_token}` },
      });

      const me = await meRes.json();

      if (me.role === "admin") navigate("/admin");
      else if (me.role === "teacher") navigate("/teacher");
      else navigate("/student");

    } catch {
      setMessage("Ошибка соединения с сервером");
    }
  };

  return (
    <div className="login-container">
      <h1>Вход</h1>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Введите email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Введите пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Войти</button>
      </form>
      <p>{message}</p>
    </div>
  );
}

export default Login;