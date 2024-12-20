'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import mysql from 'mysql2/promise'

// Database connection
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'project',
  database: 'hospital_management',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
})

// Types
interface Question {
  id: number
  title: string
  content: string
  author: string
  answers: Answer[]
  locked: boolean
}

interface Answer {
  id: number
  content: string
  author: string
}

// Login Page
function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [userType, setUserType] = useState('patient')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, userType }),
    })

    if (response.ok) {
      router.push('/dashboard')
    } else {
      alert('Login failed')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded shadow-md w-96">
        <form onSubmit={handleSubmit} className="space-y-4">
          <h1 className="mb-6 text-2xl font-bold text-center">Login</h1>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="userType">I am a:</Label>
            <select
              id="userType"
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
              className="w-full p-2 border rounded"
            >
              <option value="patient">Patient</option>
              <option value="doctor">Doctor</option>
            </select>
          </div>
          <Button type="submit" className="w-full">Login</Button>
        </form>
        <div className="mt-4 text-center">
          <Link href="/register" className="text-blue-500 hover:underline">
            Register as a new user
          </Link>
        </div>
      </div>
    </div>
  )
}

// Registration Page
function RegisterPage() {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [userType, setUserType] = useState('patient')
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password, userType }),
    })

    if (response.ok) {
      alert('Registration successful')
      router.push('/login')
    } else {
      alert('Registration failed')
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="p-8 bg-white rounded shadow-md w-96">
        <form onSubmit={handleSubmit} className="space-y-4">
          <h1 className="mb-6 text-2xl font-bold text-center">Register</h1>
          <div>
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="userType">I am a:</Label>
            <select
              id="userType"
              value={userType}
              onChange={(e) => setUserType(e.target.value)}
              className="w-full p-2 border rounded"
            >
              <option value="patient">Patient</option>
              <option value="doctor">Doctor</option>
            </select>
          </div>
          <Button type="submit" className="w-full">Register</Button>
        </form>
        <div className="mt-4 text-center">
          <Link href="/login" className="text-blue-500 hover:underline">
            Already have an account? Login
          </Link>
        </div>
      </div>
    </div>
  )
}

// Profile Page
function ProfilePage() {
  const [name, setName] = useState('')
  const [bio, setBio] = useState('')

  useEffect(() => {
    const fetchProfile = async () => {
      const response = await fetch('/api/profile')
      if (response.ok) {
        const data = await response.json()
        setName(data.name)
        setBio(data.bio)
      }
    }
    fetchProfile()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const response = await fetch('/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, bio }),
    })

    if (response.ok) {
      alert('Profile updated successfully')
    } else {
      alert('Failed to update profile')
    }
  }

  return (
    <div className="container mx-auto mt-8">
      <h1 className="mb-6 text-2xl font-bold">Your Profile</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <Label htmlFor="bio">Bio</Label>
          <Textarea
            id="bio"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
            rows={4}
          />
        </div>
        <Button type="submit">Update Profile</Button>
      </form>
    </div>
  )
}

