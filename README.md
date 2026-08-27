# Puro a Granel

Página estática da mercearia Puro a Granel, com catálogo filtrável, detalhes nutricionais, promoções, cadastro no programa de pontos, carrinho e checkout.

## Arquivos

- [purograne.html](purograne.html): interface, catálogo e lógica do carrinho.
- [CadastroUnificado.gs](CadastroUnificado.gs): endpoint Google Apps Script para clientes e pedidos.
- [schema.sql](schema.sql): modelo SQLite equivalente para uma futura API própria.

## Configuração do Google Sheets

1. Crie uma planilha no Google Sheets e copie o ID da URL.
2. Abra **Extensões > Apps Script**, cole [CadastroUnificado.gs](CadastroUnificado.gs) e preencha `SPREADSHEET_ID`.
3. Publique em **Implantar > Nova implantação > Aplicativo da Web**.
4. Execute como você e permita acesso para qualquer pessoa com o link.
5. Copie a URL `/exec` e substitua `CADASTRO_WEBHOOK_URL` em [purograne.html](purograne.html).

As abas `Clientes` e `Pedidos` são criadas automaticamente com cabeçalhos. O cadastro não duplica o mesmo telefone. Pedidos começam com status `Novo`.

O Apps Script valida os produtos, pesos e quantidades recebidos e recalcula o total com os preços oficiais antes de salvar o pedido. O número do pedido usa o formato `PG-AAAAMMDD-HHMMSS-XXX` e o status inicial é `Novo`.

## Configuração do WhatsApp

Preencha `WHATSAPP_LOJA` no JavaScript com o número internacional real da loja. O site usa `wa.me` e não inclui API paga.

## Como testar

1. Abra [purograne.html](purograne.html) no navegador.
2. Adicione produtos pela vitrine e pelo modal; teste 100g, 250g, 500g e 1kg.
3. Feche e reabra a página para confirmar a persistência do carrinho.
4. Abra o checkout, teste retirada e entrega, preencha pagamento e confira o WhatsApp.
5. Confirme cadastro em `Clientes` e pedido em `Pedidos`.

## SQL local

```bash
sqlite3 puroagranel.db < schema.sql
```

Valores monetários usam centavos (`price_per_kg_cents`, `total_cents`) para evitar erros de arredondamento. O SQL não é usado diretamente pelo HTML estático; serve como base para uma API própria.

Como o site usa `mode: "no-cors"` para enviar dados ao Google Apps Script, o navegador não consegue ler a resposta do servidor. Por isso, a confirmação definitiva deve ser feita na aba `Clientes` ou `Pedidos` do Google Sheets.

## Configurações pendentes

- [ ] ID da Google Sheet em `CadastroUnificado.gs`
- [ ] URL do Web App em `purograne.html`
- [ ] Número real do WhatsApp em `WHATSAPP_LOJA`
- [ ] Endereço, telefone e e-mail reais da loja no conteúdo do site
