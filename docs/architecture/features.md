# Features
Este módulo concentra as principais funcionalidades de autenticação, gerenciamento de usuários e operações relacionadas ao domínio da aplicação.  
Cada feature é implementada como um **Use Case** isolado, seguindo os princípios de clean architecture e mantendo regras de negócio desacopladas de infraestrutura.

As seções abaixo descrevem o comportamento, fluxo e responsabilidades de cada caso de uso.

## Register Use Case (Service)

O **RegisterUserUseCase** é responsável por realizar o processo de criação de novos usuários na aplicação.  
Ele valida as informações fornecidas, verifica duplicidade, aplica regras de senha, gera a hash e salva o novo usuário no repositório.

### 🔍 Objetivo
Garantir que apenas usuários válidos, com dados corretos e únicos, sejam cadastrados no sistema.

### 🧩 Componentes Envolvidos
- **UserRepository** — valida existência e persiste o novo usuário.
- **PasswordManager** — gera a hash e o salt da senha.
- **email_validator** — função de validação do formato do e-mail.
- **password_validator** — função responsável por validar regras de senha.
- **User** — modelo de domínio criado após o cadastro.

### 🔐 Fluxo Lógico
1. Recebe **e-mail** e **senha**.
2. Verifica se o e-mail já está cadastrado.
   - Se sim → retorna `ValueError("Usuário já existe")`.
3. Valida o e-mail usando o `email_validator`.
   - Caso inválido → retorna `ValueError` com a mensagem apropriada.
4. Valida a senha usando o `password_validator`.
   - Caso inválida → retorna `ValueError` com a mensagem apropriada.
5. Gera hash e salt usando o **PasswordManager**.
6. Cria a entidade **User**.
7. Persiste o novo usuário no repositório.
8. Retorna:
   - `(User, None)` em caso de sucesso.
   - `(None, Exception)` em caso de erro de validação.

### 🧪 Retornos
| Cenário | Retorno |
|--------|---------|
| Cadastro válido | `(User, None)` |
| Usuário já existe | `(None, ValueError("Usuário já existe"))` |
| E-mail inválido | `(None, ValueError(msg))` |
| Senha inválida | `(None, ValueError(msg))` |

### 🏭 Factory
O método `factory()` instancia o use case com todas as dependências padrão:
- `UserRepository`
- `PasswordManager`
- `email_validator`
- `password_validator`

Isso facilita o uso em serviços ou controladores sem necessidade de construir manualmente todas as dependências.

## Login Use Case (Service)

O **LoginUseCase** é responsável por autenticar usuários a partir de suas credenciais.  
Ele valida o e-mail informado, verifica a existência do usuário e utiliza o mecanismo de segurança para confirmar a senha.

### 🔍 Objetivo
Garantir que apenas usuários com credenciais válidas possam acessar a aplicação.

### 🧩 Componentes Envolvidos
- **UserRepository** — consulta o usuário pelo e-mail.
- **PasswordManager** — realiza a verificação da senha utilizando a hash armazenada.
- **User** — modelo de domínio retornado em caso de autenticação bem-sucedida.

### 🔐 Fluxo Lógico
1. Recebe **e-mail** e **senha**.
2. Busca o usuário pelo e-mail no repositório.
3. Se o usuário não existir → retorna erro de credenciais inválidas.
4. Se existir, valida a senha utilizando o PasswordManager.
5. Retorna:
   - `(User, None)` se a autenticação for bem-sucedida.
   - `(None, "Credenciais inválidas.")` em caso de falha.

### 🧪 Retornos
| Cenário | Retorno |
|--------|---------|
| Usuário encontrado e senha válida | `(User, None)` |
| Usuário não encontrado | `(None, "Credenciais inválidas.")` |
| Senha incorreta | `(None, "Credenciais inválidas.")` |

### 🏭 Factory
O método `factory()` permite instanciar o use case com suas dependências padrão (`UserRepository` e `PasswordManager`), facilitando a criação em camadas superiores.

## Change Password Use Case (Service)

O **ReplacePasswordUseCase** é responsável por atualizar a senha de um usuário já existente.  
Ele verifica a existência do usuário, valida a nova senha e aplica o processo completo de geração de hash + salt antes de salvar a alteração.

### 🔍 Objetivo
Permitir que usuários atualizem sua senha de forma segura, garantindo validação e proteção dos dados.

### 🧩 Componentes Envolvidos
- **UserRepository** — acessa e persiste o usuário no banco.
- **PasswordManager** — gera a nova hash e salt da senha.
- **password_validator** — valida regras de segurança da nova senha.

### 🔐 Fluxo Lógico
1. Recebe o **ID do usuário** e a **nova senha**.
2. Verifica se o usuário existe:
   - Se não existir → retorna erro `"Usuário não encontrado."`.
3. Recupera o usuário com o método `get_by_id_with_habilities`.
4. Valida a nova senha com o `password_validator`.
   - Se inválida → retorna mensagem de erro.
5. Gera nova hash e salt usando o **PasswordManager**.
6. Atualiza os campos `password` e `salt` do usuário.
7. Salva as alterações no repositório.
8. Retorna:
   - `(True, None)` em caso de sucesso.
   - `(False, str)` em caso de erro.

### 🧪 Retornos
| Cenário | Retorno |
|--------|---------|
| Usuário encontrado e senha atualizada | `(True, None)` |
| Usuário não encontrado | `(False, "Usuário não encontrado.")` |
| Nova senha inválida | `(False, err)` |

### 🏭 Factory
O método `factory()` retorna uma instância pronta do use case com suas dependências padrão:
- `UserRepository`
- `PasswordManager`
- `password_validator`

Isso facilita o uso em controladores/serviços sem necessidade de injeção manual das dependências.

## Update User Use Case (Service)

O **UpdateUserUseCase** é responsável por atualizar informações de um usuário existente.  
Ele valida a existência do usuário, aplica as alterações recebidas dinamicamente e persiste os novos dados no repositório.

### 🔍 Objetivo
Permitir a atualização parcial ou completa de atributos do usuário de forma flexível e segura.

### 🧩 Componentes Envolvidos
- **UserRepository** — consulta e persiste informações do usuário.
- **User** — entidade que recebe os novos valores por meio do método `update()`.

### 🔐 Fluxo Lógico
1. Recebe o **ID do usuário** e um conjunto de campos dinâmicos (**kwargs**) contendo os dados a serem atualizados.
2. Valida se o ID foi fornecido.
3. Verifica se o usuário existe no repositório.
   - Caso não exista → retorna `None`.
4. Carrega o usuário incluindo todas as suas relações através de `get_by_id_with_all_relations`.
5. Aplica as alterações utilizando `user.update(**kwargs)`.
6. Salva as modificações no repositório.
7. Retorna:
   - O objeto **User** atualizado em caso de sucesso.
   - `None` se o usuário não existir ou se o ID for inválido.

### 🧪 Retornos
| Cenário | Retorno |
|--------|---------|
| Atualização bem-sucedida | `User` atualizado |
| ID não informado | `None` |
| Usuário não encontrado | `None` |

### 🏭 Factory
O método `factory()` cria uma instância do use case com o repositório padrão (`UserRepository`).  
Isso simplifica sua utilização em controladores e serviços superiores.

