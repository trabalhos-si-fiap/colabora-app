# Admin CLI -- Painel Administrativo

A **AdminScreen** é a interface administrativa da aplicação em modo
texto (TUI), construída com o framework **Textual**.\
Ela permite gerenciar as principais entidades do sistema diretamente
pelo terminal:

-   Organizações
-   Projetos
-   Usuários

------------------------------------------------------------------------

## Como acessar

A tela administrativa é exibida dentro da aplicação Textual como uma
**Screen** chamada `AdminScreen`.\
Ela normalmente é acessada a partir de um fluxo autenticado ou via menu
principal.

Atalho disponível:\
- `Esc` → Voltar para a tela anterior

------------------------------------------------------------------------

## Layout Geral

A tela contém:

-   **Header** com relógio\
-   Área superior para mensagens (`admin-output`)\
-   Navegação por abas (Organizações, Projetos, Usuários)\
-   Sub-abas para cada operação de CRUD\
-   **Footer** com atalhos e status

------------------------------------------------------------------------

# Gerenciamento de Organizações

## Criar Organização

Campos:

-   Nome\
-   Descrição\
-   E-mail\
-   Telefone\
-   Website

Botão: **Salvar Nova Organização**

Fluxo:

1.  Preencher os campos\
2.  Clicar em "Salvar Nova Organização"\
3.  Listas são atualizadas e formulário é limpo

------------------------------------------------------------------------

## Listar/Editar Organização

Componentes:

-   Lista de organizações\
-   Formulário de edição (preenchido automaticamente)\
-   Botão: **Salvar Alterações**

Fluxo:

1.  Selecionar organização\
2.  Formulário é exibido com dados preenchidos\
3.  Editar e salvar

------------------------------------------------------------------------

## Deletar Organização

Componentes:

-   Lista de organizações\
-   Botão: **Deletar Selecionada**

Fluxo:

1.  Selecionar organização\
2.  Clicar para deletar\
3.  Listas são atualizadas

------------------------------------------------------------------------

# Gerenciamento de Projetos

## Criar Projeto

Campos:

-   Nome\
-   Descrição\
-   Organização\
-   Habilidades necessárias

Botão: **Salvar Novo Projeto**

Fluxo:

1.  Preencher dados\
2.  Selecionar habilidades\
3.  Salvar

------------------------------------------------------------------------

## Listar/Editar Projeto

Componentes:

-   Lista de projetos\
-   Formulário de edição (preenchido automaticamente)\
-   Botão: **Salvar Alterações**

Fluxo:

1.  Selecionar projeto\
2.  Editar nome, descrição, organização e habilidades\
3.  Salvar alterações

------------------------------------------------------------------------

## Deletar Projeto

Fluxo:

1.  Selecionar projeto\
2.  Clicar em "Deletar Selecionado"

------------------------------------------------------------------------

# Gerenciamento de Usuários

## Criar Usuário

Campos:

-   E-mail\
-   Senha\
-   Role (Admin / User)

Botão: **Salvar Novo Usuário**

------------------------------------------------------------------------

## Listar/Editar Usuário

Componentes:

-   Lista de usuários\
-   Formulário de edição\
-   Botão: **Salvar Alterações**

Regras:

-   E-mail é somente leitura\
-   Senha não é atualizada aqui

------------------------------------------------------------------------

## Deletar Usuário

Fluxo:

1.  Selecionar usuário\
2.  Deletar

Regras especiais:

-   O usuário logado não pode se deletar

------------------------------------------------------------------------

## Mensagens de Feedback

As ações escrevem mensagens como:

-   `✅ Sucesso`\
-   `⚠️ Aviso`\
-   `❌ Erro`

Visíveis em **admin-output**.

------------------------------------------------------------------------
