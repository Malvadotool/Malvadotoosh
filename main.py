#!/usr/bin/python

import random
import urllib.parse
import requests
from time import sleep
import os, signal, sys
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.style import Style
import pystyle
from pystyle import Colors, Colorate

from cpmcheats import CPMCheats


def signal_handler(sig, frame):
    print("\n bye bye...")
    sys.exit(0)


def gradient_text(text, colors):
    lines = text.splitlines()
    height = len(lines)
    width = max(len(line) for line in lines)
    colorful_text = Text()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != " ":
                color_index = int(
                    (
                        (x / (width - 1 if width > 1 else 1))
                        + (y / (height - 1 if height > 1 else 1))
                    )
                    * 0.5
                    * (len(colors) - 1)
                )
                color_index = min(
                    max(color_index, 0), len(colors) - 1
                )  # Ensure the index is within bounds
                style = Style(color=colors[color_index])
                colorful_text.append(char, style=style)
            else:
                colorful_text.append(char)
        colorful_text.append("\n")
    return colorful_text


def banner(console):
    os.system("cls" if os.name == "nt" else "clear")
    brand_name = "Únase a nuestro canal https://t.me/MALVADOTOOLCPM"

    text = Text(brand_name, style="bold black")

    console.print(text)
    console.print(
        "[bold white] ============================================================[/bold white]"
    )
    console.print(
        "[bold yellow]      𝗣𝗢𝗥 𝗙𝗔𝗩𝗢𝗥, 𝗖𝗜𝗘𝗥𝗥𝗘 𝗦𝗘𝗦𝗜𝗢𝗡 𝗘𝗡 𝗖𝗣𝗠 𝗔𝗡𝗧𝗘𝗦 𝗗𝗘 𝗨𝗦𝗔𝗥 𝗟𝗔 𝗛𝗘𝗥𝗥𝗔𝗠𝗜𝗘𝗡𝗧𝗔[/bold yellow]"
    )
    console.print("[bold yellow]      𝗡𝗢 𝗘𝗦𝗧𝗔 𝗣𝗘𝗥𝗠𝗜𝗧𝗜𝗗𝗢 𝗖𝗢𝗠𝗣𝗔𝗥𝗧𝗜𝗥 𝗟𝗔 𝗖𝗟𝗔𝗩𝗘 𝗗𝗘 𝗔𝗖𝗖𝗘𝗦𝗢[/bold yellow]")
    console.print(
        "[bold white] ============================================================[/bold white]"
    )


def load_player_data(cpm):
    response = cpm.get_player_data()

    if not response.get("ok"):
        console.print(
            "[bold yellow]⚠️ WARNING: Your login seems to be invalid or misconfigured.[/bold yellow]"
        )
        data = {}
    else:
        data = response.get("data", {})

    required_keys = {"floats", "localID", "money"}

    if not required_keys.issubset(data):
        console.print(
            "[bold yellow]⚠️ WARNING: New accounts must log into the game at least once for full data to be available.[/bold yellow]"
        )

    console.print(
        "[bold yellow]========[white] PLAYER DETAILS [/white]========[/bold yellow]"
    )

    console.print(
        f"[bold white]   >> Name        : {data.get('Name', 'UNDEFINED')}[/bold white]"
    )
    console.print(
        f"[bold white]   >> LocalID     : {data.get('localID', 'UNDEFINED')}[/bold white]"
    )
    console.print(
        f"[bold white]   >> Moneys      : {data.get('money', 'UNDEFINED')}[/bold white]"
    )
    console.print(
        f"[bold white]   >> Coins       : {data.get('coin', 'UNDEFINED')}[/bold white]"
    )


def load_key_data(cpm):

    data = cpm.get_key_data()

    console.print(
        "[bold][red]========[/red][ Detalles de llave de aceceso ][red]========[/red][/bold]"
    )

    console.print(
        f"[bold white]   >> clave de acceso  [/bold white]: [black]{data.get('access_key')}[/black]"
    )

    console.print(
        f"[bold white]   >> Telegram ID : {data.get('telegram_id')}[/bold white]"
    )

    console.print(
        f"[bold white]   >> SALDO     : {data.get('coins') if not data.get('is_unlimited') else 'Ilimitado'}[/bold white]"
    )


