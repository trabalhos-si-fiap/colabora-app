# Projects CLI – Tela de Projetos (ProjectScreen)

A **ProjectScreen** é a tela da aplicação TUI responsável por listar e interagir com projetos.  
Ela permite que o usuário:

- Visualize todos os projetos disponíveis
- Veja apenas os projetos em que está inscrito
- Busque projetos por nome/descrição
- Inscreva-se ou desinscreva-se de projetos (se tiver as habilidades necessárias)

---

## Navegação e Atalhos

A tela é implementada como uma `Screen` do Textual:

```python
class ProjectScreen(Screen):
    """Tela para listar e interagir com projetos."""
```

Atalhos:

- `Esc` → Voltar para a tela anterior (`app.pop_screen`)

---

## Dependências e Estado

A tela recebe na inicialização:

- `user: Optional[User]` – Usuário atual (ou `None`, se anônimo)
- `user_repository: UserRepository` – Repositório de usuários
- `project_repository: ProjectRepository` – Repositório de projetos

Estado interno:

- `self.user_id` – ID do usuário (se houver)
- `self.all_projects` – lista de todos os projetos com habilidades, utilizada para filtragem

Ao montar a tela, ela recarrega:

- O usuário (com todas as relações) caso `user_id` exista
- A lista de projetos por meio de `find_all_with_habilities()`

---

## Layout Geral

A tela é composta por:

- **Header** com relógio (`Header(show_clock=True)`)
- Área principal com:
  - Título: **Projetos Disponíveis**
  - Textos de orientação:
    - “Explore os projetos e inscreva-se naqueles que te interessam.”
    - “Para participar, você deve ter ao menos uma habilidade solicitada.”
  - Campo de busca:
    - `Input` com placeholder: `🔎  Buscar por nome ou descrição...` (`id="search-project"`)
  - Conteúdo com abas (`TabbedContent`):
    - **Todos os Projetos** (`all-projects-tab`)
    - **Meus Projetos** (`my-projects-tab`)
- **Footer** (`Footer()`)

---

## Abas de Projetos

### Aba: Todos os Projetos

Nesta aba, a lista de projetos é exibida com rolagem em:

- `VerticalScroll` com `id="project-list-container"`

Cada projeto é renderizado como um **Collapsible**:

- Título: nome do projeto
- Descrição do projeto
- Lista de habilidades necessárias
- (Opcional) Botão de inscrição / desinscrição, se o usuário tiver pelo menos uma das habilidades requeridas

---

### Aba: Meus Projetos

Nesta aba, são exibidos apenas os projetos nos quais o usuário está inscrito:

- `VerticalScroll` com `id="my-projects-container"`

Os projetos são carregados via:

```python
project_ids = [p.id for p in self.user.projects]
user_projects = self._project_repo.find_by_ids_with_habilities(project_ids)
```

Cada projeto é exibido com a mesma estrutura de **Collapsible** usada em "Todos os Projetos".

---

## Busca de Projetos

O campo de busca (`#search-project`) permite filtrar os projetos exibidos na aba **Todos os Projetos**.

Comportamento:

1. A cada alteração de texto (`Input.Changed`), o termo de busca é convertido para minúsculas.
2. A tela percorre cada `Collapsible` existente em `#project-list-container`.
3. Para cada projeto, verifica se o termo aparece no:
   - Nome do projeto
   - Descrição do projeto
4. Se não houver correspondência, o `Collapsible` é ocultado (`display = False`); caso contrário, é exibido (`display = True`).

---

## Inscrição e Desinscrição em Projetos

A inscrição/desinscrição é acionada por botões com ID no padrão:

- `all_subscribe_btn_<id>`
- `my_subscribe_btn_<id>`

### Regras para exibir o botão

- Apenas exibido se **existe um usuário logado** (`self.user` não é `None`)
- Usuário precisa ter **ao menos uma habilidade solicitada** pelo projeto
  - Caso contrário, é exibida a mensagem:
    - `Você não tem ao menos uma habilidade solicitada.`

### Comportamento ao clicar

1. A tela identifica o `project_id` a partir do `id` do botão.
2. Carrega o projeto atualizado do repositório.
3. Recarrega o usuário com todas as relações mais recentes.
4. Verifica se o usuário já está inscrito:

   - Se **já inscrito**:
     - Remove o projeto da lista de projetos do usuário (`remove_project`)
     - Atualiza todos os botões relacionados àquele projeto para:
       - Label: `Inscrever-se`
       - Variant: `success`
     - Remove o widget da aba **Meus Projetos**
     - Mostra notificação:
       - Título: `Cancelamento realizado`
       - Mensagem: `Remoção realizada com sucesso.`

   - Se **não inscrito**:
     - Adiciona o projeto ao usuário (`add_project`)
     - Atualiza botões para:
       - Label: `Desinscrever-se`
       - Variant: `error`
     - Adiciona o projeto na aba **Meus Projetos**
     - Mostra notificação:
       - Título: `Inscrição realizada com sucesso`
       - Mensagem: `A organização entrará em contato com você.`

5. O usuário é salvo com o novo estado de inscrições:

```python
self._user_repo.save(self.user)
```

---

## Estrutura do Widget de Projeto

Cada projeto é transformado em um `Collapsible` por `_create_project_widget`:

- Descrição do projeto (`Static`)
- Título: nome do projeto
- Subtítulo de borda: `<n> habilidades necessárias`
- Lista de habilidades:
  - Mostradas com ícone:
    - `✅` se o usuário possui a habilidade
    - `❌` caso contrário
- Botão de inscrição/desinscrição (quando aplicável)
- Mensagem de aviso, caso o usuário não tenha nenhuma das habilidades solicitadas

Exemplo de lógica de habilidades:

```python
has_it = self.user.has_hability(hability) if self.user else False
icon = "✅" if has_it else "❌"
```

---

## Comportamento para Usuário Anônimo

Quando a `ProjectScreen` é inicializada com `user=None`:

- Nenhum botão de inscrição/desinscrição é exibido.
- As habilidades são mostradas, mas apenas como referência.
- A aba **Meus Projetos** ficará vazia.

Essa abordagem permite que visitantes/anônimos explorem a lista de projetos, mas não se inscrevam.

---

## Resumo

A **ProjectScreen** oferece uma experiência rica de navegação por projetos no modo texto:

- Lista todos os projetos com suas habilidades
- Separa uma aba específica para os projetos do usuário
- Possibilita filtragem por texto
- Controla a inscrição com base nas habilidades do usuário
- Mantém a interface sincronizada com o estado real do domínio (repositórios)

Ideal para cenários em que usuários buscam projetos alinhados às suas competências e desejam gerenciar rapidamente suas inscrições diretamente no terminal.
