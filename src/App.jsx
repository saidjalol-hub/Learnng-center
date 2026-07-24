import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Student from './Student'
import Admin from './admin'
import Teacher from './Teacher'
import Login from './Login'
import Sign from './Sign'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Sign />} />
        <Route path="/student" element={<Student />} />
        <Route path="/admin" element={<Admin />} />
        <Route path="/teacher" element={<Teacher />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App