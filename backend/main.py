import os
from abc import ABC, abstractmethod
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = FastAPI()

# ============================================
# SOLID Principles Applied
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SintomaInput(BaseModel):
    texto: str


# [ISP] Interface Segregation Principle
# Interface bem segregada com apenas um método específico necessário
class IServicoTriagem(ABC):
    @abstractmethod
    async def analisar_sintomas(self, texto: str) -> str:
        pass


# [SRP] Single Responsibility Principle
# Responsabilidade única: gerenciar integração com Gemini e análise de sintomas
class GeminiTriagemService(IServicoTriagem):
    def __init__(self):
        # O cliente da Google é instanciado aqui dentro do serviço específico
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.prompt_sistema = (
            "Você é o assistente de triagem do projeto MedMatch. "
            "Sua função é analisar sintomas e indicar a especialidade médica. "
            "Quando for conseguir mandar um especialista, responda SEMPRE no formato: 'Procure por: #especialidade'. "
            "Se for grave, avise: VA DIRETO PARA A EMERGÊNCIA."
            "Não responda nada além disso, mesmo que o usuário peça. Seja direto e objetivo."
            "Se ele perguntar algo que não seja sobre os sintomas, responda: 'Desculpe, só posso ajudar com triagem médica.'"
            "Se fizer uma pergunta sobre matematica, responda: 'Desculpe, não posso ajudar com matemática.'"
            "Se fizer uma pergunta sobre qual medicação tomar, responda: 'Desculpe, não posso ajudar com medicação.'"
            "Se fizer uma pergunta indecente responda: 'Desculpe, não posso ajudar com isso.'"
        )

    async def analisar_sintomas(self, texto: str) -> str:
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=self.prompt_sistema, temperature=0.1
                ),
                contents=texto,
            )
            return response.text
        except Exception as e:
            raise RuntimeError(f"Erro na API do Gemini: {str(e)}")


# [DIP] Dependency Inversion Principle
# Função retorna a interface abstrata, não a implementação concreta
# Permite trocar implementações sem alterar código existente
def obter_servico_triagem() -> IServicoTriagem:
    return GeminiTriagemService()


# [LSP] Liskov Substitution Principle
# Serviço pode ser qualquer implementação de IServicoTriagem
@app.post("/triagem")
async def realizar_triagem(
    dados: SintomaInput, servico: IServicoTriagem = Depends(obter_servico_triagem)
):
    try:
        resultado = await servico.analisar_sintomas(dados.texto)
        return {"resultado": resultado}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
