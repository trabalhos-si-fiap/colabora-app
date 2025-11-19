# User CLI – Tela de Perfil (UserScreen)

A **UserScreen** é a tela de perfil do usuário na aplicação TUI.  
Ela permite que o usuário:

- Veja e edite suas informações básicas
- Atualize sua senha
- Gerencie suas habilidades
- Navegue para a tela de projetos
- Acesse o painel administrativo (se for admin)
- Fazer logout

---

## Visão Geral

Definição principal:

```python
class UserScreen(Screen):
    """Tela de perfil do usuário."""
```

Atalhos de teclado:

- `l` → Ação de **logout** (`action_logout`)
- `Esc` → Herdado da navegação da aplicação (voltar tela, quando aplicável)

Na inicialização, a tela:

1. Recarrega o usuário do banco com todas as relações usando:
   ```python
   user_repository.get_by_id_with_all_relations(user.id)
   ```
2. Carrega as habilidades organizadas por domínio:
   ```python
   self.habilities_data = hability_repository.get_dict_by_domain()
   ```
3. Cria um mapa de nome da habilidade → objeto `Hability`:
   ```python
   self.hability_map = { hability.name: hability, ... }
   ```

Se o usuário informado não for encontrado, a tela é fechada (`pop_screen`).

---

## Layout da Tela

A estrutura visual é composta por:

- **Header** com relógio (`Header(show_clock=True)`)
- Conteúdo principal dentro de um `VerticalScroll` com classes `bg with-border`
- **Footer** (`Footer()`)

### Cabeçalho do Perfil

- Saudação personalizada:
  - `Olá, <primeiro_nome>!` ou, se não houver nome, o e-mail:
    ```python
    f"[b] Olá, {self.user.first_name or self.user.email}! [/]"
    ```
- Texto auxiliar: `Edite suas informações:`

---

## Edição de Informações Básicas

Os campos são exibidos em linhas horizontais:

### Nome e Sobrenome

- Rótulos:
  - **Nome**
  - **Sobrenome**
- Campos:
  - `#first-name` – Primeiro nome (`Input`)
  - `#last-name` – Sobrenome (`Input`)

### Data de Nascimento e E-mail

- Rótulos:
  - **Data de Nascimento**
  - **E-mail**
- Campos:
  - `#birth-date` – Data de nascimento (`AAAA-MM-DD`)
  - Campo de e-mail (somente leitura)

---

## Resumo de Projetos e Habilidades

Uma seção mostra contadores:

- **Projetos** (`#projects-count`) – número de projetos em que o usuário está inscrito.
- **Habilidades** (`#habilities-count`) – número de habilidades associadas ao usuário.

Ambos são exibidos com o widget `Digits`.

Esses contadores são atualizados após salvar alterações de perfil.

---

## Troca de Senha

Seção exibida em um `Collapsible` com título **Trocar senha**:

Elementos:

- Label de saída de status (`#output-pw`)
- Campo: **Digite a nova senha** (`#new-password`, `password=True`)
- Campo: **Repita a nova senha** (`#new-password-confirmation`, `password=True`)
- Botão **Salvar** (`#save-password-button`)

### Fluxo de Troca de Senha

1. Usuário preenche os dois campos de senha.
2. Ao clicar em **Salvar**:
   - Se as senhas forem diferentes:
     - Mensagem: `As senhas não conferem!`
   - Se forem iguais:
     - Chama o caso de uso:
       ```python
       _, err = self._replace_password_uc.execute(
           id=self.user.id,
           new_password=new_password
       )
       ```
     - Se houver erro:
       - Mensagem exibida em `#output-pw`
     - Se não houver erro:
       - Mensagem: `Senha alterada com sucesso!`

---

## Gerenciamento de Habilidades

A seção de habilidades:

- Label: `Selecione suas habilidades:`
- Lista organizada por domínio, usando `Collapsible` para cada domínio.
- Dentro de cada domínio:
  - Cada habilidade é uma linha com:
    - `Switch` (on/off) indicando se o usuário possui a habilidade.
    - Nome da habilidade (`Static`).

O valor inicial de cada switch é baseado em:

```python
self.user.has_hability(hability)
```

### Comportamento dos Switches

O método `on_switch_changed` é disparado sempre que um switch muda de estado:

- Encontra a habilidade pelo `name` do switch usando `self.hability_map`.
- Se o switch for ativado:
  - Chama `self.user.add_hability(hability)`
- Se for desativado:
  - Chama `self.user.remove_hability(hability)`

> Observação: a persistência final das habilidades ocorre quando o usuário clica em **Salvar Alterações**.

---

## Botões de Ação

Na parte inferior da tela há um grupo de botões:

- **Salvar Alterações** (`#save-button`, variante `primary`)
- **Ver Projetos** (`#projects-button`)
- **Painel Admin** (`#admin-button`, apenas se o usuário for `Role.ADMIN`)
- **Logout** (`#logout-button`)

### Salvar Alterações

Ao clicar em **Salvar Alterações**:

1. Executa o caso de uso `UpdateUserUseCase`:
   ```python
   updated_user = self._update_user_uc.execute(
       id=self.user.id,
       first_name=...,
       last_name=...,
       birth_date=...,
       habilities=self.user.habilities,
   )
   ```
2. Se o retorno for um usuário válido, o objeto `self.user` é atualizado.
3. Os contadores de projetos e habilidades são atualizados:
   - `#projects-count`
   - `#habilities-count`
4. Uma notificação de sucesso é exibida:
   - `✅ alterações salvas com sucesso!`

---

### Ver Projetos

Ao clicar em **Ver Projetos**:

- A tela navega para a `ProjectScreen`, passando:
  - `user=self.user`
  - Um novo `UserRepository`
  - Um novo `ProjectRepository`

Isso permite ao usuário gerenciar inscrições em projetos a partir de sua conta.

---

### Painel Admin (somente Admin)

Se o usuário possuir `role == Role.ADMIN`:

- Um botão adicional aparece: **Painel Admin**.

Ao clicar:

- É aberta a `AdminScreen`, que permite gerenciar:

  - Organizações
  - Projetos
  - Usuários

---

### Logout

Há duas formas de fazer logout:

1. Clicando no botão **Logout** (`#logout-button`).
2. Usando o atalho `l`.

Ambos disparam:

```python
self.app.pop_screen()
```

Encerrando a tela de perfil e voltando à tela anterior (geralmente o Login).

---

## Casos de Uso Utilizados

A `UserScreen` depende diretamente dos seguintes *use cases*:

- `UpdateUserUseCase` – Atualização dos dados do usuário (nome, sobrenome, data de nascimento, habilidades).
- `ReplacePasswordUseCase` – Troca de senha com validação completa.
- Repositórios:
  - `UserRepository` – Carrega e salva o usuário.
  - `HabilityRepository` – Fornece o dicionário de habilidades por domínio.
  - `ProjectRepository` – Utilizado pela tela de projetos associada.

---

## Resumo

A **UserScreen** é o centro de gerenciamento do perfil do usuário na TUI:

- Permite editar informações pessoais.
- Dá controle total sobre habilidades associadas ao usuário.
- Oferece fluxo seguro para troca de senha.
- Integra navegação com:
  - Tela de projetos
  - Painel administrativo (para admins)
- Fornece feedback consistente via notificações e atualizações visuais (contadores, labels, etc.).

Ela representa a ponte entre a experiência de perfil e o restante do ecossistema Colabora dentro do terminal.
