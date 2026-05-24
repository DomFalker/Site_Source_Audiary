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

Como a nuvem exige credenciais pessoais para segurança, você tem duas opções para colocar seu site no ar no Render. O método Blueprint (Opção 1) é o mais recomendado, pois cria o banco de dados e o site de forma totalmente automática.

---

### ⚡ Opção 1: Deploy Automático via Render Blueprint (Recomendado - 1 Clique)

Esta opção utiliza o arquivo [render.yaml](file:///c:/Users/flavi/OneDrive/Documents/Siteaudiario%20(2)/Siteaudiario/render.yaml) incluído no projeto. O Render lerá este arquivo e criará tanto o banco de dados PostgreSQL quanto o Web Service automaticamente, já conectados.

#### Passo 1: Enviar as Alterações para o GitHub
Certifique-se de que os novos arquivos (`render.yaml`, `Dockerfile` e `.dockerignore`) foram enviados para o seu repositório Git:
```bash
git add .
git commit -m "Configure hosting with Render Blueprint and Docker"
git push origin main
```

#### Passo 2: Criar o Blueprint no Render
1. Acesse o site **[Render.com](https://render.com/)** e faça login com o **GitHub**.
2. No painel do Render, clique no botão **New +** no canto superior direito e selecione **Blueprint**.
3. Na lista de repositórios conectados, localize e selecione `Site_Source_Audiary` (ou o nome do seu repositório).
4. O Render detectará o arquivo `render.yaml` automaticamente.
5. Defina um nome para o seu Blueprint (ex: `blueprint-siteaudiario`).
6. Clique em **Apply**.

> **Pronto!** O Render criará o banco de dados e o site de forma automatizada e segura. Em 2 a 3 minutos, ambos estarão online e integrados. O link público do seu site estará disponível no painel do Web Service criado (ex: `https://siteaudiario.onrender.com`).

---

### 🛠️ Opção 2: Deploy Manual Passo a Passo

Caso prefira fazer a configuração manual de cada serviço:

#### Passo 1: Criar Conta no Render
1. Acesse **[Render.com](https://render.com/)** e clique em **Sign Up**.
2. Faça o login usando o **GitHub**.

#### Passo 2: Criar o Banco de Dados PostgreSQL na Nuvem
1. No painel do Render, clique em **New +** e selecione **PostgreSQL**.
2. Preencha as configurações:
   - **Name:** `audiario-db`
   - **Database:** `audiary`
   - **User:** `postgres`
   - **Region:** Escolha a mais próxima (ex: Oregon ou Ohio)
3. Certifique-se de que o plano selecionado é o **Free** (Gratuito).
4. Clique em **Create Database**.
5. Copie o valor de **Internal Database URL** (ex: `postgres://...`).

#### Passo 3: Criar o Web Service para Hospedar o Site
1. No painel do Render, clique em **New +** e selecione **Web Service**.
2. Escolha **Build and deploy from a Git repository**.
3. Selecione o repositório do seu site.
4. Defina as seguintes configurações:
   - **Name:** `siteaudiario`
   - **Region:** A mesma do banco de dados.
   - **Branch:** `main`
   - **Runtime:** `Python` (ou `Docker` se preferir rodar usando o [Dockerfile](file:///c:/Users/flavi/OneDrive/Documents/Siteaudiario%20(2)/Siteaudiario/Dockerfile))
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** Plano **Free**.
5. Clique em **Advanced**, depois em **Add Environment Variable**:
   - **Key:** `DATABASE_URL`
   - **Value:** Cole o endereço de **Internal Database URL** que copiou no Passo 2.
6. Clique em **Create Web Service**.

---

### 🐳 Deploy Alternativo com Docker

Se você preferir hospedar o site usando Docker em outras plataformas (como Railway, Fly.io, ou mesmo no próprio Render selecionando a runtime `Docker`):
- O projeto inclui um [Dockerfile](file:///c:/Users/flavi/OneDrive/Documents/Siteaudiario%20(2)/Siteaudiario/Dockerfile) otimizado e um [.dockerignore](file:///c:/Users/flavi/OneDrive/Documents/Siteaudiario%20(2)/Siteaudiario/.dockerignore).
- A imagem Docker é baseada em `python:3.12-slim` e inicia o site automaticamente na porta configurada pela variável `PORT` ou na `8000` por padrão.

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
