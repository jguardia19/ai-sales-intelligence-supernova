
FACTUAL_QUESTIONS = [
    "¿Cuál es la categoría con mayor ingreso total?",
    "¿Cuál es el producto más vendido en el año?",
    "¿Cuál es el estado con más ventas?",
    "¿Cuántos productos no se vendieron en el último año?",
]


RANKING_QUESTIONS = [
    "Muestra el top 5 de productos más vendidos.",
    "¿Cuáles son las 3 categorías con mayor ingreso?",
    "Ranking de clientes por volumen de compra.",
    "Top estados por ventas.",
]



ANALYSIS_QUESTIONS = [
    "Analiza el desempeño general del negocio.",
    "¿Qué tendencias observas en las ventas?",
    "¿Cómo se comportan los clientes top?",
    "¿Qué patrones ves en los productos más vendidos?",
]


RISK_QUESTIONS = [
    "¿Qué riesgos ves en el inventario actual?",
    "¿Qué productos representan mayor riesgo de estancamiento?",
    "¿Dónde ves oportunidades de crecimiento?",
    "¿Qué decisiones tomarías para mejorar ventas?",
]


AMBIGUOUS_QUESTIONS = [
    "¿Cuál es la proyección futura del negocio?",
    "¿Cómo está posicionada la empresa frente a la competencia?",
]



MULTI_CONTEXT_QUESTIONS = [
    "¿Qué clientes compran más en categorías específicas?",
    "¿Cómo se relaciona el inventario con las ventas?",
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


if __name__ == "__main__":
    print("Total preguntas:", TOTAL_QUESTIONS)
    for i, q in enumerate(TEST_QUESTIONS, 1):
        print(f"{i}. {q}")