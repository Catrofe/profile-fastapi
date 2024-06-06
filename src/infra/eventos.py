import logging

from infra.repositorio.postgres_conexao import PostgresConexao


async def preparar_aplicacao() -> None:
    logging.info("Preparando a aplicação")

    try:
        logging.debug("Iniciando conexão com o MongoDB")
        await PostgresConexao().gera_conexao()

    except Exception as ex:
        logging.error("Finalizando a aplicação.")

        raise ex


async def encerrar_aplicacao() -> None:
    await PostgresConexao().fechar_conexao()