def prompt_valid_value(content, tag, password=False):
    while True:
        value = Prompt.ask(content, password=password)
        if not value or value.isspace():
            console.print(
                f"[bold yellow]{tag} No puede estar vacío ni contener solo espacios. Inténtalo de nuevo. (✘)[/bold yellow]"
            )
        else:
            return value


def load_client_details():
    response = requests.get("http://ip-api.com/json")
    data = response.json()
    console.print(
        "[bold yellow] =============[bold white][ LOCALIZACIÓN ][/bold white]=============[/bold yellow]"
    )
    console.print(
        f"[bold white]    >> Country    : {data.get('country')} {data.get('zip')}[/bold white]"
    )
    console.print(
        "[bold yellow] ===============[bold white][ ＭＥＮＵ ][/bold white]===========[/bold yellow]"
    )


def interpolate_color(start_color, end_color, fraction):
    start_rgb = tuple(int(start_color[i : i + 2], 16) for i in (1, 3, 5))
    end_rgb = tuple(int(end_color[i : i + 2], 16) for i in (1, 3, 5))
    interpolated_rgb = tuple(
        int(start + fraction * (end - start)) for start, end in zip(start_rgb, end_rgb)
    )
    return "{:02x}{:02x}{:02x}".format(*interpolated_rgb)


def rainbow_gradient_string(customer_name):
    modified_string = ""
    num_chars = len(customer_name)
    start_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    end_color = "{:06x}".format(random.randint(0, 0xFFFFFF))
    for i, char in enumerate(customer_name):
        fraction = i / max(num_chars - 1, 1)
        interpolated_color = interpolate_color(start_color, end_color, fraction)
        modified_string += f"[{interpolated_color}]{char}"
    return modified_string


