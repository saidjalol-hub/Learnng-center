import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Admin() {
  const [requests, setRequests] = useState([]);
  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState("Загрузка...");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    fetch("/api/v1/users/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setProfile(data));

    fetch("/api/v1/admin/lesson-requests", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.lesson_requests.length === 0) {
          setMessage("Заявок пока нет");
        } else {
          setMessage("");
        }
        setRequests(data.lesson_requests);
      })
      .catch(() => setMessage("Ошибка загрузки"));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Панель администратора</h1>
        <button onClick={handleLogout}>Выйти</button>
      </div>

      {profile && (
        <div className="profile-card">
          <h2>Профиль</h2>
          <p><strong>Имя:</strong> {profile.first_name} {profile.last_name}</p>
          <p><strong>Email:</strong> {profile.email}</p>
        </div>
      )}

      <div className="schedule">
        <h2>Заявки на уроки</h2>
        {message && <p>{message}</p>}
        {requests.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Студент</th>
                <th>Телефон</th>
                <th>Статус</th>
                <th>Учитель</th>
                <th>Время урока</th>
                <th>Создано</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((req) => (
                <tr key={req.id}>
                  <td>{req.first_name}</td>
                  <td>{req.phone_number}</td>
                  <td>{req.status}</td>
                  <td>{req.teacher ? `${req.teacher.first_name} ${req.teacher.last_name}` : "Не назначен"}</td>
                  <td>{req.lesson_time ? new Date(req.lesson_time).toLocaleString("ru-RU") : "—"}</td>
                  <td>{new Date(req.created_at).toLocaleString("ru-RU")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Admin;