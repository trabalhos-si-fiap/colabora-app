# Security Module

O módulo **Security** centraliza os mecanismos de proteção relacionados
às credenciais dos usuários.\
Ele utiliza algoritmos modernos de derivação de chave para garantir que
senhas nunca sejam armazenadas em texto puro e sejam sempre verificadas
de forma segura.

------------------------------------------------------------------------

## PasswordManager

O `PasswordManager` é o componente responsável por gerenciar todo o
ciclo de hashing e validação de senhas.\
Ele utiliza o algoritmo **scrypt**, reconhecido por sua alta segurança e
resistência a ataques de força bruta.

### 🔐 Características

-   Utiliza **salt aleatório** para cada senha.
-   Deriva hashes usando o algoritmo **scrypt** com parâmetros fortes.
-   Realiza comparação segura com `hmac.compare_digest`.
-   Garante que senhas nunca sejam expostas em operações diretas.

### 🧩 Parâmetros do Scrypt

Os fatores de custo utilizados são:

-   `n = 16384`
-   `r = 8`
-   `p = 1`
-   `dklen = 64` (tamanho do hash final)

Esses valores equilibram segurança com desempenho, tornando o processo
resistente a hardware especializado (como GPUs e ASICs).

------------------------------------------------------------------------

## Métodos

### `hash_password(password: str) -> (hash: bytes, salt: bytes)`

Gera o hash seguro da senha do usuário.\
Retorna uma tupla contendo:

-   **hash_password** --- hash derivado pelo scrypt\
-   **salt** --- salt aleatório utilizado no processo

O salt é essencial para impedir ataques de rainbow table e garantir que
senhas iguais resultem em hashes diferentes.

------------------------------------------------------------------------

### `check_password(password: str, user: User) -> bool`

Verifica se uma senha fornecida corresponde ao hash salvo do usuário.

Processo:

1.  Recupera o `salt` armazenado no usuário.
2.  Gera um novo hash com base na senha digitada.
3.  Compara os hashes usando `hmac.compare_digest`, prevenindo *timing
    attacks*.

Retorna:

-   `True` se a senha for válida\
-   `False` caso contrário

------------------------------------------------------------------------

## Benefícios de Segurança

-   Senhas nunca são armazenadas ou manipuladas em texto claro.
-   O uso de **salt por usuário** elimina repetição e previsibilidade.
-   O uso de **compare_digest** evita ataques baseados em tempo de
    resposta.
-   O scrypt dificulta o uso de força bruta acelerada por hardware.

------------------------------------------------------------------------

## Exemplo de Uso

``` python
pm = PasswordManager()

# Criando uma senha segura
hash, salt = pm.hash_password("minha_senha_secreta")

# Validando durante login
pm.check_password("minha_senha_secreta", user)
```

------------------------------------------------------------------------

## Conclusão

O módulo **Security** fornece uma camada essencial de proteção ao
sistema,\
garantindo que senhas sejam tratadas de forma correta,
criptograficamente segura e resistente a ataques modernos.
