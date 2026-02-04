import { useEffect, useMemo, useState } from "react";

import { apiRequest } from "./api.js";

const initialForm = {
  title: "",
  description: "",
  priority: "MEDIA",
  status: "PENDIENTE",
  due_date: ""
};

const formatDateInput = (isoDate) => {
  if (!isoDate) return "";
  return isoDate.slice(0, 10);
};

const toIsoOrNull = (value) => {
  if (!value) return null;
  const date = new Date(value);
  return date.toISOString();
};

function App() {
  const [mode, setMode] = useState("login");
  const [token, setToken] = useState(localStorage.getItem("taskwise_token"));
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [tasks, setTasks] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const isAuthenticated = useMemo(() => Boolean(token), [token]);

  const loadTasks = async () => {
    if (!token) return;
    const data = await apiRequest("/tasks", { token });
    setTasks(data);
  };

  useEffect(() => {
    if (isAuthenticated) {
      loadTasks();
    }
  }, [isAuthenticated]);

  const handleAuth = async (event) => {
    event.preventDefault();
    setMessage("");
    setLoading(true);
    try {
      const endpoint = mode === "login" ? "/auth/login" : "/auth/register";
      const data = await apiRequest(endpoint, {
        method: "POST",
        body: { email, password }
      });
      localStorage.setItem("taskwise_token", data.access_token);
      setToken(data.access_token);
      setEmail("");
      setPassword("");
    } catch (error) {
      setMessage("No se pudo autenticar. Revisa tus credenciales.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("taskwise_token");
    setToken(null);
    setTasks([]);
    setEditingId(null);
    setForm(initialForm);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage("");
    setLoading(true);
    try {
      const payload = {
        title: form.title.trim(),
        description: form.description.trim() || null,
        priority: form.priority,
        status: form.status,
        due_date: toIsoOrNull(form.due_date)
      };

      if (editingId) {
        await apiRequest(`/tasks/${editingId}`, {
          method: "PUT",
          body: payload,
          token
        });
      } else {
        await apiRequest("/tasks", { method: "POST", body: payload, token });
      }

      await loadTasks();
      setForm(initialForm);
      setEditingId(null);
    } catch (error) {
      setMessage("No se pudo guardar la tarea.");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (task) => {
    setEditingId(task.id);
    setForm({
      title: task.title,
      description: task.description || "",
      priority: task.priority,
      status: task.status,
      due_date: formatDateInput(task.due_date)
    });
  };

  const handleCancelEdit = () => {
    setEditingId(null);
    setForm(initialForm);
  };

  const handleDelete = async (event, taskId) => {
    event.stopPropagation();
    setMessage("");
    setLoading(true);
    try {
      await apiRequest(`/tasks/${taskId}`, { method: "DELETE", token });
      await loadTasks();
      if (editingId === taskId) {
        handleCancelEdit();
      }
    } catch (error) {
      setMessage("No se pudo eliminar la tarea.");
    } finally {
      setLoading(false);
    }
  };

  const handleSuggest = async () => {
    setMessage("");
    setLoading(true);
    try {
      const data = await apiRequest("/tasks/ai/suggest", {
        method: "POST",
        token,
        body: {
          title: form.title.trim(),
          description: form.description.trim() || null,
          due_date: toIsoOrNull(form.due_date)
        }
      });
      setForm((prev) => ({
        ...prev,
        description: data.description_generated,
        priority: data.priority_suggested
      }));
    } catch (error) {
      setMessage("No se pudo generar la sugerencia.");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="page">
        <div className="card">
          <h1>TaskWise IA</h1>
          <p>Gestiona tus tareas y recibe sugerencias inteligentes.</p>
          <form className="form" onSubmit={handleAuth}>
            <label>
              Email
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </label>
            <label>
              Contraseña
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                minLength={8}
                required
              />
            </label>
            {message && <span className="message error">{message}</span>}
            <button type="submit" disabled={loading}>
              {mode === "login" ? "Iniciar sesión" : "Crear cuenta"}
            </button>
          </form>
          <button
            className="link"
            type="button"
            onClick={() => setMode(mode === "login" ? "register" : "login")}
          >
            {mode === "login" ? "¿No tienes cuenta? Regístrate" : "¿Ya tienes cuenta? Inicia sesión"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>TaskWise IA</h1>
          <p>Organiza tu semana con prioridad inteligente.</p>
        </div>
        <button type="button" onClick={handleLogout} className="secondary">
          Cerrar sesión
        </button>
      </header>

      <main className="content">
        <section className="tasks">
          <h2>Tus tareas</h2>
          <div className="task-list">
            {tasks.length === 0 && <p className="muted">Aún no tienes tareas.</p>}
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`task ${editingId === task.id ? "active" : ""}`}
                role="button"
                tabIndex={0}
                onClick={() => handleEdit(task)}
              >
                <div>
                  <h3>{task.title}</h3>
                  <p>{task.description || "Sin descripción"}</p>
                  <div className="meta">
                    <span>{task.priority}</span>
                    <span>{task.status}</span>
                    {task.due_date && <span>Vence: {formatDateInput(task.due_date)}</span>}
                  </div>
                </div>
                <button
                  type="button"
                  className="danger"
                  onClick={(event) => handleDelete(event, task.id)}
                >
                  Eliminar
                </button>
              </div>
            ))}
          </div>
        </section>

        <section className="form-panel">
          <h2>{editingId ? "Editar tarea" : "Nueva tarea"}</h2>
          <form className="form" onSubmit={handleSubmit}>
            <label>
              Título
              <input name="title" value={form.title} onChange={handleChange} required />
            </label>
            <label>
              Descripción
              <textarea name="description" value={form.description} onChange={handleChange} />
            </label>
            <label>
              Prioridad
              <select name="priority" value={form.priority} onChange={handleChange}>
                <option value="ALTA">ALTA</option>
                <option value="MEDIA">MEDIA</option>
                <option value="BAJA">BAJA</option>
              </select>
            </label>
            <label>
              Estado
              <select name="status" value={form.status} onChange={handleChange}>
                <option value="PENDIENTE">PENDIENTE</option>
                <option value="EN_PROGRESO">EN_PROGRESO</option>
                <option value="COMPLETADA">COMPLETADA</option>
              </select>
            </label>
            <label>
              Fecha límite
              <input type="date" name="due_date" value={form.due_date} onChange={handleChange} />
            </label>
            <div className="actions">
              <button type="button" className="secondary" onClick={handleSuggest} disabled={!form.title}>
                ✨ Sugerir con IA
              </button>
              <button type="submit" disabled={loading}>
                {editingId ? "Guardar cambios" : "Crear"}
              </button>
              {editingId && (
                <button type="button" className="ghost" onClick={handleCancelEdit}>
                  Cancelar edición
                </button>
              )}
            </div>
            {message && <span className="message error">{message}</span>}
          </form>
        </section>
      </main>
    </div>
  );
}

export default App;
