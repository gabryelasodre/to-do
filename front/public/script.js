const API_URL = 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', buscarTarefas);

function buscarTarefas() {
  fetch(API_URL)
    .then(res => res.json())
    .then(tarefas => {
      const lista = document.getElementById('listaTarefas');
      lista.innerHTML = '';
      tarefas.forEach(adicionarElemento);
    });
}

function adicionarTarefa() {
  const input = document.getElementById('novaTarefa');
  const title = input.value.trim();
  if (!title) return;

  fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title })
  })
    .then(() => {
      input.value = '';
      buscarTarefas();
    });
}

function alternarConclusao(tarefa) {
  fetch(`${API_URL}?id=${tarefa.id}`, {
    method: 'PUT'
  }).then(buscarTarefas);
}

function removerTarefa(id) {
  fetch(`${API_URL}/${id}`, {
    method: 'DELETE'
  }).then(buscarTarefas);
}

function adicionarElemento(tarefa) {
  const div = document.createElement('div');
  div.className = 'todo-item';
  if (tarefa.checked) div.classList.add('completed');

  const icone = document.createElement('span');
  icone.className = 'check-circle';
  icone.innerHTML = tarefa.checked ? '✔️' : '⚪';
  icone.onclick = () => alternarConclusao(tarefa);

  const texto = document.createElement('span');
  texto.textContent = tarefa.title;

  const btnExcluir = document.createElement('button');
  btnExcluir.className = 'delete-btn';
  btnExcluir.textContent = 'x';
  btnExcluir.onclick = () => removerTarefa(tarefa.id);

  div.appendChild(icone);
  div.appendChild(texto);
  div.appendChild(btnExcluir);

  document.getElementById('listaTarefas').appendChild(div);
}