// Questions Page
function QuestionsPage() {
  const [questions, setQuestions] = useState<Question[]>([])
  const [newQuestion, setNewQuestion] = useState({ title: '', content: '' })

  useEffect(() => {
    const fetchQuestions = async () => {
      const response = await fetch('/api/questions')
      if (response.ok) {
        const data = await response.json()
        setQuestions(data)
      }
    }
    fetchQuestions()
  }, [])

  const handleSubmitQuestion = async (e: React.FormEvent) => {
    e.preventDefault()
    const response = await fetch('/api/questions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newQuestion),
    })

    if (response.ok) {
      const data = await response.json()
      setQuestions([...questions, data])
      setNewQuestion({ title: '', content: '' })
    } else {
      alert('Failed to post question')
    }
  }

  return (
    <div className="container mx-auto mt-8">
      <h1 className="mb-6 text-2xl font-bold">Questions</h1>
      <form onSubmit={handleSubmitQuestion} className="mb-8 space-y-4">
        <Input
          placeholder="Question title"
          value={newQuestion.title}
          onChange={(e) => setNewQuestion({ ...newQuestion, title: e.target.value })}
          required
        />
        <Textarea
          placeholder="Question content"
          value={newQuestion.content}
          onChange={(e) => setNewQuestion({ ...newQuestion, content: e.target.value })}
          required
        />
        <Button type="submit">Ask Question</Button>
      </form>
      <div className="space-y-6">
        {questions.map((question) => (
          <div key={question.id} className="p-4 border rounded">
            <h2 className="text-xl font-bold">{question.title}</h2>
            <p>{question.content}</p>
            <p className="mt-2 text-sm text-gray-500">Asked by: {question.author}</p>
            <div className="mt-4 space-y-2">
              {question.answers.map((answer) => (
                <div key={answer.id} className="p-2 bg-gray-100 rounded">
                  <p>{answer.content}</p>
                  <p className="mt-1 text-sm text-gray-500">Answered by: {answer.author}</p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Admin Page
function AdminPage() {
  const [questions, setQuestions] = useState<Question[]>([])

  useEffect(() => {
    const fetchQuestions = async () => {
      const response = await fetch('/api/admin/questions')
      if (response.ok) {
        const data = await response.json()
        setQuestions(data)
      }
    }
    fetchQuestions()
  }, [])

  const handleLockToggle = async (questionId: number) => {
    const response = await fetch(`/api/admin/questions/${questionId}/toggle-lock`, {
      method: 'POST',
    })

    if (response.ok) {
      setQuestions(questions.map(q => 
        q.id === questionId ? { ...q, locked: !q.locked } : q
      ))
    } else {
      alert('Failed to toggle lock')
    }
  }

  return (
    <div className="container mx-auto mt-8">
      <h1 className="mb-6 text-2xl font-bold">Admin Dashboard</h1>
      <div className="space-y-4">
        {questions.map((question) => (
          <div key={question.id} className="flex items-center justify-between p-4 border rounded">
            <span>{question.title}</span>
            <Button onClick={() => handleLockToggle(question.id)}>
              {question.locked ? 'Unlock' : 'Lock'}
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
}

// API Routes
async function loginHandler(req: Request) {
  const { email, password, userType } = await req.json()

  try {
    const [rows] = await pool.query(
      'SELECT * FROM users WHERE email = ? AND password = ? AND user_type = ?',
      [email, password, userType]
    )

    if (Array.isArray(rows) && rows.length > 0) {
      return new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      })
    } else {
      return new Response(JSON.stringify({ success: false, message: 'Invalid credentials' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      })
    }
  } catch (error) {
    console.error('Login error:', error)
    return new Response(JSON.stringify({ success: false, message: 'Server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}

async function registerHandler(req: Request) {
  const { name, email, password, userType } = await req.json()

  try {
    const [result] = await pool.query(
      'INSERT INTO users (name, email, password, user_type) VALUES (?, ?, ?, ?)',
      [name, email, password, userType]
    )

    if ('affectedRows' in result && result.affectedRows > 0) {
      return new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      })
    } else {
      return new Response(JSON.stringify({ success: false, message: 'Registration failed' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      })
    }
  } catch (error) {
    console.error('Registration error:', error)
    return new Response(JSON.stringify({ success: false, message: 'Server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}

async function profileHandler(req: Request) {
  if (req.method === 'GET') {
    const userId = 1 // This should come from the session

    try {
      const [rows] = await pool.query('SELECT name, bio FROM users WHERE id = ?', [userId])

      if (Array.isArray(rows) && rows.length > 0) {
        return new Response(JSON.stringify(rows[0]), {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        })
      } else {
        return new Response(JSON.stringify({ message: 'User not found' }), {
          status: 404,
          headers: { 'Content-Type': 'application/json' },
        })
      }
    } catch (error) {
      console.error('Profile fetch error:', error)
      return new Response(JSON.stringify({ message: 'Server error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      })
    }
  } else if (req.method === 'POST') {
    const { name, bio } = await req.json()
    const userId = 1 // This should come from the session

    try {
      await pool.query('UPDATE users SET name = ?, bio = ? WHERE id = ?', [name, bio, userId])
      return new Response(JSON.stringify({ success: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      })
    } catch (error) {
      console.error('Profile update error:', error)
      return new Response(JSON.stringify({ message: 'Server error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      })
    }
  }
}

async function questionsHandler(req: Request) {
  if (req.method === 'GET') {
    try {
      const [rows] = await pool.query(`
        SELECT q.id, q.title, q.content, u.name as author, 
               a.id as answer_id, a.content as answer_content, au.name as answer_author
        FROM questions q
        JOIN users u ON q.user_id = u.id
        LEFT JOIN answers a ON q.id = a.question_id
        LEFT JOIN users au ON a.user_id = au.id
        ORDER BY q.created_at DESC, a.created_at
      `)

      const questions = []
      let currentQuestion = null

      if (Array.isArray(rows)) {
        for (const row of rows) {
          if (!currentQuestion || currentQuestion.id !== row.id) {
            if (currentQuestion) {
              questions.push(currentQuestion)
            }
            currentQuestion = {
              id: row.id,
              title: row.title,
              content: row.content,
              author: row.author,
              answers: []
            }
          }
          if (row.answer_id) {
            currentQuestion.answers.push({
              id: row.answer_id,
              content: row.answer_content,
              author: row.answer_author
            })
          }
        }
        if (currentQuestion) {
          questions.push(currentQuestion)
        }
      }

      return new Response(JSON.stringify(questions), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      })
    } catch (error) {
      console.error('Questions fetch error:', error)
      return new Response(JSON.stringify({ message: 'Server error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      })
    }
  } else if (req.method === 'POST') {
    const { title, content } = await req.json()
    const userId = 1 // This should come from the session

    try {
      const [result] = await pool.query(
        'INSERT INTO questions (title, content, user_id) VALUES (?, ?, ?)',
        [title, content, userId]
      )

      if ('insertId' in result) {
        const newQuestionId = result.insertId
        const [rows] = await pool.query(
          'SELECT q.id, q.title, q.content, u.name as author FROM questions q JOIN users u ON q.user_id = u.id WHERE q.id = ?',
          [newQuestionId]
        )

        if (Array.isArray(rows) && rows.length > 0) {
          return new Response(JSON.stringify(rows[0]), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
          })
        }
      }

      return new Response(JSON.stringify({ message: 'Failed to create question' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      })
    } catch (error) {
      console.error('Question creation error:', error)
      return new Response(JSON.stringify({ message: 'Server error' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      })
    }
  }
}

async function adminQuestionsHandler(req: Request) {
  try {
    const [rows] = await pool.query('SELECT id, title, locked FROM questions ORDER BY created_at DESC')
    return new Response(JSON.stringify(rows), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    console.error('Admin questions fetch error:', error)
    return new Response(JSON.stringify({ message: 'Server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}

async function toggleLockHandler(req: Request, questionId: string) {
  try {
    await pool.query('UPDATE questions SET locked = NOT locked WHERE id = ?', [questionId])
    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    console.error('Question lock toggle error:', error)
    return new Response(JSON.stringify({ message: 'Server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}

// Main App Component
export default function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <Link href="/" className="text-xl font-bold text-gray-800">
                  MedicalQA
                </Link>
              </div>
              <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                <Link href="/questions" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300 text-sm font-medium">
                  Questions
                </Link>
                <Link href="/profile" className="text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-gray-300 text-sm font-medium">
                  Profile
                </Link>
              </div>
            </div>
            <div className="hidden sm:ml-6 sm:flex sm:items-center">
              <Button asChild>
                <Link href="/login">Login</Link>
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Router would go here in a real Next.js app */}
        <LoginPage />
        <RegisterPage />
        <ProfilePage />
        <QuestionsPage />
        <AdminPage />
      </main>
    </div>
  )
}
