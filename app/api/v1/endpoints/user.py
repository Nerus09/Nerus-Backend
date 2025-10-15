#CRUD users - ATUALIZADO
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import date
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_active_user

router = APIRouter()

# ==================== SCHEMAS ATUALIZADOS ====================

class UserProfile(BaseModel):
    """Schema do perfil do usuário - CAMPOS ATUALIZADOS"""
    id: int
    nome: str  # ANTES: nome_completo
    username: str  # NOVO CAMPO
    email: str
    data_nascimento: Optional[date] = None
    nivel_educacao: str
    palavras_chave: Optional[str] = None  # NOVO CAMPO
    foto_perfil: Optional[str] = None  # MANTIDO
    pontos_totais: int
    nivel_atual: int
    patente: str
    created_at: str

class UserUpdate(BaseModel):
    """Schema para atualização de perfil - CAMPOS ATUALIZADOS"""
    nome: Optional[str] = Field(None, min_length=3, max_length=255)
    username: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=50, 
        pattern="^[a-zA-Z0-9_]+$"
    )
    data_nascimento: Optional[date] = None
    nivel_educacao: Optional[str] = None
    palavras_chave: Optional[str] = None

class PasswordChange(BaseModel):
    """Schema para mudança de senha"""
    senha_atual: str
    senha_nova: str = Field(..., min_length=6)

class UserStats(BaseModel):
    """Estatísticas do usuário"""
    total_solucoes: int
    solucoes_aprovadas: int
    solucoes_pendentes: int
    solucoes_reprovadas: int
    pontos_totais: int
    nivel_atual: int
    patente: str
    media_pontuacao: Optional[float] = None
    ranking_posicao: Optional[int] = None
    certificados_obtidos: int

class HabilidadeAdd(BaseModel):
    """Adicionar habilidade ao usuário"""
    habilidade_id: int
    nivel_proficiencia: str = Field(..., pattern="^(basico|intermediario|avancado|expert)$")

class UserPublic(BaseModel):
    """Perfil público simplificado"""
    id: int
    nome: str
    username: str
    foto_perfil: Optional[str] = None
    pontos_totais: int
    nivel_atual: int
    patente: str

# ==================== LISTAR HABILIDADES DISPONÍVEIS ====================
# IMPORTANTE: Esta rota deve vir ANTES de /{user_id} para evitar conflitos

@router.get("/habilidades-disponiveis", response_model=List[dict])
def get_habilidades_disponiveis(cursor = Depends(get_db)):
    """Listar todas as habilidades disponíveis no sistema"""
    
    cursor.execute("""
        SELECT id, nome, categoria, descricao
        FROM habilidades
        ORDER BY categoria, nome
    """)
    
    return cursor.fetchall()

# ==================== PERFIL DO USUÁRIO ====================

@router.get("/me", response_model=UserProfile)
def get_my_profile(
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Obter perfil completo do usuário logado"""
    
    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        (current_user['id'],)
    )
    
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Converter datetime para string
    if user.get('created_at'):
        user['created_at'] = str(user['created_at'])
    
    return user

# ==================== ATUALIZAR PERFIL ====================

@router.put("/me", response_model=dict)
def update_my_profile(
    user_update: UserUpdate,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Atualizar perfil do usuário logado"""
    
    # Construir query dinamicamente apenas com campos fornecidos
    update_fields = []
    values = []
    
    if user_update.nome:
        update_fields.append("nome = %s")
        values.append(user_update.nome)
    
    if user_update.username:
        # Verificar se username já existe (exceto o próprio usuário)
        cursor.execute(
            "SELECT id FROM users WHERE username = %s AND id != %s",
            (user_update.username, current_user['id'])
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso por outro usuário"
            )
        update_fields.append("username = %s")
        values.append(user_update.username)
    
    if user_update.data_nascimento:
        update_fields.append("data_nascimento = %s")
        values.append(user_update.data_nascimento)
    
    if user_update.nivel_educacao:
        update_fields.append("nivel_educacao = %s")
        values.append(user_update.nivel_educacao)
    
    if user_update.palavras_chave is not None:  # Permite string vazia
        update_fields.append("palavras_chave = %s")
        values.append(user_update.palavras_chave)
    
    if not update_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar"
        )
    
    values.append(current_user['id'])
    
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, values)
    
    return {"message": "Perfil atualizado com sucesso!"}

