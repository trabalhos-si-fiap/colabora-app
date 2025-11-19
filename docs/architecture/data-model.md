# Data Models
A camada de **Data Models** representa as entidades principais da aplicação.  
Cada modelo define a estrutura dos dados, seus atributos e suas relações com outras entidades do domínio.

## Hability Model

O **Hability** representa uma habilidade pertencente a um usuário ou utilizada como referência dentro do domínio da aplicação.  
Ele define propriedades essenciais para descrever uma competência e pode ser utilizado em filtros, perfis profissionais, projetos ou regras de negócio relacionadas a capacidades técnicas.

### 🔧 Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| **id** | `int \| None` | Identificador único da habilidade (opcional). |
| **name** | `str` | Nome da habilidade (ex.: "Python", "Gestão de Projetos"). |
| **description** | `str` | Descrição detalhada da habilidade. |
| **domain** | `str` | Área/domínio à qual a habilidade pertence (ex.: "backend", "design", "management"). |

### 🧠 Comportamentos
#### `to_dict()`
Retorna um dicionário contendo todos os campos da habilidade, útil para serialização e APIs.

#### `__repr__()`
Retorna uma representação amigável para debug:  
`<Hability(id=ID, name='NOME')>`

#### `__eq__(other)`
Duas habilidades são consideradas iguais quando possuem o **mesmo nome**.  
Isso permite comparação lógica e evita duplicidades sem depender do ID.

#### `__hash__()`
O hash da habilidade é baseado no seu **name**, permitindo que objetos `Hability` sejam usados em:
- `set()`
- chaves de dicionário
- coleções que exigem elementos hashable

### 🔗 Relacionamentos
Embora o modelo não contenha relações diretas no código, ele é normalmente associado a:
- **Users** (um usuário pode ter várias habilidades)
- **Projects** (opcional, dependendo da arquitetura)

### 📝 Exemplo de Instanciação
```python
h = Hability(
    name="Python",
    description="Experiência em desenvolvimento backend com Python.",
    domain="backend"
)
```
## Organization Model

O **Organization** representa uma entidade organizacional dentro da aplicação, como uma empresa, instituição, agência ou equipe.  
Ele centraliza informações institucionais e de contato, servindo como base para relacionar usuários, projetos ou outros elementos do domínio.

### 🔧 Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| **id** | `int \| None` | Identificador único da organização (opcional). |
| **name** | `str` | Nome da organização. |
| **description** | `str` | Breve resumo ou descrição da instituição. |
| **contact_email** | `str` | E-mail de contato oficial da organização. |
| **contact_phone** | `str` | Telefone de contato. |
| **website** | `str` | URL oficial do site da organização. |

### 🧠 Comportamentos
#### `to_dict()`
Retorna um dicionário com todos os campos da organização.  
Muito útil para serialização, respostas de API e persistência.

#### `__repr__()`
Retorna uma representação amigável para depuração:  
`<Organization(id=ID, name='NOME')>`

### 🔗 Relacionamentos
Embora não definidos diretamente no modelo, organizações normalmente se relacionam com:
- **Users** — usuários pertencem a uma organização.
- **Projects** — projetos podem estar vinculados a uma organização.

### 📝 Exemplo de Instanciação
```python
org = Organization(
    name="Tech Solutions",
    description="Empresa especializada em soluções de software.",
    contact_email="contato@techsolutions.com",
    contact_phone="+55 11 99999-0000",
    website="https://techsolutions.com"
)
```
## Project Model

O **Project** representa um projeto pertencente a uma organização e associado a um conjunto de habilidades necessárias.  
Ele serve como unidade de trabalho ou iniciativa dentro da aplicação, podendo agrupar usuários, competências e objetivos específicos.

### 🔧 Campos
| Campo | Tipo | Descrição |
|-------|------|-----------|
| **id** | `int \| None` | Identificador único do projeto. |
| **name** | `str` | Nome do projeto. |
| **description** | `str` | Descrição detalhada do projeto. |
| **organization** | `Organization \| None` | Instância completa da organização vinculada ao projeto (opcional). |
| **organization_id** | `int \| None` | ID da organização (usado principalmente ao carregar do banco de dados). |
| **habilities** | `list[Hability]` | Lista de habilidades necessárias ao projeto. |
| **hability_ids** | `list[int]` | IDs das habilidades, útil para carregamento via persistência. |

### 🧠 Lógica Interna Importante
- Se `organization` for fornecida, o `organization_id` é automaticamente derivado dela.
- `habilities` é sempre inicializado como uma lista (mesmo se `None` for passado).
- `hability_ids` é mantido separado para suportar ORMs ou carregamento parcial.

