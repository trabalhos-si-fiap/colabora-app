# Login CLI – Tela Inicial (ColaboraApp)

A **tela de Login** é o ponto de entrada da aplicação TUI do Colabora, construída com o framework **Textual**.  
Ela permite que o usuário:

- Faça login na plataforma
- Acesse a tela de registro
- Visualize projetos sem estar logado

---

## Visão Geral

Aplicativo principal:

```python
class ColaboraApp(App):
    """Um aplicativo TUI para o Colabora."""
```

Configurações principais:

- **TITLE**: `Colabora APP`
- **CSS_PATH**: `src/tui/css/styles.css`
- **Atalhos (Bindings)**:
  - `t` → `change_theme()` – muda o tema da interface
  - `q` → `quit()` – sai da aplicação

Telas registradas:

- `register` → `RegisterScreen`

---

## Layout da Tela de Login

A tela é composta por:

- **Header** com relógio (`Header(show_clock=True)`)
- Container central com:
  - Título em Markdown: `# 📒 Bem vido ao app Colabora! ✏️`
  - Subtítulo: `Conectando talentos a projetos de impacto social.`
  - Mensagem de orientação (`login-output`): `Entre em sua conta ou registre-se.`
- Campos de entrada:
  - **E-mail** (`email-input`)
  - **Senha** (`password-input`, modo oculto)
- Botões principais:
  - **Entrar** (`login-button`)
  - **Registrar** (`register-button`)
  - **Ver Projetos** (`view-projects-button`)
- Dicas de zoom:
  - `Ctrl + "+"` aumenta o zoom da interface.
  - `Ctrl + "-"` diminui o zoom da interface.
- **Footer** com status/atalhos (`Footer()`)

> Observação: no código atual, e-mail e senha possuem valores padrão de exemplo (`elias@gmail.com` e `1234567A*`), úteis para desenvolvimento.

---

## Funcionalidades

### 1. Login (`Entrar`)

Ao pressionar o botão **Entrar**:

1. Os valores dos campos:
   - `#email-input`
   - `#password-input`
   são lidos.

2. O **LoginUseCase** é executado:

   ```python
   user, err_msg = self.login_use_case.execute(email, password)
   ```

3. Se o login for bem-sucedido (`user` != `None`):
   - A aplicação navega para a tela de usuário:

     ```python
     self.push_screen(
         UserScreen(
             user=user,
             user_repository=self.user_repository,
             hability_repository=self.hability_repository,
             update_user_use_case=self.update_user_use_case,
             replace_password_use_case=self.replace_password_use_case,
         )
     )
     ```

4. Se o login falhar:
   - Uma notificação de erro é exibida:

     ```python
     self.notify(
         '⚠️  ' + err_msg,
         title='Erro ao fazer login',
         severity='error'
     )
     ```

---

### 2. Registro (`Registrar`)

Ao pressionar o botão **Registrar**:

- A aplicação navega para a tela de registro já registrada nas `SCREENS`:

  ```python
  self.push_screen("register")
  ```

Essa tela é representada por `RegisterScreen` e é responsável pela criação de novos usuários.

---

### 3. Visualizar Projetos (`Ver Projetos`)

Ao pressionar o botão **Ver Projetos**:

- A aplicação navega para a `ProjectScreen`, permitindo visualizar projetos mesmo sem estar logado:

  ```python
  self.push_screen(
      ProjectScreen(
          user=None,
          user_repository=self.user_repository,
          project_repository=self.project_repository,
      )
  )
  ```

> Nesse cenário, o usuário é considerado **anônimo** (`user=None`), e algumas ações podem estar restritas dependendo da implementação da `ProjectScreen`.

---

## Casos de Uso Internos

A tela de login utiliza os seguintes *use cases*:

- `LoginUseCase` – autenticação de usuário.
- `UpdateUserUseCase` – atualização de dados do usuário (utilizado na `UserScreen`).
- `ReplacePasswordUseCase` – troca de senha (também usado na `UserScreen`).

Esses casos de uso são gerenciados pela camada de domínio e injetados na interface TUI, mantendo a separação entre lógica de negócio e apresentação.

---

## Resumo

A **tela de Login do ColaboraApp** é a porta de entrada do usuário na experiência TUI:

- Centraliza autenticação
- Fornece acesso rápido ao registro
- Permite explorar projetos sem login
- Integra diretamente com os principais *use cases* da aplicação

Ela fornece uma UX simples, guiada por mensagens claras e atalhos úteis para navegação e visualização.