# ==================== ESTATÍSTICAS DO USUÁRIO ====================

@router.get("/me/stats", response_model=UserStats)
def get_my_stats(
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Obter estatísticas completas do usuário"""
    
    # Estatísticas de soluções
    cursor.execute("""
        SELECT 
            COUNT(*) as total_solucoes,
            SUM(CASE WHEN status = 'aprovada' THEN 1 ELSE 0 END) as aprovadas,
            SUM(CASE WHEN status = 'em_analise' THEN 1 ELSE 0 END) as pendentes,
            SUM(CASE WHEN status = 'reprovada' THEN 1 ELSE 0 END) as reprovadas,
            AVG(pontuacao_final) as media_pontuacao
        FROM solucoes
        WHERE user_id = %s
    """, (current_user['id'],))
    
    stats_solucoes = cursor.fetchone()
    
    # Dados do usuário
    cursor.execute("""
        SELECT pontos_totais, nivel_atual, patente
        FROM users
        WHERE id = %s
    """, (current_user['id'],))
    
    user_data = cursor.fetchone()
    
    # Posição no ranking
    cursor.execute("""
        SELECT COUNT(*) + 1 as posicao
        FROM users
        WHERE pontos_totais > %s AND ativo = TRUE
    """, (user_data['pontos_totais'],))
    
    ranking = cursor.fetchone()
    
    # Certificados obtidos
    cursor.execute("""
        SELECT COUNT(*) as total_certificados
        FROM certificados
        WHERE user_id = %s
    """, (current_user['id'],))
    
    certificados = cursor.fetchone()
    
    return {
        "total_solucoes": stats_solucoes['total_solucoes'] or 0,
        "solucoes_aprovadas": stats_solucoes['aprovadas'] or 0,
        "solucoes_pendentes": stats_solucoes['pendentes'] or 0,
        "solucoes_reprovadas": stats_solucoes['reprovadas'] or 0,
        "pontos_totais": user_data['pontos_totais'],
        "nivel_atual": user_data['nivel_atual'],
        "patente": user_data['patente'],
        "media_pontuacao": float(stats_solucoes['media_pontuacao']) if stats_solucoes['media_pontuacao'] else None,
        "ranking_posicao": ranking['posicao'],
        "certificados_obtidos": certificados['total_certificados']
    }

# ==================== HABILIDADES ====================

@router.get("/me/habilidades", response_model=List[dict])
def get_my_habilidades(
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Listar habilidades do usuário"""
    
    cursor.execute("""
        SELECT 
            uh.id,
            uh.nivel_proficiencia,
            uh.comprovado,
            h.nome as habilidade_nome,
            h.categoria
        FROM user_habilidades uh
        INNER JOIN habilidades h ON uh.habilidade_id = h.id
        WHERE uh.user_id = %s
        ORDER BY uh.nivel_proficiencia DESC
    """, (current_user['id'],))
    
    return cursor.fetchall()

@router.post("/me/habilidades", response_model=dict)
def add_habilidade(
    habilidade: HabilidadeAdd,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Adicionar habilidade ao perfil"""
    
    try:
        cursor.execute("""
            INSERT INTO user_habilidades (user_id, habilidade_id, nivel_proficiencia)
            VALUES (%s, %s, %s)
        """, (current_user['id'], habilidade.habilidade_id, habilidade.nivel_proficiencia))
        
        return {"message": "Habilidade adicionada com sucesso!"}
    
    except Exception as e:
        if "Duplicate entry" in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Habilidade já adicionada"
            )
        raise

@router.delete("/me/habilidades/{habilidade_id}", response_model=dict)
def remove_habilidade(
    habilidade_id: int,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Remover habilidade do perfil"""
    
    cursor.execute("""
        DELETE FROM user_habilidades 
        WHERE user_id = %s AND habilidade_id = %s
    """, (current_user['id'], habilidade_id))
    
    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habilidade não encontrada"
        )
    
    return {"message": "Habilidade removida com sucesso!"}

# ==================== MUDAR SENHA ====================

@router.post("/me/change-password", response_model=dict)
def change_password(
    password_data: PasswordChange,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Alterar senha do usuário"""
    
    from app.core.security import verify_password, hash_password
    
    # Buscar senha atual
    cursor.execute(
        "SELECT senha_hash FROM users WHERE id = %s",
        (current_user['id'],)
    )
    
    user = cursor.fetchone()
    
    # Verificar senha atual
    if not verify_password(password_data.senha_atual, user['senha_hash']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha atual incorreta"
        )
    
    # Atualizar senha
    nova_senha_hash = hash_password(password_data.senha_nova)
    
    cursor.execute(
        "UPDATE users SET senha_hash = %s WHERE id = %s",
        (nova_senha_hash, current_user['id'])
    )
    
    return {"message": "Senha alterada com sucesso!"}

# ==================== BUSCAR USUÁRIOS ====================

@router.get("/search", response_model=List[UserPublic])
def search_users(
    query: str = Query(..., min_length=3),
    limit: int = Query(20, le=50),
    cursor = Depends(get_db)
):
    """Buscar usuários por nome, username ou palavras-chave"""
    
    search_term = f"%{query}%"
    
    cursor.execute("""
        SELECT 
            id, nome, username, foto_perfil, 
            pontos_totais, nivel_atual, patente
        FROM users
        WHERE ativo = TRUE
        AND (
            nome LIKE %s 
            OR username LIKE %s 
            OR palavras_chave LIKE %s
        )
        ORDER BY pontos_totais DESC
        LIMIT %s
    """, (search_term, search_term, search_term, limit))
    
    return cursor.fetchall()

# ==================== HISTÓRICO DE ATIVIDADES ====================

@router.get("/me/atividades", response_model=List[dict])
def get_my_atividades(
    limit: int = 20,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Obter histórico de atividades do usuário"""
    
    cursor.execute("""
        SELECT 
            acao,
            detalhes,
            created_at
        FROM logs_atividade
        WHERE user_id = %s AND tipo_usuario = 'user'
        ORDER BY created_at DESC
        LIMIT %s
    """, (current_user['id'], limit))
    
    return cursor.fetchall()

# ==================== DESATIVAR CONTA ====================

@router.delete("/me/deactivate", response_model=dict)
def deactivate_account(
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    """Desativar conta do usuário"""
    
    cursor.execute(
        "UPDATE users SET ativo = FALSE WHERE id = %s",
        (current_user['id'],)
    )
    
    return {"message": "Conta desativada com sucesso. Entre em contato com o suporte para reativar."}

# ==================== PERFIL PÚBLICO ====================
# IMPORTANTE: Esta rota deve vir POR ÚLTIMO porque captura qualquer /{user_id}

@router.get("/{user_id}", response_model=UserPublic)
def get_user_profile(
    user_id: int,
    cursor = Depends(get_db)
):
    """Obter perfil público de um usuário"""
    
    cursor.execute(
        """SELECT id, nome, username, foto_perfil, 
           pontos_totais, nivel_atual, patente 
           FROM users WHERE id = %s AND ativo = TRUE""",
        (user_id,)
    )
    
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user

# ADICIONAR em user.py:
@router.get("/me/solucoes", response_model=List[dict])
def get_my_solucoes(
    status: Optional[str] = None,
    limit: int = 50,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    # TODO: Implementar lógica para retornar as soluções do usuário
    raise NotImplementedError("Endpoint não implementado ainda.")

@router.get("/me/certificados", response_model=List[dict])
def get_my_certificados(
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    # TODO: Implementar lógica para retornar os certificados do usuário
    raise NotImplementedError("Endpoint não implementado ainda.")

@router.get("/me/problemas-recomendados", response_model=List[dict])
def get_problemas_recomendados(
    limit: int = 10,
    current_user = Depends(get_current_user),
    cursor = Depends(get_db)
):
    # TODO: Implementar lógica para retornar problemas recomendados ao usuário
    raise NotImplementedError("Endpoint não implementado ainda.")