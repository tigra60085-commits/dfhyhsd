'use strict';

const STORAGE_KEY = 'todos';

// ── State ──────────────────────────────────────────────────────────────────

let todos = loadTodos();
let currentFilter = 'all';

// ── Persistence ────────────────────────────────────────────────────────────

function loadTodos() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveTodos() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
}

// ── Mutations ──────────────────────────────────────────────────────────────

function addTodo(text) {
  const trimmed = text.trim();
  if (!trimmed) return;
  todos.push({ id: crypto.randomUUID(), text: trimmed, completed: false });
  saveTodos();
  render();
}

function toggleTodo(id) {
  const todo = todos.find(t => t.id === id);
  if (todo) {
    todo.completed = !todo.completed;
    saveTodos();
    render();
  }
}

function deleteTodo(id) {
  todos = todos.filter(t => t.id !== id);
  saveTodos();
  render();
}

function clearCompleted() {
  todos = todos.filter(t => !t.completed);
  saveTodos();
  render();
}

// ── Rendering ──────────────────────────────────────────────────────────────

function getFiltered() {
  switch (currentFilter) {
    case 'active':    return todos.filter(t => !t.completed);
    case 'completed': return todos.filter(t => t.completed);
    default:          return todos;
  }
}

function render() {
  const list    = document.getElementById('todo-list');
  const footer  = document.getElementById('footer');
  const counter = document.getElementById('counter');
  const filtered = getFiltered();

  // List
  list.innerHTML = '';

  if (filtered.length === 0) {
    const li = document.createElement('li');
    li.className = 'empty-state';
    li.textContent = currentFilter === 'completed'
      ? 'Нет выполненных задач.'
      : currentFilter === 'active'
        ? 'Нет активных задач.'
        : 'Список пуст. Добавьте первую задачу!';
    list.appendChild(li);
  } else {
    for (const todo of filtered) {
      list.appendChild(createTodoItem(todo));
    }
  }

  // Footer
  if (todos.length === 0) {
    footer.classList.add('hidden');
  } else {
    footer.classList.remove('hidden');
    const activeCount = todos.filter(t => !t.completed).length;
    counter.textContent = `${activeCount} ${plural(activeCount, 'задача', 'задачи', 'задач')} осталось`;
  }
}

function createTodoItem(todo) {
  const li = document.createElement('li');
  if (todo.completed) li.classList.add('completed');

  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.checked = todo.completed;
  checkbox.setAttribute('aria-label', `Отметить: ${todo.text}`);
  checkbox.addEventListener('change', () => toggleTodo(todo.id));

  const span = document.createElement('span');
  span.className = 'todo-text';
  span.textContent = todo.text;

  const deleteBtn = document.createElement('button');
  deleteBtn.className = 'delete-btn';
  deleteBtn.textContent = '×';
  deleteBtn.setAttribute('aria-label', `Удалить: ${todo.text}`);
  deleteBtn.addEventListener('click', () => deleteTodo(todo.id));

  li.append(checkbox, span, deleteBtn);
  return li;
}

// ── Helpers ────────────────────────────────────────────────────────────────

function plural(n, one, few, many) {
  const mod10  = n % 10;
  const mod100 = n % 100;
  if (mod100 >= 11 && mod100 <= 14) return many;
  if (mod10 === 1) return one;
  if (mod10 >= 2 && mod10 <= 4) return few;
  return many;
}

// ── Bootstrap ──────────────────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  const input    = document.getElementById('new-todo');
  const addBtn   = document.getElementById('add-btn');
  const clearBtn = document.getElementById('clear-completed');
  const filterBtns = document.querySelectorAll('.filter-btn');

  addBtn.addEventListener('click', () => {
    addTodo(input.value);
    input.value = '';
    input.focus();
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      addTodo(input.value);
      input.value = '';
    }
  });

  clearBtn.addEventListener('click', clearCompleted);

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.filter;
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    });
  });

  render();
});
