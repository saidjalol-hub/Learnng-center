import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function Teacher() {
  const [lessons, setLessons] = useState([]);
  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState("Загрузка...");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    fetch("http://localhost:8000/v1/users/me", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setProfile(data));

    fetch("http://localhost:8000/v1/teacher/my-lessons", {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.lessons.length === 0) {
          setMessage("Уроков пока нет");
        } else {
          setMessage("");
        }
        setLessons(data.lessons);
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
        <h1>Личный кабинет учителя</h1>
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
        <h2>Мои уроки</h2>
        {message && <p>{message}</p>}
        {lessons.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>Студент</th>
                <th>Телефон</th>
                <th>Время урока</th>
                <th>Статус</th>
              </tr>
            </thead>
            <tbody>
              {lessons.map((lesson) => (
                <tr key={lesson.id}>
                  <td>{lesson.student.first_name}</td>
                  <td>{lesson.student.phone_number}</td>
                  <td>{new Date(lesson.lesson_time).toLocaleString("ru-RU")}</td>
                  <td>{lesson.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Teacher;