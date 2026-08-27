const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("form-ingreso");
const inputPlaca = document.getElementById("placa");
const mensaje = document.getElementById("mensaje");
const tablaActivos = document.getElementById("tabla-activos");
const contadorActivos = document.getElementById("contador-activos");
const clock = document.getElementById("clock");

const modal = document.getElementById("modal-salida");
const btnCerrarModal = document.getElementById("btn-cerrar-modal");

// -------------------- Reloj en vivo --------------------
function actualizarReloj() {
  clock.textContent = new Date().toLocaleTimeString("es-EC");
}
setInterval(actualizarReloj, 1000);
actualizarReloj();

// -------------------- Utilidades --------------------

// El backend devuelve datetimes "naive" (sin zona horaria) que en realidad
// están en UTC. Si el string no trae ya 'Z' o un offset (+hh:mm), se lo
// agregamos para que el navegador lo interprete como UTC y lo convierta
// correctamente a la hora local del usuario (Ecuador, UTC-5).
function parseUTC(isoString) {
  const tieneZonaHoraria = /Z$|[+-]\d{2}:\d{2}$/.test(isoString);
  return new Date(tieneZonaHoraria ? isoString : `${isoString}Z`);
}

function formatearFecha(isoString) {
  const fecha = parseUTC(isoString);
  return fecha.toLocaleString("es-EC", {
    day: "2-digit", month: "2-digit", year: "2-digit",
    hour: "2-digit", minute: "2-digit"
  });
}

function tiempoTranscurrido(isoEntrada) {
  const entrada = parseUTC(isoEntrada);
  const ahora = new Date();
  const minutos = Math.floor((ahora - entrada) / 60000);
  const horas = Math.floor(minutos / 60);
  const min = minutos % 60;
  return `${horas}h ${min}m`;
}

function mostrarMensaje(texto, tipo) {
  mensaje.textContent = texto;
  mensaje.hidden = false;
  mensaje.className = `feedback feedback--${tipo}`;
  setTimeout(() => { mensaje.hidden = true; }, 4000);
}

// -------------------- Cargar vehículos activos --------------------
async function cargarActivos() {
  try {
    const res = await fetch(`${API_URL}/parqueadero/activos`);
    if (!res.ok) throw new Error("No se pudo consultar el parqueadero.");
    const activos = await res.json();
    renderizarActivos(activos);
  } catch (err) {
    console.error(err);
  }
}

function renderizarActivos(activos) {
  contadorActivos.textContent = activos.length;

  if (activos.length === 0) {
    tablaActivos.innerHTML = `
      <tr class="empty-row">
        <td colspan="4">No hay vehículos registrados todavía.</td>
      </tr>`;
    return;
  }

  tablaActivos.innerHTML = activos.map((v) => `
    <tr data-id="${v.id}">
      <td><span class="plate">${v.placa}</span></td>
      <td>${formatearFecha(v.fecha_entrada)}</td>
      <td><span class="time-elapsed" data-entrada="${v.fecha_entrada}">${tiempoTranscurrido(v.fecha_entrada)}</span></td>
      <td><button class="btn-exit" data-id="${v.id}">Registrar salida</button></td>
    </tr>
  `).join("");

  document.querySelectorAll(".btn-exit").forEach((btn) => {
    btn.addEventListener("click", () => registrarSalida(btn.dataset.id));
  });
}

// Refresca el contador de "tiempo transcurrido" cada segundo sin re-consultar la API
setInterval(() => {
  document.querySelectorAll(".time-elapsed").forEach((el) => {
    el.textContent = tiempoTranscurrido(el.dataset.entrada);
  });
}, 1000);

// -------------------- Registrar ingreso --------------------
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const placa = inputPlaca.value.trim();
  if (!placa) return;

  try {
    const res = await fetch(`${API_URL}/parqueadero/ingreso`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ placa })
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "No se pudo registrar el ingreso.");
    }

    mostrarMensaje(`Vehículo ${data.placa} registrado.`, "ok");
    inputPlaca.value = "";
    cargarActivos();
  } catch (err) {
    mostrarMensaje(err.message, "error");
  }
});

// -------------------- Registrar salida --------------------
async function registrarSalida(id) {
  try {
    const res = await fetch(`${API_URL}/parqueadero/salida/${id}`, {
      method: "PUT"
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "No se pudo registrar la salida.");
    }

    mostrarTicket(data);
    cargarActivos();
  } catch (err) {
    mostrarMensaje(err.message, "error");
  }
}

function mostrarTicket(data) {
  document.getElementById("ticket-placa").textContent = data.placa;
  document.getElementById("ticket-entrada").textContent = formatearFecha(data.fecha_entrada);
  document.getElementById("ticket-salida").textContent = formatearFecha(data.fecha_salida);
  document.getElementById("ticket-fracciones").textContent = data.horas_o_fracciones;
  document.getElementById("ticket-monto").textContent = `$${data.monto.toFixed(2)}`;
  modal.hidden = false;
}

btnCerrarModal.addEventListener("click", () => { modal.hidden = true; });

// -------------------- Init --------------------
cargarActivos();
setInterval(cargarActivos, 15000); // refresco automático cada 15s