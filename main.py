
import asyncio
import math
import random
import flet as ft
import flet_audio as fta

from core.dice import roll_d100
from core.calculator import calculate_roll


def main(page: ft.Page):

    # ----------------------------------
    # CONFIGURACIÓN GENERAL
    # ----------------------------------

    page.title = "ARKHAM D100"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#10140F"
    page.padding = 0

    page.window.width = 430
    page.window.height = 800

    # ----------------------------------
    # PALETA DE COLORES
    # ----------------------------------

    GREEN = "#91B878"
    DARK_GREEN = "#263D2B"
    PARCHMENT = "#D5C69A"
    MUTED = "#B4B9A9"
    RED = "#9E3939"
    GOLD = "#B99A55"

    # ----------------------------------
    # TÍTULOS ALEATORIOS
    # ----------------------------------

    titles = [
        "MÁS ALLÁ DE LA RAZÓN",
        "EL ABISMO NOS OBSERVA",
        "DONDE LA CORDURA TERMINA",
        "LOS SECRETOS DE R'LYEH",
        "EL HORROR AGUARDA",
        "BAJO LA SOMBRA DE LOS ANTIGUOS",
        "LO QUE NO DEBERÍA SER CONOCIDO",
        "EL UNIVERSO NO ESTÁ HECHO PARA NOSOTROS",
        "EN LAS PUERTAS DE LA LOCURA",
        "EL DESTINO ESTÁ ESCRITO EN SANGRE",
        "NINGÚN INVESTIGADOR ESTÁ A SALVO",
        "LA OSCURIDAD TIENE MUCHOS NOMBRES",
        "EL MIEDO ES SOLO EL PRINCIPIO",
        "CUANDO LOS DIOSES DESPIERTEN",
        "LA CORDURA ES UNA ILUSIÓN",
        "EL VELO DE LO DESCONOCIDO",
        "LOS LÍMITES DE LA REALIDAD",
        "EN EL UMBRAL DEL ABISMO",
        "ECOS DE UN UNIVERSO MUERTO",
        "LA VERDAD YACE MÁS ALLÁ",
        "SECRETOS ENTERRADOS EN LA ETERNIDAD",
    ]

    selected_title = random.choice(titles)

    # ----------------------------------
    # CITAS DE H. P. LOVECRAFT
    # Traducciones y adaptaciones al español
    # ----------------------------------

    quotes = [
        (
            "La emoción más antigua y más intensa de la "
            "humanidad es el miedo, y el más antiguo y más "
            "intenso de los miedos es el miedo a lo desconocido.",
            "El horror sobrenatural en la literatura"
        ),
        (
            "Vivimos en una plácida isla de ignorancia, "
            "en medio de negros mares de infinitud.",
            "La llamada de Cthulhu"
        ),
        (
            "No está muerto aquello que puede yacer eternamente, "
            "y con extraños eones incluso la muerte puede morir.",
            "La ciudad sin nombre"
        ),
        (
            "He visto más allá de los límites del infinito "
            "y he atraído demonios desde las estrellas.",
            "Desde el más allá"
        ),
        (
            "Los buscadores del horror frecuentan lugares "
            "extraños y lejanos.",
            "La imagen en la casa"
        ),
        (
            "El mundo es ciertamente cómico, pero el chiste "
            "recae sobre la humanidad.",
            "En defensa de Dagon"
        ),
        (
            "En su casa de R'lyeh, el difunto Cthulhu "
            "espera soñando.",
            "La llamada de Cthulhu"
        ),
        (
            "La cosa más misericordiosa del mundo es, creo, "
            "la incapacidad de la mente humana para relacionar "
            "todo su contenido.",
            "La llamada de Cthulhu"
        ),
        (
            "De los mayores horrores rara vez está ausente "
            "la ironía.",
            "La casa evitada"
        ),
        (
            "Los recuerdos y las posibilidades son más "
            "horribles que las realidades.",
            "Herbert West: Reanimador"
        ),
        (
            "Una voz de otras épocas pertenece a un cementerio "
            "de otras épocas.",
            "La llamada de Cthulhu"
        ),
        (
            "Los niños siempre temerán a la oscuridad.",
            "El horror sobrenatural en la literatura"
        ),
    ]

    selected_quote, selected_author = random.choice(quotes)

    # ----------------------------------
    # CONTROL DE SONIDO
    # ----------------------------------

    sound_enabled = True

    # ----------------------------------
    # REPRODUCTORES DE AUDIO
    # ----------------------------------

    dice_audio = fta.Audio(
        src="sounds/dice_roll.mp3",
        autoplay=False,
        volume=0.70,
        release_mode=fta.ReleaseMode.STOP,
    )

    fail_audio = fta.Audio(
        src="sounds/fail.mp3",
        autoplay=False,
        volume=0.85,
        release_mode=fta.ReleaseMode.STOP,
    )

    page.services.append(dice_audio)
    page.services.append(fail_audio)

    # ----------------------------------
    # CAMPO DE HABILIDAD
    # ----------------------------------

    skill_input = ft.TextField(
        label="Habilidad del investigador",
        hint_text="Entre 1 y 100",
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
        width=280,
        border_color=GREEN,
        focused_border_color=PARCHMENT,
        cursor_color=GREEN,
        bgcolor="#8010140F",
    )

    # ----------------------------------
    # RESULTADO DEL DADO
    # ----------------------------------

    dice_display = ft.Text(
        "",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=PARCHMENT,
        text_align=ft.TextAlign.CENTER,
        bgcolor="#B010140F",
    )

    result_display = ft.Text(
        "ESPERANDO TIRADA",
        size=21,
        weight=ft.FontWeight.BOLD,
        color=MUTED,
        text_align=ft.TextAlign.CENTER,
    )

    message_display = ft.Text(
        "El destino del investigador está por decidirse.",
        size=12,
        color=MUTED,
        text_align=ft.TextAlign.CENTER,
    )

    # ----------------------------------
    # TÍTULO Y CITA DE BIENVENIDA
    # ----------------------------------

    title_display = ft.Text(
        selected_title,
        size=13,
        weight=ft.FontWeight.BOLD,
        color=GREEN,
        text_align=ft.TextAlign.CENTER,
    )

    quote_display = ft.Text(
        f"«{selected_quote}»",
        size=11,
        italic=True,
        color=PARCHMENT,
        text_align=ft.TextAlign.CENTER,
    )

    quote_author_display = ft.Text(
        f"— {selected_author} —",
        size=9,
        color=MUTED,
        text_align=ft.TextAlign.CENTER,
    )

    # ----------------------------------
    # IMAGEN ANIMADA DEL DADO
    # ----------------------------------

    dice_image = ft.Image(
        src="images/dice.png",
        width=215,
        height=215,
        fit=ft.BoxFit.CONTAIN,
        rotate=ft.Rotate(
            angle=0,
            alignment=ft.Alignment.CENTER,
        ),
        animate_rotation=ft.Animation(
            100,
            ft.AnimationCurve.LINEAR,
        ),
    )

    dice_stage = ft.Stack(
        width=240,
        height=185,
        controls=[
            ft.Container(
                width=240,
                height=185,
                alignment=ft.Alignment.CENTER,
                content=dice_image,
            ),

            ft.Container(
                width=240,
                height=185,
                alignment=ft.Alignment.CENTER,
                content=dice_display,
            ),
        ],
    )

    # ----------------------------------
    # ACTIVAR / DESACTIVAR SONIDO
    # ----------------------------------

    async def stop_audio():

        await dice_audio.pause()
        await dice_audio.seek(0)

        await fail_audio.pause()
        await fail_audio.seek(0)

    def toggle_sound(e):

        nonlocal sound_enabled

        sound_enabled = not sound_enabled

        if sound_enabled:
            sound_button.content = "♫  SOUND ON"
            sound_button.style.bgcolor = DARK_GREEN

        else:
            sound_button.content = "♫  SOUND OFF"
            sound_button.style.bgcolor = "#454545"

            page.run_task(stop_audio)

        page.update()

    sound_button = ft.Button(
        content="♫  SOUND ON",
        width=180,
        height=40,
        style=ft.ButtonStyle(
            bgcolor=DARK_GREEN,
            color=PARCHMENT,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=toggle_sound,
    )

    # ----------------------------------
    # FUNCIÓN DE LANZAMIENTO
    # ----------------------------------

    async def make_roll(e):

        try:
            skill = int(skill_input.value)

            # Generar la tirada real una sola vez
            roll = roll_d100()

            # Calcular su clasificación
            result = calculate_roll(skill, roll)

        except (ValueError, TypeError):

            dice_display.value = "?"
            result_display.value = "TIRADA IMPOSIBLE"
            result_display.color = RED

            message_display.value = (
                "Introduce un valor entero entre 1 y 100."
            )

            page.update()
            return

        # ----------------------------------
        # BLOQUEAR CONTROLES
        # ----------------------------------

        roll_button.disabled = True
        skill_input.disabled = True

        result_display.value = "CONSULTANDO EL DESTINO..."
        result_display.color = GREEN

        message_display.value = "Los dados han sido invocados."

        dice_display.value = "?"
        dice_display.size = 28

        page.update()

        # ----------------------------------
        # SONIDO DE TIRADA
        # ----------------------------------

        if sound_enabled:
            await dice_audio.seek(0)
            await dice_audio.play()

        # ----------------------------------
        # ANIMACIÓN DEL DADO
        # Duración programada: 1,06 segundos
        # ----------------------------------

        durations = [
            80, 90, 100, 120, 150, 220, 300
        ]

        display_numbers = [
            "17", "83", "42", "06",
            "91", "28", "74",
        ]

        for i, duration in enumerate(durations):

            angle = (i + 1) * (math.pi * 1.25)

            dice_image.animate_rotation = ft.Animation(
                duration,
                ft.AnimationCurve.LINEAR,
            )

            dice_image.rotate = ft.Rotate(
                angle=angle,
                alignment=ft.Alignment.CENTER,
            )

            dice_display.value = display_numbers[i]

            page.update()

            await asyncio.sleep(duration / 1000)

        # ----------------------------------
        # DETENER SONIDO DE TIRADA
        # ----------------------------------

        await dice_audio.pause()
        await dice_audio.seek(0)

        # ----------------------------------
        # MOSTRAR RESULTADO REAL
        # ----------------------------------

        dice_display.value = str(roll)
        dice_display.size = 28

        colors = {
            "ÉXITO CRÍTICO": GOLD,
            "ÉXITO EXTREMO": GREEN,
            "ÉXITO DIFÍCIL": "#75A85B",
            "ÉXITO NORMAL": "#A3B18A",
            "FALLO": "#D0D0D0",
            "PIFIA": RED,
        }

        result_display.value = result["result"]
        result_display.color = colors[result["result"]]

        message_display.value = (
            f"Habilidad: {skill}%  |  "
            f"Difícil: {result['difficult_threshold']}%  |  "
            f"Extremo: {result['extreme_threshold']}%"
        )

        page.update()

        # ----------------------------------
        # SONIDO ESPECIAL DE PIFIA
        # ----------------------------------

        if result["result"] == "PIFIA" and sound_enabled:

            await fail_audio.seek(0)
            await fail_audio.play()

        # ----------------------------------
        # REACTIVAR CONTROLES
        # ----------------------------------

        roll_button.disabled = False
        skill_input.disabled = False

        page.update()

    # ----------------------------------
    # BOTÓN DE LANZAMIENTO
    # ----------------------------------

    roll_button = ft.Button(
        content="✦  INVOCAR EL DESTINO  ✦",
        width=280,
        height=58,
        style=ft.ButtonStyle(
            bgcolor=DARK_GREEN,
            color=PARCHMENT,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=make_roll,
    )

    # ----------------------------------
    # PANEL DEL DADO
    # ----------------------------------

    dice_panel = ft.Container(
        content=ft.Column(
            controls=[

                ft.Text(
                    "✧  EL ORÁCULO DE LOS DADOS  ✧",
                    size=11,
                    color=GREEN,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text(
                    "◈",
                    size=25,
                    color=GOLD,
                ),

                dice_stage,

                result_display,

                message_display,

                ft.Text(
                    "◈",
                    size=25,
                    color=GOLD,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
        ),

        bgcolor="#B010140F",
        border=ft.Border.all(1, "#657B5940"),
        border_radius=16,
        padding=20,
        width=350,
    )

    # ----------------------------------
    # CONTENIDO PRINCIPAL
    # ----------------------------------

    content = ft.Column(
        controls=[

            ft.Container(height=15),

            ft.Text(
                "✦  ARKHAM D100  ✦",
                size=31,
                weight=ft.FontWeight.BOLD,
                color=GREEN,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "CALL OF CTHULHU · 7TH EDITION",
                size=10,
                color=PARCHMENT,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Divider(color="#657B5970"),

            ft.Container(height=15),

            # TÍTULO Y CITA ALEATORIOS

            ft.Container(
                width=350,
                padding=ft.Padding.symmetric(horizontal=15),
                content=ft.Column(
                    controls=[
                        title_display,
                        quote_display,
                        quote_author_display,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
            ),

            ft.Container(height=15),

            ft.Text(
                "INTRODUCE TU HABILIDAD",
                size=12,
                color=GREEN,
                weight=ft.FontWeight.BOLD,
            ),

            skill_input,

            ft.Container(height=15),

            roll_button,

            sound_button,

            ft.Container(height=15),

            dice_panel,

            ft.Container(height=20),

            # ----------------------------------
            # CRÉDITOS DE ARKHAM D100
            # ----------------------------------

            ft.Divider(color="#657B5940"),

            ft.Text(
                "DESARROLLO GRÁFICO: YOG-SOTHOTH",
                size=9,
                color=PARCHMENT,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "PROGRAMACIÓN ARCANA: NYARLATHOTEP",
                size=9,
                color=MUTED,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "DISEÑO SONORO: AZATHOTH",
                size=9,
                color=MUTED,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=5),

            ft.Text(
                "DIRECTOR: DANI GE ESE",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=GREEN,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=15),

            ft.Text(
                "ARKHAM D100 · UNA APP PARA EVITAR LAS MATES",
                size=9,
                color=MUTED,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=20),

        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ----------------------------------
    # CAPAS DE LA INTERFAZ
    # ----------------------------------

    page.add(
        ft.Stack(
            expand=True,
            controls=[

                # CAPA 1: ILUSTRACIÓN DE FONDO
                ft.Image(
                    src="images/background_cosmic.png",
                    fit=ft.BoxFit.COVER,
                    expand=True,
                ),

                # CAPA 2: OSCURECER EL FONDO
                ft.Container(
                    expand=True,
                    bgcolor="#A610140F",
                ),

                # CAPA 3: INTERFAZ
                content,

            ],
        )
    )


# ----------------------------------
# INICIO DE LA APLICACIÓN
# ----------------------------------

ft.run(main, assets_dir="assets")