if __name__ == "__main__":
    console = Console()
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        banner(console)
        acc_email = prompt_valid_value(
            "[bold][?] Correo electrónico de la cuenta[/bold]", "EMAIL", password=False
        )
        acc_password = prompt_valid_value(
            "[bold][?] Contraseña de la cuenta[/bold]", "PASSWORD", password=False
        )
        acc_access_key = prompt_valid_value(
            "[bold][?] Clave de acceso[/bold]", "ACCESS KEY", password=False
        )
        console.print("[bold yellow][%] Intentando iniciar sesión[/bold yellow]: ", end=None)
        cpm = CPMCheats(acc_access_key)
        login_response = cpm.login(acc_email, acc_password)
        if login_response != 0:
            if login_response == 100:
                console.print("[bold yellow]CUENTA NO ENCONTRADA (✘)[/bold yellow]")
                sleep(2)
                continue
            elif login_response == 101:
                console.print("[bold yellow]CONTRASEÑA INCORRECTA (✘)[/bold yellow]")
                sleep(2)
                continue
            elif login_response == 103:
                console.print("[bold yellow]CLAVE DE ACCESO NO VÁLIDA (✘)[/bold yellow]")
                sleep(2)
                continue
            else:
                console.print("[bold yellow]TRY AGAIN[/bold yellow]")
                console.print(
                    "[bold yellow] '! Nota: asegúrese de completar los campos ![/bold yellow]"
                )
                sleep(2)
                continue
        else:
            console.print("[bold green]EXITOSO (✔)[/bold green]")
            sleep(1)
        while True:
            banner(console)
            load_player_data(cpm)
            load_key_data(cpm)
            load_client_details()
            choices = [
                "00",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
                "32",
                "33",
                "34",
                "35",
                "36",
                "37",
                "38",
                "39",
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "48",
                "49",
            ]
            console.print(
                "[bold yellow][bold white](01)[/bold white]: Aumentar el dinero                              [bold yellow]1500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](02)[/bold white]: Aumentar monedas                                [bold yellow]1500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](03)[/bold white]: Rango De Rey                                    [bold yellow]8000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](04)[/bold white]: Cambiar ID                                      [bold yellow]4500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](05)[/bold white]: Cambiar nombre                                  [bold yellow]100[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](06)[/bold white]: Cambiar nombre (Arcoíris)                       [bold yellow]100[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](07)[/bold white]: Diseños de placas aleatorias                    [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](08)[/bold white]: Eliminar cuenta                                 [bold yellow]Gratis[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](09)[/bold white]: Registro de cuenta                              [bold yellow]Gratis[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](10)[/bold white]: Eliminar amigos                                 [bold yellow]500[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](11)[/bold white]: Desbloquear Lamborghinis (solo iPhone)          [bold yellow]5000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](12)[/bold white]: Desbloquear todos los coches                    [bold yellow]6000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](13)[/bold white]: Desbloquear la sirena de todos los coches       [bold yellow]3500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](14)[/bold white]: Desbloquear el motor W16                        [bold yellow]4000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](15)[/bold white]: Desbloquea todos los claxon                     [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](16)[/bold white]: Desactivar Daño del motor                       [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](17)[/bold white]: Desbloquea combustible ilimitado                [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](18)[/bold white]: Desbloquear casa 3                              [bold yellow]4000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](19)[/bold white]: Desbloquear humo                                [bold yellow]4000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](20)[/bold white]: Desbloquear rines                               [bold yellow]4000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](21)[/bold white]: Desbloquear animaciones                         [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](22)[/bold white]: Desbloquear equipos M                           [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](23)[/bold white]: Desbloquear equipos F                           [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](24)[/bold white]: Cambiar carreras ganadas                        [bold yellow]1000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](25)[/bold white]: Cambiar carreras perdidas                       [bold yellow]1000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](26)[/bold white]: Clonar cuenta                                   [bold yellow]7000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](27)[/bold white]: HP personalizado                                [bold yellow]2500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](28)[/bold white]: Ángulo personalizado                            [bold yellow]1500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](29)[/bold white]: Quemador neumáticos personalizado               [bold yellow]1500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](30)[/bold white]: Millaje de coches personalizados                [bold yellow]1500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](31)[/bold white]: Freno de coche personalizado                    [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](32)[/bold white]: Quitar el parachoques trasero                   [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](33)[/bold white]: Quitar el parachoques delantero                 [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](34)[/bold white]: Cambiar la contraseña de la cuenta              [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](35)[/bold white]: Cambiar el correo electrónico de la cuenta      [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](36)[/bold white]: Alerón personalizado                            [bold yellow]1000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](37)[/bold white]: Kit de carrocería personalizado                 [bold yellow]1000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](38)[/bold white]: Desbloquea rines premium                        [bold yellow]4500K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](39)[/bold white]: Desbloquear Toyota Crown                        [bold yellow]2000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](40)[/bold white]: Desbloquear sombrero de clan (M)                [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](41)[/bold white]: Quitar cabeza macho                             [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](42)[/bold white]: Quitar cabeza hembra                            [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](43)[/bold white]: Desbloquear el Top 1 del Clan (M)               [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](44)[/bold white]: Desbloquear los 2 mejores del clan (M)          [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](45)[/bold white]: Desbloquear los 3 mejores del clan (M)          [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](46)[/bold white]: Desbloquear el Top 1 del Clan (FM)              [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](47)[/bold white]: Desbloquear los 2 mejores del clan (FM)         [bold yellow]3000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](48)[/bold white]: Desbloquear Mercedes Cls                        [bold yellow]4000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](49)[/bold white]: Comba de postura                                [bold yellow]1000K[/bold yellow][/bold yellow]"
            )
            console.print(
                "[bold yellow][bold white](0) [/bold white]: Salir de la herramienta [/bold yellow]"
            )

            console.print(
                "[bold yellow]===============[bold white][ EL MALVADO ][/bold white]===============[/bold yellow]"
            )

            service = IntPrompt.ask(
                f"[bold][?] Seleccione un servicio [red][1-{choices[-1]} or 0][/red][/bold]",
                choices=choices,
                show_choices=False,
            )

            console.print(
                "[bold yellow]===============[bold white][ EL MALVADO ][/bold white]===============[/bold yellow]"
            )

            if service == 0:  # Exit
                console.print("[bold white] Gracias por usar mi herramienta[/bold white]")
            elif service == 1:  # Increase Money
                console.print(
                    "[bold yellow][bold white][?][/bold white] Inserta cuanto dinero deseas[/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Cantidad")
                console.print("[%] Guardado de datos: ", end=None)
                if amount > 0 and amount <= 500000000:
                    if cpm.set_player_money(amount):
                        console.print("[bold green]EXITOSO (✔)[/bold green]")
                        console.print(
                            "[bold green]======================================[/bold green]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO (✘)[/bold yellow]")
                        console.print(
                            "[bold yellow]Por favor, inténtelo de nuevo más tarde! (✘)[/bold yellow]"
                        )
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO (✘)[/bold yellow]")
                    console.print("[bold yellow]¡Por favor utilice valores válidos! (✘)[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 2:  # Increase Coins
                console.print(
                    "[bold yellow][bold white][?][/bold white] Inserta cuantas monedas deseas[/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Cantidad")
                print("[ % ] Guardado de datos: ", end="")
                if amount > 0 and amount <= 500000:
                    if cpm.set_player_coins(amount):
                        console.print("[bold green]EXITOSO (✔)[/bold green]")
                        console.print(
                            "[bold green]======================================[/bold green]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO[/bold yellow]")
                        console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] 'Por favor, utilice valores válidos[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 3:  # King Rank
                console.print(
                    "[bold yellow][!] Nota:[/bold yellow]: Si el rango de rey no aparece en el juego, ciérrelo y ábralo varias veces..",
                    end=None,
                )
                console.print(
                    "[bold yellow][!] Note:[/bold yellow]: Por favor, no hagas King Rank en la misma cuenta dos veces..",
                    end=None,
                )
                sleep(2)
                console.print("[%] Subido a king: ", end=None)
                if cpm.set_player_rank():
                    console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                    console.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 4:  # Change ID
                console.print("[bold yellow] '[?] Ingrese su nuevo ID [/bold yellow]")
                new_id = Prompt.ask("[?] ID")
                console.print("[%] Guardando sus datos: ", end=None)
                if (
                    len(new_id) >= 1
                    and len(new_id)
                    <= 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                    and (" " in new_id) == False
                ):
                    if cpm.set_player_localid(new_id.upper()):
                        console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO[/bold yellow]")
                        console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] 'Por favor utilice un ID valido [/bold yellow]")
                    sleep(2)
                    continue
            elif service == 5:  # Change Name
                console.print("[bold yellow] '[?] Ingrese su nuevo nombre[/bold yellow]")
                new_name = Prompt.ask("[?] Nombre")
                console.print("[%] Guardado de datos: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(new_name):
                        console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO[/bold yellow]")
                        console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] 'Por favor, utilice valores válidos[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 6:  # Change Name Rainbow
                console.print("[bold yellow] '[?] Ingresa tu nuevo nombre arcoíris[/bold yellow]")
                new_name = Prompt.ask("[?] Nombre")
                console.print("[%] Guardando sus datos: ", end=None)
                if len(new_name) >= 0 and len(new_name) <= 999999999:
                    if cpm.set_player_name(rainbow_gradient_string(new_name)):
                        console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO[/bold yellow]")
                        console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] 'Por favor, utilice valores válidos[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 7:  # Number Plates
                console.print("[%] Dándole una Matrícula: ", end=None)
                if cpm.set_player_plates():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 8:  # Account Delete
                console.print(
                    "[bold yellow] '[!] Después de eliminar tu cuenta no hay vuelta atrás !![/bold yellow]"
                )
                answ = Prompt.ask(
                    "[?] ¿Quieres eliminar esta cuenta? ?!",
                    choices=["y", "n"],
                    default="n",
                )
                if answ == "y":
                    cpm.delete()
                    console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                    console.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    console.print(
                        "[bold yellow] Gracias por usar nuestra herramienta, únete a nuestro canal de telegram.: @Jaim2s[/bold yellow]"
                    )
                else:
                    continue
            elif service == 9:  # Account Register
                console.print("[bold yellow] '[!] Registrar una nueva cuenta[/bold yellow]")
                acc2_email = prompt_valid_value(
                    "[?] Account Email", "Gmail", password=False
                )
                acc2_password = prompt_valid_value(
                    "[?] Account Password", "Contraseña", password=False
                )
                console.print("[%] Creando una nueva cuenta: ", end=None)
                status = cpm.register(acc2_email, acc2_password)
                if status == 0:
                    console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                    console.print(
                        "[bold yellow] '======================================[/bold yellow]"
                    )
                    console.print(
                        "[bold yellow] f'INFO: Para poder modificar esta cuenta con Termux[/bold yellow]"
                    )
                    console.print(
                        "[bold yellow] 'Debes iniciar sesión en el juego usando esta cuenta[/bold yellow]"
                    )
                    sleep(2)
                    continue
                elif status == 105:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print(
                        "[bold yellow] 'Este correo electrónico ya existe ![/bold yellow]"
                    )
                    sleep(2)
                    continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 10:  # Delete Friends
                console.print("[%] Eliminar a tus amigos: ", end=None)
                if cpm.delete_player_friends():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 11:  # Unlock All Lamborghinis
                console.print(
                    "[!] Nota: esta función tarda un tiempo en completarse, no la canceles..",
                    end=None,
                )
                console.print("[%] Desbloqueo de todos los Lamborghinis: ", end=None)
                if cpm.unlock_all_lamborghinis():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 12:  # Unlock All Cars
                console.print("[%] Desbloqueo de todos los coches: ", end=None)
                if cpm.unlock_all_cars():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir? ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 13:  # Unlock All Cars Siren
                console.print("[%] Desbloqueo de la sirena de todos los coches: ", end=None)
                if cpm.unlock_all_cars_siren():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir? ", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 14:  # Unlock w16 Engine
                console.print("[%] Desbloqueo del motor w16: ", end=None)
                if cpm.unlock_w16():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 15:  # Unlock All Horns
                console.print("[%] Desbloqueando todos los claxon: ", end=None)
                if cpm.unlock_horns():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta1[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 16:  # Disable Engine Damage
                console.print("[%] Motor indestructibles desbloqueado: ", end=None)
                if cpm.disable_engine_damage():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] Do You want to Exit ?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 17:  # Unlimited Fuel
                console.print("[%] Gasolina infinita desbloqueada: ", end=None)
                if cpm.unlimited_fuel():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 18:  # Unlock House 3
                console.print("[%] Desbloqueado la casa de paga: ", end=None)
                if cpm.unlock_houses():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 19:  # Unlock Smoke
                console.print("[%] desbloqueando humo: ", end=None)
                if cpm.unlock_smoke():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 20:  # Unlock Wheels
                console.print("[%] Desbloqueo de rines: ", end=None)
                if cpm.unlock_wheels():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(8)
                    continue
            elif service == 21:  # Unlock Animations
                console.print("[%] Desbloqueo de animaciones: ", end=None)
                if cpm.unlock_animations():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 22:  # Unlock Equipaments Male
                console.print("[%] Desbloqueo de equipos masculinos: ", end=None)
                if cpm.unlock_equipments_male():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 23:  # Unlock Equipaments Female
                console.print("[%] Desbloqueo de equipos femeninos: ", end=None)
                if cpm.unlock_equipments_female():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 24:  # Change Races Wins
                console.print(
                    "[bold yellow] '[!] ponga las carreras ganadas que va a querer [/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Cantidad")
                console.print("[%] Cambiando sus datos: ", end=None)
                if (
                    amount > 0
                    and amount
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                ):
                    if cpm.set_player_wins(amount):
                        console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO[/bold yellow]")
                        console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] '[!] Por favor, utilice valores válidos[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 25:  # Change Races Loses
                console.print(
                    "[bold yellow] '[!] Ponga cuantas carreras perdidas quieres tener [/bold yellow]"
                )
                amount = IntPrompt.ask("[?] Cantidad")
                console.print("[%] Cambiando  sus datos: ", end=None)
                if (
                    amount > 0
                    and amount
                    <= 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
                ):
                    if cpm.set_player_loses(amount):
                        console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                        console.print(
                            "[bold yellow] '======================================[/bold yellow]"
                        )
                        answ = Prompt.ask(
                            "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                        )
                        if answ == "y":
                            console.print(
                                "[bold white] Gracias por usar mi herramienta[/bold white]"
                            )
                        else:
                            continue
                    else:
                        console.print("[bold yellow]FALLIDO[/bold yellow]")
                        console.print(
                            "[bold yellow] '[!] Por favor, utilice valores válidos[/bold yellow]"
                        )
                        sleep(2)
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] '[!] Por favor, utilice valores válidos[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 26:  # Clone Account
                console.print("[bold yellow] '[!] Por favor ingrese los datos de la cuenta[/bold yellow]")
                to_email = prompt_valid_value(
                    "[?] Correo electrónico de la cuenta", "Email", password=False
                )
                to_password = prompt_valid_value(
                    "[?] Contraseña de la cuenta", "Password", password=False
                )
                console.print("[%] Clonando tu cuenta: ", end=None)
                if cpm.account_clone(to_email, to_password):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print(
                        "[bold yellow] '[!] LA CONTRASEÑA DE GMAIL DE LA CUENTA DEL DESTINATARIO NO ES VÁLIDA O ESA CUENTA NO ESTÁ REGISTRADA[/bold yellow]"
                    )
                    sleep(2)
                    continue
            elif service == 27:
                console.print(
                    "[bold yellow][!] Nota[/bold yellow]: ¡La velocidad original no se puede restaurar!."
                )
                console.print("[bold yellow][!] Introduzca los detalles del vehículo.[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] ID de auto [/bold]")
                new_hp = IntPrompt.ask("[bold][?] Ponga un nuevo HP [/bold]")
                new_inner_hp = IntPrompt.ask("[bold][?] Ponga inner del HP[/bold]")
                new_nm = IntPrompt.ask("[bold][?]Enter Nuevo NM[/bold]")
                new_torque = IntPrompt.ask("[bold][?]Enter Nuevo Torque[/bold]")
                console.print("[bold yellow][%] Hackeando la velocidad del coche[/bold yellow]:", end=None)
                if cpm.hack_car_speed(car_id, new_hp, new_inner_hp, new_nm, new_torque):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print("================================")
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi tambiénl[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow] '[!] Por favor, utilice valores válidos[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 28:  # ANGLE
                console.print("[bold yellow] '[!] INGRESE LOS DETALLES DEL VEHÍCULO[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] ID del auto [/bold]")
                console.print("[bold yellow] '[!] INTRODUCIR EL ÁNGULO DE DIRECCIÓN[/bold yellow]")
                custom = IntPrompt.ask(
                    "[red][?]﻿INTRODUCE LA CANTIDAD DE ÁNGULO QUE DESEAS[/red]"
                )
                console.print("[red][%] HACKEANDO EL ÁNGULO DEL COCHE[/red]: ", end=None)
                if cpm.max_max1(car_id, custom):
                    console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                    answ = Prompt.ask(
                        "[red][?] ¿QUIERES SALIR? [/red] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 29:  # tire
                console.print("[bold yellow] '[!] INGRESE LOS DETALLES DEL VEHÍCULO[/bold yellow]")
                car_id = IntPrompt.ask("[bold][?] ID del auto[/bold]")
                console.print("[bold yellow] '[!] INTRODUCIR PORCENTAJE[/bold yellow]")
                custom = IntPrompt.ask("[pink][?]﻿INGRESE EL PORCENTAJE DE NEUMÁTICOS QUE DESEA[/pink]")
                console.print("[red][%] Ajuste de porcentaje [/red]: ", end=None)
                if cpm.max_max2(car_id, custom):
                    console.print("[bold yellow] 'EXITOSO[/bold yellow]")
                    answ = Prompt.ask(
                        "[bold green][?] ¿QUIERES SALIR?[/bold green] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 30:  # Millage
                console.print("[bold]¡INGRESE LOS DETALLES DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID del auto [/bold]")
                console.print("[bold]¡INGRESE EL NUEVO MILLAGE![/bold]")
                custom = IntPrompt.ask(
                    "[bold blue][?]﻿INGRESE EL KILOMETRAJE QUE DESEE[/bold blue]"
                )
                console.print(
                    "[bold yellow][%] Ajuste de porcentaje [/bold yellow]: ", end=None
                )
                if cpm.millage_car(car_id, custom):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 31:  # Brake
                console.print("[bold]INTRODUCIR LOS DATOS DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID del auto [/bold]")
                console.print("[bold]¡INTRODUCE NUEVO FRENO![/bold]")
                custom = IntPrompt.ask("[bold blue][?]﻿ENTRA EL FRENO QUE QUIERAS[/bold blue]")
                console.print("[bold yellow][%] Ajuste del FRENO [/bold yellow]: ", end=None)
                if cpm.brake_car(car_id, custom):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 32:  # Bumper rear
                console.print("[bold]INTRODUCIR LOS DATOS DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID del auto [/bold]")
                console.print(
                    "[bold yellow][%] Desmontaje del parachoques trasero [/bold yellow]: ", end=None
                )
                if cpm.rear_bumper(car_id):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 33:  # Bumper front
                console.print("[bold]¡INGRESE LOS DETALLES DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID del auto [/bold]")
                console.print(
                    "[bold yellow][%] Desmontaje del parachoques delantero [/bold yellow]: ", end=None
                )
                if cpm.front_bumper(car_id):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 75:  # /testin endpoint
                console.print("[bold]INTRODUCIR DATOS DE FLOTACIÓN PERSONALIZADOS[/bold]")
                custom = IntPrompt.ask(
                    "[bold][?] VALOR (e.g. 1 or 0)[/bold]"
                )  # This is the value
                console.print(
                    f"[bold yellow][%] Estableciendo llave flotante... [/bold yellow]", end=None
                )
                if cpm.testin(custom):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]POR FAVOR INTÉNTALO DE NUEVO[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 34:
                console.print("[bold]Introducir nueva contraseña![/bold]")
                new_password = prompt_valid_value(
                    "[bold][?] Cuenta Nueva Contraseña[/bold]", "Password", password=False
                )
                console.print("[bold yellow][%] Cambiar contraseña [/bold yellow]: ", end=None)
                if cpm.change_password(new_password):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white]Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]POR FAVOR INTÉNTALO DE NUEVO[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 36:  # telmunnongodz
                console.print("[bold]INTRODUCIR LOS DATOS DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID del auto [/bold]")
                console.print("[bold]INTRODUCIR ID DE SPOILER![/bold]")
                custom = IntPrompt.ask("[bold blue][?]INTRODUZCA EL NUEVO ID DE SPOILER[/bold blue]")
                console.print("[bold yellow][%] GUARDANDO SUS DATOS [/bold yellow]: ", end=None)
                if cpm.telmunnongodz(car_id, custom):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 37:  # telmunnongonz
                console.print("[bold]¡INGRESE LOS DETALLES DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID DEL COCHE[/bold]")
                console.print("[bold]INGRESE EL ID DEL BODYKIT![/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERTAR ID DEL BODYKIT[/bold blue]")
                console.print("[bold yellow][%] GUARDANDO SUS DATOS [/bold yellow]: ", end=None)
                if cpm.telmunnongonz(car_id, custom):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 49:  # telmunnongonz
                console.print("[bold]¡INGRESE LOS DETALLES DEL VEHÍCULO![/bold]")
                car_id = IntPrompt.ask("[bold][?] ID DEL COCHE[/bold]")
                console.print("[bold]INTRODUZCA EL VALOR DE LA POSTURA [/bold]")
                custom = IntPrompt.ask("[bold blue][?]INSERTAR VALOR[/bold blue]")
                console.print("[bold yellow][%] GUARDANDO SUS DATOS [/bold yellow]: ", end=None)
                if cpm.incline(car_id, custom):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 35:
                console.print("[bold]Ingrese un nuevo correo electrónico![/bold]")
                new_email = prompt_valid_value(
                    "[bold][?] Cuenta Nueva Correo Electrónico[/bold]", "Email"
                )
                console.print("[bold yellow][%] Cambiar el correo electrónico [/bold yellow]: ", end=None)
                if cpm.change_email(new_email):
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    answ = Prompt.ask(
                        "[bold][?] ¿QUIERES SALIR?[/bold] ?",
                        choices=["y", "n"],
                        default="n",
                    )
                    if answ == "y":
                        console.print(
                            "[bold white]Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        break
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]EL CORREO ELECTRÓNICO YA ESTÁ REGISTRADO [/bold yellow]")
                    sleep(4)
            elif service == 38:  # SHITTIN
                console.print("[%] Desbloqueo de ruedas premium..: ", end=None)
                if cpm.shittin():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 39:  # Unlock toyota crown
                console.print(
                    "[!] Nota: esta función tarda un tiempo en completarse, no la cancele.",
                    end=None,
                )
                console.print("[%] Desbloqueo de Toyota Crown: ", end=None)
                if cpm.unlock_crown():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 40:  # Unlock Hat
                console.print("[%] Desbloqueo del sombrero del clan: ", end=None)
                if cpm.unlock_hat_m():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 41:  # remove head male
                console.print("[%] Quitando la cabeza masculina: ", end=None)
                if cpm.rmhm():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 42:  # remove head female
                console.print("[%] Quitando la cabeza femenina: ", end=None)
                if cpm.rmhfm():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 43:  # Unlock TOPM
                console.print("[%] Desbloqueo de ropa de clan Top 1: ", end=None)
                if cpm.unlock_topm():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 44:  # Unlock TOPMz
                console.print("[%] Desbloqueo de ropa de clan Top 1: ", end=None)
                if cpm.unlock_topmz():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 45:  # Unlock TOPMX
                console.print("[%] Desbloqueo de ropa de clan Top 2: ", end=None)
                if cpm.unlock_topmx():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 46:  # Unlock TOPF
                console.print("[%] Desbloqueo de ropa de clan Superior: ", end=None)
                if cpm.unlock_topf():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 47:  # Unlock TOPFZ
                console.print("[%] Desbloqueo de ropa de clan Top 1: ", end=None)
                if cpm.unlock_topfz():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            elif service == 48:  # Unlock Mercedes Cls
                console.print("[%] Desbloqueo de Mercedes Cls: ", end=None)
                if cpm.unlock_cls():
                    console.print("[bold green]EXITOSO (✔)[/bold green]")
                    console.print(
                        "[bold green]======================================[/bold green]"
                    )
                    answ = Prompt.ask(
                        "[?] ¿Quieres salir?", choices=["y", "n"], default="n"
                    )
                    if answ == "y":
                        console.print(
                            "[bold white] Gracias por usar mi herramienta[/bold white]"
                        )
                    else:
                        continue
                else:
                    console.print("[bold yellow]FALLIDO[/bold yellow]")
                    console.print("[bold yellow]Por favor, inténtalo de nuevo[/bold yellow]")
                    sleep(2)
                    continue
            else:
                continue
            break
        break
