# Register CLI – Tela de Registro (RegisterScreen)

A **RegisterScreen** é a tela TUI responsável por registrar novos usuários na aplicação Colabora.  
Ela oferece um fluxo simples e guiado para criação de conta diretamente no terminal.

---

## Visão Geral

Definição principal:

```python
class RegisterScreen(Screen):
    """Tela de registro de usuário."""
```

Objetivo:

- Permitir que um novo usuário informe e-mail e senha
- Validar a confirmação de senha
- Delegar a criação do usuário ao `RegisterUserUseCase`
- Exibir mensagens claras de sucesso ou erro

---

## Layout da Tela

Ao entrar na tela de registro, o usuário visualiza:

- **Header** com relógio (`Header(show_clock=True)`)
- Container central com bordas (`bg with-border center`) contendo:
  - Título em Markdown: `# 📝 Tela de registro 📝`
  - Subtítulo: `Crie sua conta`
  - Campos de entrada:
    - `Seu e-mail` (`id="email-input-register"`)
    - `Sua senha` (`id="password-input-register"`, modo oculto)
    - `Confirme a senha` (`id="password-input-register-confirmation"`, modo oculto)
  - Botões:
    - **Registrar** (`id="register-button-screen"`, variante `primary`)
    - **Voltar** (`id="back-button"`)
- **Footer** (`Footer()`)

---

## Fluxo de Registro

### 1. Preenchimento dos Campos

O usuário deve:

1. Informar um **e-mail válido** no campo:
   - `#email-input-register`
2. Digitar a **senha desejada** no campo:
   - `#password-input-register`
3. Confirmar a mesma senha em:
   - `#password-input-register-confirmation`

---

### 2. Validação de Senha

Ao clicar no botão **Registrar**:

1. A tela lê os valores dos três campos (`e-mail`, `senha` e `confirmação`).
2. A primeira validação verifica:

   ```python
   if password != confirm_password:
       self.notify('⚠️  As senhas não coincidem.', title='Falha ao cadastrar', severity='error')
       return
   ```

   - Em caso de senhas diferentes, o fluxo é interrompido e uma notificação de erro é exibida.

---

### 3. Execução do Caso de Uso

Se as senhas coincidirem:

1. A tela chama o `RegisterUserUseCase` via o método de fábrica:

   ```python
   user, err = RegisterUserUseCase.factory().execute(email, password)
   ```

2. O caso de uso é responsável por:
   - Verificar se o usuário já existe
   - Validar formato de e-mail
   - Validar regras de senha
   - Persistir o novo usuário

---

### 4. Tratamento de Erros

Se o `RegisterUserUseCase` retornar um erro (`err` não é `None`):

- A tela exibe uma notificação de falha:

```python
self.notify(
    '⚠️  ' + str(err),
    title='Falha ao cadastrar',
    severity='error'
)
```

Possíveis mensagens incluem:

- Usuário já existe
- E-mail inválido
- Senha inválida

---

### 5. Registro Bem-sucedido

Se não houver erro:

- A tela exibe:

```python
self.notify(
    'Você foi registrado! Agora, faça login.',
    title='🎉  Registro bem-sucedido  🥳',
    severity='information',
)
```

- Em seguida, volta para a tela anterior:

```python
self.app.pop_screen()
```

O fluxo natural após o registro é retornar à tela de **Login**, para que o usuário possa entrar com suas novas credenciais.

---

## Botão Voltar

O botão **Voltar** (`#back-button`) simplesmente fecha a tela atual:

```python
self.app.pop_screen()
```

Isso permite ao usuário abandonar o fluxo de registro e retornar ao contexto anterior (geralmente a tela de Login).

---

## Resumo

A **RegisterScreen**:

- Fornece um fluxo simples e seguro para criar novas contas.
- Valida senhas localmente antes de acionar regras de negócio.
- Centraliza o uso do `RegisterUserUseCase`.
- Fornece feedback imediato através de notificações claras (sucesso/erro).
- Integra-se naturalmente com o fluxo de Login, retornando à tela anterior após o registro bem-sucedido.
