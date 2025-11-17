# Colabora APP

✨ O aplicativo que conecta talentos a projetos de impacto social. ✨

Colabora é uma aplicação de interface de texto (TUI) construída com [Textual](https://textual.textualize.io/) que permite a voluntários encontrar projetos e a ONGs encontrarem as habilidades de que precisam.

<p align="center">
  <img src="docs/assets/p1.png" alt="Screenshot da tela inicial" width="49%">
  <img src="docs/assets/p2.png" alt="Screenshot da tela cadastro de novo usuario" width="49%">
</p>


<p align="center">
  <img src="docs/assets/p3.png" alt="Screenshot da tela inicial" width="50%">
</p>


## 🚀 Começando

Siga estas instruções para obter uma cópia do projeto em sua máquina local para desenvolvimento e testes.

### Pré-requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

-   **Python 3.11+**
-   **Poetry**: Uma ferramenta para gerenciamento de dependências e pacotes em Python. Você pode instalá-lo seguindo as [instruções oficiais](https://python-poetry.org/docs/#installation).

### Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/trabalhos-si-fiap/colabora-app
    cd colabora-app
    ```

2.  **Instale as dependências:**

    Use o Poetry para criar um ambiente virtual e instalar todas as dependências do projeto listadas no arquivo `pyproject.toml`.

    ```bash
    poetry install
    ```

## 🏃‍♀️ Executando a Aplicação

Este projeto usa Taskipy para gerenciar e executar tarefas de desenvolvimento. Os comandos são executados através do Poetry.

Para iniciar a aplicação TUI, execute o seguinte comando:

```bash
poetry run task start
```

Isso iniciará a tela de login, onde você pode entrar com uma conta existente ou se registrar.

## ✅ Executando os Testes

Para garantir a qualidade e a estabilidade do código, temos uma suíte de testes. Para executá-la, use o comando:

```bash
poetry run task test
```

Para verificar a cobertura dos testes, execute:

```bash
poetry run task coverage
```

## 🎨 Estilo de Código e Linting

Mantemos um padrão de código consistente usando `black` para formatação, `isort` para ordenação de imports e `flake8` para linting.

Para formatar e verificar seu código automaticamente, execute:

```bash
poetry run task lint
```

## 🤝 Como Contribuir

Estamos abertos a contribuições! Se você deseja colaborar, siga estes passos:

1.  **Faça um Fork** do projeto.
2.  **Crie uma branch** para sua nova feature (`git checkout -b feature/nova-feature`).
3.  **Faça o commit** de suas alterações (`git commit -m 'Adiciona nova feature'`).
4.  **Faça o push** para a branch (`git push origin feature/nova-feature`).
5.  **Abra um Pull Request**.

Agradecemos por sua ajuda para tornar o Colabora ainda melhor!
