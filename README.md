# Encontrando gargalos de forma rápida com FastAPI
<br/>

Um código otimizado é sempre o nosso mundo ideal como desenvolvedores, porem essa nem sempre é uma tarefa fácil. Então hoje iremos desvendar e simplificar uma ferramenta de profiling altamente poderosa com Python e FastAPI.

### Porem antes de iniciarmos, o que é Profiling?
Profiling é o ato de se coletar o perfil de execução de um programa. Entender quais chamadas estão sendo feitas, a ordem e o tempo de execução. O profile pode ser usado no rastreamento de gargalos, para encontrar chamadas duplicadas ou até mesmo aquela query que acabaram duplicando no código.

<br/>
<br/>

Pense no seguinte caso: nós temos um endpoint que está demorando mais do que esperávamos, o p99 dele está girando em torno de 5 segundos e nosso cliente não tem gostado desse resultado.
Então precisamos avaliar e descobrir o que está acontecendo, onde está nosso gargalo. E não é certo ficar tentando chutar ou apontar para o código do colega de equipe. O que realmente precisamos é de um bom profile que nos ajude a identificar os ofensores e descobrir como resolve-los. 
Hoje apresento a vocês o PyInstrument, uma ferramenta extremamente poderosa de Profile que funciona nativamente com código Python assíncrono e de uma forma bem intuitiva.

<br/>
<br/>

### Case:

Eu propus a seguinte situação: Temos um endpoint onde você diz alguns ativos da bolsa de valores e o número de transações que ele deve registrar no banco. Então para cada registro eu escolho um ativo aleatoriamente e um valor entre 1.0 e 100.0 .

Nosso payload:

```json
{
    "ativos": ["PETR4", "BRFS3", "AMBV3", "ITAU4", "CMIN3", "VALE3", "SUZB3", "RAIL3", "B3SA3"],
    "quantidadeAtivos": 50000
}
```
<br/>

Essa requisição está levando em média algo em torno de 6 segundos e nosso gerente pediu que investigássemos para tentar reduzir esse tempo.
Com o PyInstrument podemos criar e aplicar um middleware em nosso código python que irá com poucas linhas de código preparar nosso profile para ser executado.

</br>

```python
from typing import Callable

from fastapi import Request
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.config import settings


class ProfileMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if not settings.PROFILE or not request.query_params.get("profile", False):
            return await call_next(request)

        profile_tipo_renderizacao = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }

        profile_tipo = request.query_params.get("profile_format", "html")
        with Profiler(interval=0.001) as profiler:
            response = await call_next(request)

        tipo_extensao = {"html": "html", "speedscope": "speedscope.json"}
        extension = tipo_extensao[profile_tipo]
        render = profile_tipo_renderizacao[profile_tipo]()
        with open(f"profile.{extension}", "w") as out:
            out.write(profiler.output(renderer=render))
        return response
```

<br/>

Com nosso middleware devidamente registrado em nosso serviço, basta agora fazermos uma requisição passando um Query Params informando que gostariamos de obter um profile.

```json
/api/v1/transaction?profile=true
```

Feito isso teremos um arquivo na raiz do projeto chamado "profile.html" e ele nos ajudará a mapear e atuar diretamente nos nossos gargalos. 

<img src="https://media.licdn.com/dms/image/D4D12AQFovgLbE1yFDg/article-inline_image-shrink_1500_2232/0/1717718510575?e=1723075200&v=beta&t=zsi6uc_0JuPWgd4oLZFePvJUG9hcO3ycdORTi-UIYk0" alt="Imagem mostrando tempo que cade função levou">

<img src="https://media.licdn.com/dms/image/D4D12AQHRq0NLkpIT2A/article-inline_image-shrink_1500_2232/0/1717718536768?e=1723075200&v=beta&t=eFrH1FSd7PQ8MgfMqzzqh-sXCikbZZOrAE_FRPTZqsM" alt="Imagem mostrando a porcentagem da função em relação ao tempo" >

<br/>
<br/>
<br/>

Bom, com esses dados ficou claro de que um dos nossos grandes ofensores sem dúvidas é o nosso Repositório e agora podemos analisar mais profundamente e propor um plano para solucionar esse gargalo.
Intencionalmente nesse código eu estou tentando dar um "save_all" em cerca de 50.000 transações e o nosso banco está tendo dificuldades de lidar com isso.
Uma proposta de solução poderia por exemplo ser um Chunck Iterator, porem isso é assunto para outro artigo.

Espero que esse artigo possa ajuda-los pessoal, muito obrigado.


<br/>
