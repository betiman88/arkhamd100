
def calculate_roll(skill: int, roll: int) -> dict:
    """
    Clasifica una tirada D100 según las reglas
    de La llamada de Cthulhu 7.ª edición.

    skill: porcentaje de habilidad (1-100)
    roll: resultado del dado (1-100)
    """

    # Validar los valores recibidos
    if not isinstance(skill, int) or not 1 <= skill <= 100:
        raise ValueError("La habilidad debe estar entre 1 y 100.")

    if not isinstance(roll, int) or not 1 <= roll <= 100:
        raise ValueError("El resultado debe estar entre 1 y 100.")

    # Calcular los niveles de éxito
    difficult = skill // 2
    extreme = skill // 5

    # Clasificar el resultado
    if roll == 1:
        result = "ÉXITO CRÍTICO"

    elif roll == 100 or (skill < 50 and roll >= 96):
        result = "PIFIA"

    elif roll <= extreme:
        result = "ÉXITO EXTREMO"

    elif roll <= difficult:
        result = "ÉXITO DIFÍCIL"

    elif roll <= skill:
        result = "ÉXITO NORMAL"

    else:
        result = "FALLO"

    return {
        "skill": skill,
        "roll": roll,
        "difficult_threshold": difficult,
        "extreme_threshold": extreme,
        "result": result
    }
