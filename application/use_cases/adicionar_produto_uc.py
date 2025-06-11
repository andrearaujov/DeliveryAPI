
import uuid
from decimal import Decimal

from domain.entities.produto import Produto
from application.interfaces.i_produto_repository import IProdutoRepository
from application.interfaces.i_restaurante_repository import IRestauranteRepository
from application.interfaces.i_categoria_produto_repository import ICategoriaProdutoRepository
from application.dtos.adicionar_produto_request_dto import AdicionarProdutoRequestDTO
from application.dtos.produto_response_dto import ProdutoResponseDTO

class AdicionarProdutoUseCase:
    def __init__(self,
                 produto_repository: IProdutoRepository,
                 restaurante_repository: IRestauranteRepository,
                 categoria_produto_repository: ICategoriaProdutoRepository):
        self.produto_repository = produto_repository
        self.restaurante_repository = restaurante_repository
        self.categoria_produto_repository = categoria_produto_repository

    async def executar(self, request_dto: AdicionarProdutoRequestDTO) -> ProdutoResponseDTO:
        # 1. Validar se o restaurante existe
        restaurante = await self.restaurante_repository.buscar_por_id(request_dto.restaurante_id)
        if not restaurante:
            # Lançar uma exceção específica da camada de aplicação ou domínio
            raise ValueError(f"Restaurante com ID {request_dto.restaurante_id} não encontrado.")
            # idealmente: raise RestauranteNaoEncontradoError(request_dto.restaurante_id)

        # 2. Validar se a categoria do produto existe (se fornecida) e pertence ao restaurante
        if request_dto.categoria_produto_id:
            categoria = await self.categoria_produto_repository.buscar_por_id(request_dto.categoria_produto_id)
            if not categoria or categoria.restaurante_id!= restaurante.id:
                raise ValueError(
                    f"Categoria de produto com ID {request_dto.categoria_produto_id} "
                    f"não encontrada ou não pertence ao restaurante {restaurante.id}."
                )
                # idealmente: raise CategoriaNaoEncontradaError(request_dto.categoria_produto_id)
        
        # 3. Criar a entidade Produto
        # A lógica de validação de atributos do produto (nome, preço) já está na entidade Produto.
        try:
            novo_produto = Produto(
                restaurante_id=restaurante.id, # Usar o ID do restaurante validado
                nome=request_dto.nome,
                descricao=request_dto.descricao,
                preco=request_dto.preco, # A entidade Produto validará o Decimal
                categoria_produto_id=request_dto.categoria_produto_id,
                imagem_url=request_dto.imagem_url,
                disponivel=request_dto.disponivel
            )
        except ValueError as e:
            # Capturar erros de validação da entidade e relançar ou tratar
            # Poderia ser uma exceção mais específica da camada de aplicação
            raise ValueError(f"Erro ao criar produto: {str(e)}")

        # 4. Salvar o novo produto usando o repositório
        produto_salvo = await self.produto_repository.salvar(novo_produto)

        return ProdutoResponseDTO(
            id=produto_salvo.id,
            restaurante_id=produto_salvo.restaurante_id,
            nome=produto_salvo.nome,
            descricao=produto_salvo.descricao,
            preco=produto_salvo.preco,
            categoria_produto_id=produto_salvo.categoria_produto_id,
            imagem_url=produto_salvo.imagem_url,
            disponivel=produto_salvo.disponivel,
            data_criacao=produto_salvo.data_criacao,
            data_atualizacao=produto_salvo.data_atualizacao
        )
