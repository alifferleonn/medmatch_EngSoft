MedMatch
========

O **MedMatch** é uma plataforma inteligente desenvolvida para otimizar o processo de triagem e encaminhamento médico. Utilizando tecnologias modernas, o sistema busca conectar pacientes aos cuidados adequados de forma rápida e eficiente.

🚀 Funcionalidades
------------------

*   **Triagem Inteligente:** Processamento de sintomas com IA usando Google Gemini para análise automática.
    
*   **Encaminhamento Especializado:** Direcionamento do paciente para a especialidade médica mais adequada.
    
*   **Interface Intuitiva:** Aplicação Vue 3 moderna com suporte a TypeScript.
    
*   **Chat Interativo:** Visualização de chat para interação com pacientes.


🛠️ Tecnologias Utilizadas
--------------------------

### Backend
*   **Framework:** FastAPI (Python)
*   **IA/Processamento:** Google Gemini API
*   **CORS:** Suporte para comunicação com frontend
*   **Variáveis de Ambiente:** python-dotenv

### Frontend
*   **Framework:** Vue 3
*   **Build Tool:** Vite
*   **Linguagem:** TypeScript
*   **State Management:** Pinia
*   **Roteamento:** Vue Router
*   **HTTP Client:** Axios
*   **Node.js:** ^20.19.0 ou >=22.12.0


📁 Estrutura do Projeto
-----------------------

```
MedMatch/
├── backend/
│   └── main.py              # API FastAPI com endpoint de triagem
├── medmatch-frontend/       # Aplicação Vue 3
│   ├── src/
│   │   ├── views/
│   │   │   ├── ChatView.vue     # Visualização do chat
│   │   │   └── HomeView.vue     # Página inicial
│   │   ├── services/
│   │   │   └── api.js           # Cliente HTTP (Axios)
│   │   ├── router/
│   │   │   └── index.ts         # Configuração de rotas
│   │   ├── stores/
│   │   │   └── counter.ts       # State management com Pinia
│   │   ├── App.vue              # Componente raiz
│   │   └── main.ts              # Entrada da aplicação
│   ├── package.json
│   └── vite.config.ts
├── package.json
└── README.md


⚙️ Configuração Inicial
-----------------------

### Pré-requisitos
- Python 3.8+
- Node.js 20.19.0 ou superior
- pip (gerenciador de pacotes Python)
- npm ou yarn

### Backend Setup

1. Navegue para a pasta backend:
   ```sh
   cd backend
   ```

2. Crie um arquivo `.env` com a chave do Gemini:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

3. Instale as dependências:
   ```sh
   pip install fastapi uvicorn python-dotenv google-genai pydantic
   ```

4. Inicie o servidor:
   ```sh
   uvicorn main:app --reload
   ```
   O backend estará rodando em `http://localhost:8000`

### Frontend Setup

1. Navegue para a pasta frontend:
   ```sh
   cd medmatch-frontend
   ```

2. Instale as dependências:
   ```sh
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```sh
   npm run dev
   ```
   A aplicação estará disponível em `http://localhost:5173`

4. Para construir para produção:
   ```sh
   npm run build
   ```


🔌 API Endpoints
----------------

### POST /triagem
Realiza a triagem automática baseada em sintomas.

**Request:**
```json
{
  "texto": "Estou com dor de cabeça e febre"
}
```

**Response:**
```json
{
  "resultado": "Procure por: Clínica Geral"
}
```

**Nota:** Em casos graves, a resposta conterá "EMERGÊNCIA".


🌍 Variáveis de Ambiente
------------------------

### Backend
- `GEMINI_API_KEY`: Chave da API Google Gemini (obrigatória)

### Frontend
Configure conforme necessário em `medmatch-frontend/.env`


🚀 Como Usar
-----------

1. Inicie o backend (porta 8000)
2. Inicie o frontend (porta 5173)
3. Acesse a aplicação no navegador
4. Use a visualização de chat para inserir sintomas
5. O sistema analisará e indicará a especialidade médica apropriada


📝 Scripts Disponíveis
---------------------

### Backend
```sh
uvicorn main:app --reload    # Iniciar servidor com auto-reload
```

### Frontend
```sh
npm run dev          # Iniciar servidor de desenvolvimento
npm run build        # Build para produção
npm run preview      # Visualizar build de produção
npm run type-check   # Verificar tipos TypeScript
```
