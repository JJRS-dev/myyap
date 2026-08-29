# Puro a Granel

Loja virtual estática para venda de produtos a granel, com catálogo responsivo, imagens próprias para cada produto, filtros por categoria, detalhes nutricionais, promoções, carrinho persistente e finalização do pedido pelo WhatsApp.

## Estrutura

- `index.html`: página principal pronta para publicação no GitHub Pages.
- `purograne.html`: cópia compatível da loja para acessos antigos.
- `CadastroUnificado.gs`: endpoint do Google Apps Script para clientes e pedidos.
- `schema.sql`: modelo SQLite equivalente para uma futura API própria.

## Recursos da loja

- 369 produtos com visuais exclusivos incorporados ao próprio HTML, sem links externos de imagens.
- Filtros para cereais, leguminosas, sementes, chás, snacks, oleaginosas, temperos e liofilizados.
- Seleção de 100g, 250g, 500g ou 1kg, com cálculo automático.
- Carrinho salvo no navegador.
- Retirada ou entrega, com validação do endereço.
- Pedido formatado e enviado pelo WhatsApp.
- Cadastro no programa de pontos e registro de pedidos no Google Sheets.
- Layout responsivo e navegação por teclado.

## Google Sheets

1. Abra o projeto vinculado à planilha no Google Apps Script.
2. Use o conteúdo de `CadastroUnificado.gs`.
3. Publique como **Aplicativo da Web**, executando como o proprietário e permitindo acesso para qualquer pessoa com o link.
4. Informe a URL terminada em `/exec` em `CADASTRO_WEBHOOK_URL`, dentro dos dois arquivos HTML.

As abas `Clientes` e `Pedidos` são criadas automaticamente. O mesmo telefone não é duplicado no programa de pontos. Os totais dos pedidos são recalculados no servidor usando os preços oficiais.

## Publicação

No GitHub, abra **Settings > Pages**, selecione a branch `main` e a pasta raiz. Depois do merge, a loja será servida diretamente pelo `index.html`.

## Validação recomendada

1. Acesse a página inicial e confirme os 369 produtos.
2. Teste todos os filtros.
3. Abra um produto, altere o peso e adicione ao carrinho.
4. Atualize a página e confirme que o carrinho foi mantido.
5. Teste retirada e entrega.
6. Confirme o pedido no WhatsApp e os registros nas abas `Clientes` e `Pedidos`.

O envio ao Google Apps Script usa `mode: "no-cors"`. Por isso, a confirmação definitiva do cadastro e do pedido deve ser feita na planilha.
