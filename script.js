document.getElementById("data-atual").innerText = new Date().toLocaleString("pt-BR");

function mostrarOutros(valor) {
  const outrosLabel = document.getElementById("outrosLabel");
  outrosLabel.style.display = valor === "Outro" ? "block" : "none";
  if (valor !== "Outro") document.getElementById("outros_causa").value = "";
}

function limparFormulario() {
  document.getElementById("formulario").reset();
  document.getElementById("resumo").value = "";
}

function gerarRelatorio() {
  const form = document.getElementById("formulario");
  const dados = Object.fromEntries(new FormData(form).entries());
  if (!dados.descricao || !dados.chamado || !dados.os || !dados.endereco || !dados.causa) {
    alert("Preencha todos os campos obrigatórios!");
    return;
  }

  const causa = dados.causa === "Outro" ? `${dados.causa} (${dados.outros_causa || "Não especificado"})` : dados.causa;

  const resumo = `
RELATÓRIO DE BAIXA/RFO - ALLOHA FIBRA
Data: ${new Date().toLocaleString("pt-BR")}
Descrição: ${dados.descricao}
Chamado: ${dados.chamado}
OS: ${dados.os}
Endereço: ${dados.endereco}
KM da Falha: ${dados.km_falha}
Local Medição: ${dados.local_medicao}
Causa: ${causa}
Ação Executada: ${dados.acao_executada}
Material Utilizado: ${dados.material_usado}
Fibra: ${dados.fibra}
Fusões: ${dados.fusoes}
Localização: ${dados.localizacao}
`.trim();

  document.getElementById("resumo").value = resumo;
}

function copiarRelatorio() {
  const texto = document.getElementById("resumo").value;
  if (texto) {
    navigator.clipboard.writeText(texto);
    alert("Relatório copiado!");
  } else {
    alert("Gere o relatório primeiro!");
  }
}

function enviarWhatsApp() {
  const texto = document.getElementById("resumo").value;
  if (texto) {
    const msg = encodeURIComponent(texto);
    window.open(`https://wa.me/?text=${msg}`, "_blank");
  } else {
    alert("Gere o relatório primeiro!");
  }
}

function salvarTxt() {
  const texto = document.getElementById("resumo").value;
  if (texto) {
    const blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    const link = document.createElement("a");
    link.href =