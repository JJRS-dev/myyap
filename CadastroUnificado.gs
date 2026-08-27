const SPREADSHEET_ID = "1PW8l9sCgb_nTwDcmmsoEEMrD8yG67qs6BZmfodSU1s4";
const CLIENTS_SHEET = "Clientes";
const ORDERS_SHEET = "Pedidos";
const ORDER_STATUSES = ["Novo", "Confirmado", "Preparando", "Pronto", "Saiu para entrega", "Concluído", "Cancelado"];
const PRODUCT_PRICES_CENTS = {
  "arroz-integral": 890, "feijao-carioca": 950, "aveia-em-flocos": 620, "quinoa": 1890,
  "lentilha": 1140, "grao-de-bico": 1280, "castanha-do-para": 3490, "amendoas": 2950,
  "chia": 2200, "linhaca": 1550, "camomila": 1800, "hibisco": 2200, "erva-doce": 1650,
  "torradas-integrais": 1490, "batata-doce-temperada": 2600, "amendoim-sabor-barbecue": 1990,
  "amendoim-sabor-alho-e-ervas": 1990, "oregano": 3200, "paprica-defumada": 3800,
  "curcuma-em-po": 2900, "morango-liofilizado": 8900, "banana-liofilizada": 7200,
  "manga-liofilizada": 8400
};

function doPost(event) {
  try {
    const payload = parsePayload_(event);
    if (payload.action === "order") return jsonResponse_(saveOrder_(payload));
    return jsonResponse_(saveCustomer_(payload));
  } catch (error) {
    return jsonResponse_({ ok: false, error: error.message });
  }
}

function parsePayload_(event) {
  if (!event || !event.postData || !event.postData.contents) throw new Error("Requisicao vazia.");
  const data = JSON.parse(event.postData.contents);
  data.nome = clean_(data.nome, 120);
  data.telefone = clean_(data.telefone, 30);
  data.email = clean_(data.email, 160).toLowerCase();
  if (data.nome.length < 2) throw new Error("Nome invalido.");
  if (!/^\+?[0-9 ()-]{8,}$/.test(data.telefone)) throw new Error("Telefone invalido.");
  if (data.email && !/^\S+@\S+\.\S+$/.test(data.email)) throw new Error("E-mail invalido.");
  return data;
}

function spreadsheet_() {
  if (SPREADSHEET_ID === "COLOQUE_AQUI_O_ID_DA_GOOGLE_SHEET") throw new Error("Configure o ID da Google Sheet.");
  return SpreadsheetApp.openById(SPREADSHEET_ID);
}

function sheet_(name, headers) {
  const sheet = spreadsheet_().getSheetByName(name) || spreadsheet_().insertSheet(name);
  if (sheet.getLastRow() === 0) sheet.appendRow(headers);
  return sheet;
}

function saveCustomer_(data) {
  const sheet = sheet_(CLIENTS_SHEET, ["ID", "Nome", "Telefone", "E-mail", "Data/Hora"]);
  const rows = sheet.getDataRange().getValues();
  const normalizedPhone = data.telefone.replace(/\D/g, "");
  const duplicate = rows.slice(1).find(row => String(row[2]).replace(/\D/g, "") === normalizedPhone);
  if (duplicate) return { ok: true, duplicate: true, id: duplicate[0], message: "Bem-vindo de volta ao programa de pontos!" };
  const id = Utilities.getUuid();
  sheet.appendRow([id, data.nome, data.telefone, data.email, new Date()]);
  return { ok: true, id: id, message: "Seja bem-vindo(a) ao programa de pontos da Puro a Granel!" };
}

function saveOrder_(data) {
  if (!Array.isArray(data.itens) || !data.itens.length || !data.recebimento || !data.pagamento) throw new Error("Dados do pedido incompletos.");
  if (["Retirada na loja", "Entrega"].indexOf(data.recebimento) === -1) throw new Error("Forma de recebimento invalida.");
  if (["Pix", "Cartão", "Dinheiro"].indexOf(data.pagamento) === -1) throw new Error("Forma de pagamento invalida.");
  if (data.recebimento === "Entrega" && !data.endereco) throw new Error("Endereco obrigatorio para entrega.");
  const products = data.itens.map(item => {
    const id = clean_(item.productId, 80);
    const grams = Number(item.grams);
    const quantity = Number(item.quantity);
    if (!PRODUCT_PRICES_CENTS[id] || [100, 250, 500, 1000].indexOf(grams) === -1 || !Number.isInteger(quantity) || quantity < 1 || quantity > 100) throw new Error("Item do pedido invalido.");
    return { id: id, grams: grams, quantity: quantity, unitPrice: PRODUCT_PRICES_CENTS[id] };
  });
  const total = products.reduce((sum, item) => sum + Math.round(item.unitPrice * item.grams * item.quantity / 1000), 0);
  const productText = products.map(item => item.quantity + "x " + item.id + " - " + item.grams + "g").join("; ");
  const sheet = sheet_(ORDERS_SHEET, ["ID Pedido", "Data/Hora", "Cliente", "Telefone", "E-mail", "Produtos", "Total (centavos)", "Recebimento", "Endereço", "Pagamento", "Status"]);
  const date = new Date();
  const clientOrderId = clean_(data.orderId, 40);
  const orderId = /^PG-[0-9]{14}-[0-9]{3}$/.test(clientOrderId) ? clientOrderId : "PG-" + Utilities.formatDate(date, Session.getScriptTimeZone(), "yyyyMMdd-HHmmss") + "-" + Math.floor(Math.random() * 1000).toString().padStart(3, "0");
  sheet.appendRow([orderId, date, data.nome, data.telefone, data.email, productText, total, clean_(data.recebimento, 80), clean_(data.endereco, 300), clean_(data.pagamento, 40), "Novo"]);
  return { ok: true, id: orderId, total: total, status: "Novo" };
}

function clean_(value, maxLength) {
  return String(value || "").replace(/[<>]/g, "").replace(/\s+/g, " ").trim().slice(0, maxLength);
}

function jsonResponse_(body) {
  return ContentService.createTextOutput(JSON.stringify(body)).setMimeType(ContentService.MimeType.JSON);
}
