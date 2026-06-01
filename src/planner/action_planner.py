"""
Módulo de Planificación - Action Planner
Algoritmo de búsqueda para generar secuencias de acciones
"""
import json
from typing import List, Dict, Tuple, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class ActionType(Enum):
    """Tipos de acciones disponibles"""
    RETRIEVE = "recuperar_informacion"
    EXPLORE = "explorar_grafo"
    SYNTHESIZE = "generar_respuesta"
    SEARCH = "buscar"
    ANALYZE = "analizar"


@dataclass
class Action:
    """Representa una acción a ejecutar"""
    id: str
    name: str
    type: ActionType
    parameters: Dict
    dependencies: List[str]
    priority: int = 0
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario"""
        d = asdict(self)
        d["type"] = self.type.value
        return d


class ActionPlanner:
    """Planificador de acciones basado en algoritmos de búsqueda"""
    
    def __init__(self):
        """Inicializa el planificador"""
        self.available_actions: Dict[str, Action] = {}
        self.executed_actions: List[Action] = []
        self.plan: List[Action] = []
    
    def register_action(self, action: Action) -> None:
        """
        Registra una acción disponible
        
        Args:
            action: Acción a registrar
        """
        self.available_actions[action.id] = action
    
    def build_plan(self, goal: str, available_context: Dict = None) -> List[Action]:
        """
        Construye un plan de acciones para alcanzar un objetivo
        
        Args:
            goal: Objetivo a alcanzar
            available_context: Contexto disponible
            
        Returns:
            Lista de acciones ordenadas
        """
        plan = []
        
        # Lógica simple: siempre recuperar, luego explorar, luego sintetizar
        if "recuperar" in goal.lower() or True:  # Primera acción por defecto
            retrieve_action = Action(
                id="step_1",
                name="recuperar_informacion",
                type=ActionType.RETRIEVE,
                parameters={"query": goal, "top_k": 5},
                dependencies=[]
            )
            plan.append(retrieve_action)
        
        if "explorar" in goal.lower():
            explore_action = Action(
                id="step_2",
                name="explorar_grafo",
                type=ActionType.EXPLORE,
                parameters={"nodo_inicio": "entidad_1", "profundidad": 2},
                dependencies=["step_1"]
            )
            plan.append(explore_action)
        
        # Siempre terminar con síntesis
        synthesize_action = Action(
            id=f"step_{len(plan) + 1}",
            name="generar_respuesta",
            type=ActionType.SYNTHESIZE,
            parameters={"contexto": "recuperado", "pregunta": goal},
            dependencies=[p.id for p in plan]
        )
        plan.append(synthesize_action)
        
        self.plan = plan
        return plan
    
    def execute_plan(self, plan: List[Action], executor=None) -> Dict:
        """
        Ejecuta un plan de acciones
        
        Args:
            plan: Plan a ejecutar
            executor: Función que ejecuta cada acción
            
        Returns:
            Resultados de ejecución
        """
        results = {}
        executed = []
        
        for action in plan:
            # Verificar dependencias
            if action.dependencies:
                if not all(dep in executed for dep in action.dependencies):
                    print(f"⚠️  Saltando acción {action.id}: dependencias no cumplidas")
                    continue
            
            print(f"▶️  Ejecutando: {action.name}")
            
            if executor:
                try:
                    result = executor(action)
                    results[action.id] = result
                except Exception as e:
                    print(f"❌ Error ejecutando {action.id}: {e}")
                    results[action.id] = {"error": str(e)}
            else:
                # Simulación
                results[action.id] = {"status": "ejecutado", "accion": action.to_dict()}
            
            executed.append(action.id)
            self.executed_actions.append(action)
        
        return results
    
    def optimize_plan(self, plan: List[Action]) -> List[Action]:
        """
        Optimiza un plan de acciones
        
        Args:
            plan: Plan a optimizar
            
        Returns:
            Plan optimizado
        """
        # Ordenar por prioridad
        optimized = sorted(plan, key=lambda a: (-a.priority, len(a.dependencies)))
        
        # Eliminar acciones redundantes
        unique = []
        seen = set()
        for action in optimized:
            if action.id not in seen:
                unique.append(action)
                seen.add(action.id)
        
        return unique
    
    def get_plan_summary(self) -> str:
        """
        Genera un resumen del plan
        
        Returns:
            Resumen en formato texto
        """
        summary = "Plan de Acciones:\n"
        for i, action in enumerate(self.plan, 1):
            summary += f"\n{i}. {action.name}"
            summary += f"\n   - Tipo: {action.type.value}"
            summary += f"\n   - Parámetros: {action.parameters}"
            if action.dependencies:
                summary += f"\n   - Depende de: {action.dependencies}"
        
        return summary


def main():
    """Pruebas del módulo"""
    print("=" * 60)
    print("TEST: Action Planner")
    print("=" * 60)
    
    # Crear planificador
    planner = ActionPlanner()
    
    # Registrar acciones disponibles
    actions = [
        Action("retrieve", "Recuperar información", ActionType.RETRIEVE, {}, []),
        Action("explore", "Explorar grafo", ActionType.EXPLORE, {}, []),
        Action("synthesize", "Sintetizar respuesta", ActionType.SYNTHESIZE, {}, []),
    ]
    
    for action in actions:
        planner.register_action(action)
    
    # Construir plan para un objetivo
    goal = "¿Cuál es la relación entre IA y Graph RAG?"
    print(f"\n🎯 Objetivo: {goal}")
    print()
    
    plan = planner.build_plan(goal)
    print(planner.get_plan_summary())
    
    # Optimizar plan
    print("\n\n🔧 Optimizando plan...")
    optimized = planner.optimize_plan(plan)
    
    # Ejecutar plan
    print("\n\n▶️  Ejecutando plan...")
    results = planner.execute_plan(optimized)
    
    print(f"\n✅ Ejecución completada")
    print(f"   Acciones ejecutadas: {len(results)}")


if __name__ == "__main__":
    main()
