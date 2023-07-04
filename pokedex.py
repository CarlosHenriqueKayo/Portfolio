from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlite3

app = FastAPI()

conexao = sqlite3.connect('pokedex.db')
cursor = conexao.cursor()
# Inicializar a conexão com o banco de dados
@app.on_event("startup")
def startup():
    return conexao

# Fechar a conexão com o banco de dados ao encerrar o aplicativo
@app.on_event("shutdown")
def shutdown(conexao):
    conexao.close()   

# Lista de cadastro
pokemons = []

# Lista tipos
types = []

# Cadastro
@app.post("/pokemon", tags=["Pokemon"])
def create_pokemon(pokemon: dict):
    pokemons.append(pokemon)
    return {"message": "Pokémon cadastrado com sucesso", "pokemon": pokemon}

# Obter todos os pokemons cadastrados
@app.get("/pokemon", tags=["Pokedex"])
def get_all_pokemons():
    return {"pokemons": pokemons}

# Obter pokemon pelo id
@app.get("/pokemon/{pokemon_id}", tags=["Pokemon"])
def get_pokemon_by_id(pokemon_id:int):
    for pokemon in pokemons:
        if pokemon["pokemon_id"] == pokemon_id:
            return {"pokemon": pokemon}
    return {"message": "Pokémon não encontrado"}

# Tipo de Pokémon
@app.post ("/pokemons/type", tags=["Type"])
def create_type(pokemon_type: dict):
    types.append(pokemon_type)
    return {"message": f" Pokémon tipo {pokemon_type['type']} cadastrado com sucesso"}

# Obter todos os tipos de pokemons cadastrados
@app.get("/pokemon/type/{pokemons_type}", tags=["Type"])
def get_all_pokemons_type():
    return {"type": types}

# Atualizar dados pelo id
@app.put("/pokemon/{pokemon_id}", tags=["Pokemon"])
def update_pokemon(pokemon_id:int, update_pokemon: dict):
    for pokemon in pokemons:
        if pokemon["pokemon_id"] == pokemon_id:
            pokemon.update(update_pokemon)
            return {"message": "Dados do Pokémon atualizados com sucesso", "pokemon": pokemon}
    return {"message": "Pokémon não encontrado"}

# Atualizar tipo pelo Type id
@app.put("/pokemon/type/{type_id}", tags=["Type"])
def update_pokemon_type(type_id:int, update_type: dict):
    for pokemon_type in types:
        if pokemon_type["type_id"] == type_id:
            pokemon_type.update(update_type)
            return {"message": "Dados do Pokémon atualizados com sucesso"}
    return {"message": "Pokémon não encontrado"}

# Excluir Pokemon pelo id
@app.delete("/pokemon/{pokemon_id}", tags=["Pokemon"])
def delete_pokemon(pokemon_id:int):
    for pokemon in pokemons:
        if pokemon["pokemon_id"] == pokemon_id:
            pokemons.remove(pokemon)
            return {"message": f"{pokemon['pokemon_name']} removido com sucesso"}
    return {"message": "Pokémon não encontrado"}

# Excluir Tipo Pokemon pelo type ID
@app.delete("/pokemon/type/{type_id}", tags=["Type"])
def delete_type(type_id:int):
    for pokemon_type in types:
        if pokemon_type["type_id"] == type_id:
            types.remove(pokemon_type)
            return {"message": f"Tipo {pokemon_type['type']} removido com sucesso"}
    return {"message": f"Tipo não encontrado"}

# Definir modelo para Pokémon
class Pokemon(BaseModel):
    pokemon_name: str = Field(default="Charizard")
    pokemon_id: int = Field(default=0)
    pokemon_type_id: int = Field(default=1)

# Cadastro Pokemon
@app.post("/pokemon", tags=["Pokemon"])
async def create_pokemon(pokemon: Pokemon):
    query = "INSERT INTO pokemons (pokemon_name, pokemon_id, pokemon_type_id) VALUES (?, ?, ?)"
    values = pokemon.dict()
    cursor.execute(query, values)
    return {"message": "Pokémon cadastrado com sucesso", "pokemon": pokemon.dict()}

# Definir modelo para Tipos
class PokemonType(BaseModel):
    type: str = Field(default="fogo")
    type_id: int = Field(default=1)

# Cadastro Tipos
@app.post ("/pokemons/type", tags=["Type"])
async def create_type(pokemon_type: PokemonType):
    query = "INSERT INTO types (type, type_id) VALUES (?, ?)"
    values = pokemon_type.dict()
    cursor.execute(query, values)
    return {"message": f"Tipo {pokemon_type.type} cadastrado com sucesso"}

