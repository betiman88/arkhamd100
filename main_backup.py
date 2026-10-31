
import asyncio
import math
import flet as ft

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
        height=215,
        controls=[
            ft.Container(
                width=240,
                height=215,
                alignment=ft.Alignment.CENTER,
                content=dice_image,
            ),

            # Número superpuesto sobre el dado
            ft.Container(
                width=240,
                height=215,
                alignment=ft.Alignment.CENTER,
                content=dice_display,
            ),
        ],
    )

    # ----------------------------------
    # FUNCIÓN DE LANZAMIENTO
    # ----------------------------------

    async def make_roll(e):

        try:
            skill = int(skill_input.value)

            # Generamos la tirada REAL una sola vez
            roll = roll_d100()

            # Calculamos su clasificación
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

        # Bloqueamos los controles mientras gira
        roll_button.disabled = True
        skill_input.disabled = True

        result_display.value = "CONSULTANDO EL DESTINO..."
        result_display.color = GREEN

        message_display.value = "Los dados han sido invocados."

        dice_display.value = "?"
        dice_display.size = 28

        page.update()

        # ----------------------------------
        # ANIMACIÓN RÁPIDA DEL DADO
        # Duración programada: 1,06 segundos
        # ----------------------------------

        durations = [
            80, 90, 100, 120, 150, 220, 300
        ]

        # Números decorativos durante el giro.
        # No modifican la tirada real.
        display_numbers = [
            "17", "83", "42", "06",
            "91", "28", "74",
        ]

        for i, duration in enumerate(durations):

            # Giro que va perdiendo velocidad
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

        # Reactivamos los controles
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

            ft.Text(
                "LOS MISTERIOS DEL UNIVERSO",
                size=13,
                color=PARCHMENT,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "No todos los secretos deberían ser descubiertos.",
                size=11,
                color=MUTED,
                text_align=ft.TextAlign.CENTER,
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

            ft.Container(height=15),

            dice_panel,

            ft.Container(height=20),

            ft.Text(
                "PH'NGLUI MGLW'NAFH CTHULHU",
                size=10,
                color=PARCHMENT,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "R'LYEH WGAH'NAGL FHTAGN",
                size=10,
                color=MUTED,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Container(height=15),

            ft.Text(
                "ARKHAM D100 · DANI GE ESE",
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
