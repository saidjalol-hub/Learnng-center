import { useNavigate } from "react-router-dom";

const student = {
  name: "Алишер Каримов",
  email: "student@gmail.com",
  group: "Группа A1",
};

const schedule = [
  { day: "Понедельник", subject: "Математика", time: "09:00 - 10:30", teacher: "********" },
  { day: "Вторник", subject: "Английский", time: "11:00 - 12:30", teacher: "********" },
  { day: "Среда", subject: "Программирование", time: "09:00 - 10:30", teacher: "********" },
  { day: "Четверг", subject: "Математика", time: "11:00 - 12:30", teacher: "********" },
  { day: "Пятница", subject: "Английский", time: "09:00 - 10:30", teacher: "********" },
];

function Student() {
  const navigate = useNavigate();

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Личный кабинет студента</h1>
        <button onClick={() => navigate("/")}>Выйти</button>
      </div>

      <div className="profile-card">
        <h2>Профиль</h2>
        <p><strong>Имя:</strong> {student.name}</p>
        <p><strong>Email:</strong> {student.email}</p>
        <p><strong>Группа:</strong> {student.group}</p>
      </div>

      <div className="schedule">
        <h2>Расписание уроков</h2>
        <table>
          <thead>
            <tr>
              <th>День</th>
              <th>Предмет</th>
              <th>Время</th>
              <th>Учитель</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((lesson, index) => (
              <tr key={index}>
                <td>{lesson.day}</td>
                <td>{lesson.subject}</td>
                <td>{lesson.time}</td>
                <td>{lesson.teacher}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Student;