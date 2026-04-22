

FACTUAL_QUESTIONS = [
    "¿Cuál es la categoría con mayor ingreso total?",
    "¿Cuál es el producto más vendido en el año?",
    "¿Qué cliente tiene mayor volumen de compras?",
    "¿Cuál es el estado con más ventas?",
    "¿Cuál es el ticket promedio global?",
    "¿Cuántos productos no se vendieron en el último año?",
    "¿Qué almacén tiene mayor stock total?",
    "¿Qué categoría tiene menor desempeño?",
    "¿Cuál es el mes con mayores ventas?",
    "¿Cuántos clientes activos hay actualmente?",
]


RANKING_QUESTIONS = [
    "Muestra el top 5 de productos más vendidos.",
    "¿Cuáles son las 3 categorías con mayor ingreso?",
    "Ranking de clientes por volumen de compra.",
    "Top estados por ventas.",
    "Ranking de productos estancados más críticos.",
    "¿Cuáles son los 5 productos con mayor riesgo por inventario?",
    "Ranking de almacenes por stock.",
    "¿Qué categorías dominan el negocio?",
    "Ranking de meses por ventas.",
    "Top productos por categoría.",
]



ANALYSIS_QUESTIONS = [
    "Analiza el desempeño general del negocio.",
    "¿Qué tendencias observas en las ventas?",
    "¿Qué categorías parecen más importantes?",
    "¿Cómo se comportan los clientes top?",
    "¿Qué patrones ves en los productos más vendidos?",
    "¿Cómo se distribuyen las ventas por estado?",
    "¿Qué comportamiento tienen los clientes frecuentes?",
    "¿Qué conclusiones puedes sacar del inventario?",
    "¿Qué indica el ticket promedio sobre el negocio?",
    "¿Qué factores parecen impulsar las ventas?",
]



RISK_QUESTIONS = [
    "¿Qué riesgos ves en el inventario actual?",
    "¿Qué productos representan mayor riesgo de estancamiento?",
    "¿Dónde ves oportunidades de crecimiento?",
    "¿Qué categorías podrían crecer más?",
    "¿Qué clientes tienen potencial de recompra?",
    "¿Qué problemas podríamos tener en logística?",
    "¿Qué estados tienen bajo rendimiento?",
    "¿Qué decisiones tomarías para mejorar ventas?",
    "¿Qué productos deberían promocionarse?",
    "¿Dónde ves ineficiencias?",
]



AMBIGUOUS_QUESTIONS = [
    "¿Qué opinas del comportamiento del mercado?",
    "¿Cómo está posicionada la empresa frente a la competencia?",
    "¿Qué factores externos afectan las ventas?",
    "¿Cuál es la proyección futura del negocio?",
    "¿Qué estrategia global recomendarías?",
]



MULTI_CONTEXT_QUESTIONS = [
    "Relaciona categorías con productos más vendidos.",
    "¿Qué estados compran más ciertas categorías?",
    "¿Qué clientes compran más en categorías específicas?",
    "¿Cómo se relaciona el inventario con las ventas?",
    "¿Qué productos dominan dentro de las categorías líderes?",
]



TEST_QUESTIONS = (
    FACTUAL_QUESTIONS
    + RANKING_QUESTIONS
    + ANALYSIS_QUESTIONS
    + RISK_QUESTIONS
    + AMBIGUOUS_QUESTIONS
    + MULTI_CONTEXT_QUESTIONS
)



TOTAL_QUESTIONS = len(TEST_QUESTIONS)

CATEGORIES = {
    "factual": len(FACTUAL_QUESTIONS),
    "ranking": len(RANKING_QUESTIONS),
    "analysis": len(ANALYSIS_QUESTIONS),
    "risk": len(RISK_QUESTIONS),
    "ambiguous": len(AMBIGUOUS_QUESTIONS),
    "multi_context": len(MULTI_CONTEXT_QUESTIONS),
}


if __name__ == "__main__":
    print("Total preguntas:", TOTAL_QUESTIONS)
    print("Distribución:", CATEGORIES)

    print("\nEjemplo:")
    for q in TEST_QUESTIONS[:5]:
        print("-", q)