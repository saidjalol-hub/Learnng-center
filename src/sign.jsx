import { useState } from "react";

function Sign() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSign = (e) => {
    e.preventDefault();

    if (email === "admin@gmail.com" && password === "123456") {
      setMessage("Успешная регистрация!");
    } else {
      setMessage("Ошибка регистрации");
    }
  };

  return (
    <div className="login-container">
      <h1>Регистрация</h1>

      <form onSubmit={handleSign}>
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

        <button type="submit">Зарегистрироваться</button>
      </form>

      <p>{message}</p>
    </div>
  );
}

export default Sign;