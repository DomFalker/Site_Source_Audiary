# Documentação do Projeto: Alterações Realizadas e Guia de Deploy na Nuvem

Este documento serve como um guia completo sobre o trabalho realizado no projeto **Site Audiário** e contém todas as instruções necessárias para colocar o seu site no ar na nuvem (funcionando 24 horas por dia, sem depender do seu computador estar ligado).

---

## 🛠️ O que foi Feito no Projeto

### 1. Restauração do Ambiente de Desenvolvimento
- Reconfiguração do ambiente local após a formatação do computador.
- Criação e ativação do ambiente virtual (`venv`) com Python 3.12.
- Instalação e atualização de todas as dependências necessárias listadas em `requirements.txt`.

### 2. Configuração do Banco de Dados Local
- Inicialização do servidor PostgreSQL local na porta `5432`.
- Criação do banco de dados `audiary` para funcionamento do sistema.
- Teste de integração bem-sucedido entre o backend FastAPI e o banco de dados.

### 3. Implementação de Autenticação Segura (Cookies HTTP-Only)
- Substituição do fluxo de autenticação básico por uma arquitetura robusta baseada em tokens JWT armazenados em **Cookies HTTP-Only**.
- Aumento da segurança contra ataques XSS e sequestro de sessão.
- Proteção das rotas de visualização (frontend) e API (backend), garantindo que apenas usuários autenticados acessem áreas restritas.

### 4. Preparação para Hospedagem em Nuvem (Cloud-Ready)
- Modificação inteligente em `db/conex.py` para suportar tanto o banco de dados local quanto o banco de dados na nuvem dinamicamente usando variáveis de ambiente (`DATABASE_URL`).
- Tratamento automático do protocolo de conexão: converte `postgres://` (padrão de serviços como Render e Heroku) para `postgresql+psycopg2://` exigido pelo SQLAlchemy.

### 5. Sincronização com o GitHub
- Todos os arquivos modificados e prontos para produção foram devidamente comitados e enviados para o repositório remoto:
  **Repositório:** `https://github.com/DomFalker/Site_Source_Audiary.git` (branch `main`).

---

## 🚀 Guia de Deploy na Nuvem (Render.com - 100% Gratuito)

Como a nuvem exige credenciais pessoais para segurança, você precisará seguir estes 3 passos simples no painel do Render para ativar seu site:

### Passo 1: Criar Conta no Render
1. Acesse o site **[Render.com](https://render.com/)** e clique em **Sign Up**.
2. Escolha fazer o login usando o **GitHub**. Isso vinculará a sua conta de desenvolvedor de forma automática e segura.

### Passo 2: Criar o Banco de Dados PostgreSQL na Nuvem
1. No painel do Render, clique no botão **New +** no canto superior direito e selecione **PostgreSQL**.
2. Preencha as configurações:
   - **Name:** `audiario-db` (ou o nome que preferir)
   - **Database:** `audiary`
   - **User:** `postgres`
   - **Region:** Escolha a mais próxima (ex: Oregon ou Ohio)
3. Role até o fim e certifique-se de que o plano selecionado é o **Free** (Gratuito).
4. Clique em **Create Database**.
5. Quando a criação terminar, a página mostrará as credenciais do banco. Localize o campo **Internal Database URL** e copie o valor correspondente (começará com `postgres://...`).

### Passo 3: Criar o Web Service para Hospedar o Site
1. No painel do Render, clique em **New +** e selecione **Web Service**.
2. Escolha a opção **Build and deploy from a Git repository**.
3. Na lista de repositórios vinculados, selecione o `DomFalker/Site_Source_Audiary`.
4. Defina as seguintes configurações do serviço:
   - **Name:** `siteaudiario` (esse nome definirá o seu link gratuito, ex: `siteaudiario.onrender.com`)
   - **Region:** Selecione a mesma região que escolheu para o banco de dados.
   - **Branch:** `main`
   - **Runtime:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Selecione o plano **Free**.
5. Role até o final da página e clique no botão **Advanced**.
6. Clique em **Add Environment Variable** e adicione a seguinte variável:
   - **Key:** `DATABASE_URL`
   - **Value:** Cole o endereço completo (**Internal Database URL**) que você copiou no *Passo 2*.
7. Clique em **Create Web Service**.

> **Pronto!** O Render começará a compilar e publicar seu site automaticamente. Em 2 a 3 minutos, seu site estará online e o link público (ex: `https://siteaudiario.onrender.com`) estará visível no topo esquerdo do painel do seu Web Service.

---

## 💻 Comandos Úteis para o Desenvolvimento Local

Caso queira fazer novos testes ou rodar o projeto localmente em seu computador:

### Como Ativar a venv (Ambiente Virtual)
Abra o PowerShell na pasta do projeto e execute:
```powershell
.\venv\Scripts\Activate.ps1
```

### Como Iniciar o Servidor Local
Com a venv ativa ou executando diretamente pelo interpretador da pasta:
```powershell
venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```
O site estará acessível localmente em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Como Desativar a venv ou Fechar o Servidor
- **Para parar o site:** Pressione `CTRL + C` no terminal onde o uvicorn está rodando.
- **Para desativar a venv:** Digite `deactivate` no terminal.