Isso permite que o modelo funcione tanto com instâncias completas quanto com relações parciais vindas do banco.

### 🔧 Métodos Públicos

#### `to_dict()`
Retorna um dicionário contendo todos os campos do projeto, incluindo:
- `organization_id`
- lista de habilidades (`habilities`)
- IDs das habilidades (`hability_ids`)

Útil para APIs, serialização e testes.

#### `has_hability(hability: Hability) -> bool`
Verifica se o projeto requer uma habilidade específica.  
Regras:
- Retorna `False` se a habilidade for `None` ou não possuir `id`.
- Retorna `True` se existir uma habilidade com o mesmo `id` na lista do projeto.

### 🔗 Relacionamentos
O modelo se conecta naturalmente com:
- **Organization** — um projeto pertence a uma organização.
- **Hability** — um projeto pode exigir várias habilidades.

### 📝 Exemplo de Instanciação
```python
p = Project(
    name="Sistema de Gestão",
    description="Desenvolvimento de um sistema interno para automação de processos.",
    organization=Organization(name="TechCorp", description="Empresa X", contact_email="c@x.com", contact_phone="123", website="https://x.com"),
    habilities=[
        Hability(name="Python", description="Backend", domain="backend"),
        Hability(name="React", description="Frontend", domain="frontend")
    ]
)
```
## User Model

O **User** representa a entidade central de autenticação e vínculo
dentro da aplicação.\
Ele armazena credenciais seguras, dados pessoais essenciais,
habilidades, projetos associados e o papel (role) do usuário no sistema.

Além disso, contém métodos utilitários para cálculo de idade,
gerenciamento de habilidades e inscrição em projetos.

------------------------------------------------------------------------

### 🧩 Estrutura do Modelo

  ---------------------------------------------------------------------------
  Campo                Tipo                  Descrição
  -------------------- --------------------- --------------------------------
  **id**               `int \| None`         Identificador único do usuário.

  **email**            `str`                 Endereço de e-mail do usuário.

  **password**         `str`                 Hash da senha.

  **salt**             `str`                 Salt utilizado no processo de
                                             hashing.

  **first_name**       `str \| None`         Primeiro nome do usuário.

  **last_name**        `str \| None`         Sobrenome do usuário.

  **birth_date**       `str \| None`         Data de nascimento em formato
                                             ISO (string).

  **phone**            `str \| None`         Telefone de contato.

  **role**             `"ADMIN" \| "USER"`   Nível de permissão do usuário
                                             (padrão: `USER`).

  **habilities**       `list[Hability]`      Lista de habilidades que o
                                             usuário possui.

  **projects**         `list[Project]`       Projetos nos quais o usuário
                                             está inscrito.
  ---------------------------------------------------------------------------

------------------------------------------------------------------------

### 🔐 Role Enum

O modelo define um enum interno simples:

``` python
class Role:
    ADMIN = "ADMIN"
    USER = "USER"
```

------------------------------------------------------------------------

### 🧠 Comportamentos Principais

#### `to_dict()`

Retorna um dicionário completo com todos os dados do usuário, incluindo
listas de habilidades e projetos.

#### `__str__()` / `__repr__()`

Retorna uma string amigável no formato:

    Usuário: EMAIL ROLE

#### `age() -> int | None`

Calcula a idade do usuário com base no `birth_date`.

------------------------------------------------------------------------

### 🔧 Atualização de Campos

#### `update(**kwargs)`

Atualiza atributos dinamicamente.

------------------------------------------------------------------------

### 🛠️ Gerenciamento de Habilidades

#### `add_hability(hability)`

Adiciona uma nova habilidade ao usuário.

#### `remove_hability(hability)`

Remove a habilidade caso esteja presente.

#### `has_hability(hability) -> bool`

Verifica se o usuário possui uma habilidade específica.

------------------------------------------------------------------------

### 📌 Gerenciamento de Projetos

#### `is_subscribed_to(project) -> bool`

Retorna `True` se o usuário estiver inscrito no projeto fornecido.

#### `add_project(project)`

Inscreve o usuário em um projeto.

#### `remove_project(project)`

Remove a inscrição do usuário.

------------------------------------------------------------------------

### 📝 Exemplo de Instanciação

``` python
user = User(
    email="john@example.com",
    password="hashed-password",
    salt="random-salt",
    first_name="John",
    last_name="Doe",
    birth_date="1998-05-10",
    phone="(11) 99999-0000",
    role=Role.USER,
)
```
